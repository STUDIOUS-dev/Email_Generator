import logging
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _build_provider_definitions() -> list[dict[str, Any]]:
    """Return ordered list of provider definitions (name, available flag, factory fn)."""
    providers: list[dict[str, Any]] = []

    # ── 1. Groq / llama3 (PRIMARY) ───────────────────────────────────────────
    if settings.groq_api_key:
        def _make_groq():
            from langchain_groq import ChatGroq
            return ChatGroq(
                model="llama-3.3-70b-versatile",
                groq_api_key=settings.groq_api_key,
                temperature=0,
                max_retries=0,
            )
        providers.append({"name": "Groq (llama-3.3-70b-versatile)", "available": True, "factory": _make_groq})
    else:
        providers.append({"name": "Groq (llama-3.3-70b-versatile)", "available": False, "factory": None})

    # ── 2. Gemini (DISABLED — free-tier daily quota exhausted) ───────────────
    # langchain_google_genai ignores max_retries=0 for ResourceExhausted errors
    # and retries indefinitely, causing the app to hang. Re-enable below once
    # the daily quota resets (~midnight Pacific time).
    #
    # To re-enable: change "available": False  →  True  and restore the factory.
    providers.append({"name": "Gemini (gemini-2.0-flash)", "available": False, "factory": None})
    #
    # Full factory (un-comment the block below and remove the line above to restore):
    # if settings.gemini_api_key:
    #     def _make_gemini():
    #         from langchain_google_genai import ChatGoogleGenerativeAI
    #         return ChatGoogleGenerativeAI(
    #             model="gemini-2.0-flash",
    #             google_api_key=settings.gemini_api_key,
    #             temperature=0,
    #             convert_system_message_to_human=True,
    #             max_retries=0,
    #         )
    #     providers.append({"name": "Gemini (gemini-2.0-flash)", "available": True, "factory": _make_gemini})
    # else:
    #     providers.append({"name": "Gemini (gemini-2.0-flash)", "available": False, "factory": None})

    # ── 3. OpenAI (FALLBACK 2) — PLACEHOLDER ─────────────────────────────────
    # To enable:
    #   1. Uncomment `# langchain-openai==...` in requirements.txt and re-install
    #   2. Add OPENAI_API_KEY to your .env file
    #   3. Uncomment the block below:
    #
    # if settings.openai_api_key:
    #     def _make_openai():
    #         from langchain_openai import ChatOpenAI
    #         return ChatOpenAI(
    #             model="gpt-4o-mini",
    #             openai_api_key=settings.openai_api_key,
    #             temperature=0,
    #             max_retries=1,
    #         )
    #     providers.append({"name": "OpenAI (gpt-4o-mini)", "available": True, "factory": _make_openai})
    # else:
    #     providers.append({"name": "OpenAI (gpt-4o-mini)", "available": False, "factory": None})

    return providers


class LLMManager:
    """
    Manages LLM provider selection with lazy initialisation and caching.

    Strategy:
    - Providers are NOT smoke-tested at startup (avoids burning API quota on pings).
    - On the first real request, providers are tried in order. The first one that
      successfully completes a real invocation is cached and reused.
    - If the cached provider fails (e.g. rate-limited mid-session), call
      invalidate_cache() to force re-selection on the next request.
    """

    def __init__(self):
        self._provider_defs = _build_provider_definitions()
        self._active_llm: BaseChatModel | None = None
        self._active_name: str | None = None

    @property
    def providers_status(self) -> list[dict[str, Any]]:
        """Return provider availability overview (used by /api/health)."""
        return [
            {
                "name": p["name"],
                "available": p["available"],
                "active": (p["name"] == self._active_name),
            }
            for p in self._provider_defs
        ]

    def get_llm(self) -> tuple[BaseChatModel, str]:
        """
        Return the cached active LLM. Falls through to the next provider on failure.

        On first call (or after invalidate_cache()), each available provider is
        instantiated. The first provider that successfully processes a REAL request
        (not a smoke-test ping) is then cached.

        Returns:
            (llm_instance, provider_name) for the *first available* provider.
            The caller is responsible for catching invocation errors and calling
            invalidate_cache() + get_llm() to try the next provider.

        Raises:
            RuntimeError if no providers are configured.
        """
        if self._active_llm is not None:
            return self._active_llm, self._active_name  # type: ignore[return-value]

        # Find the first available provider and return it without probing
        for provider in self._provider_defs:
            if not provider["available"]:
                logger.info("Skipping %s — API key not configured.", provider["name"])
                continue
            try:
                llm = provider["factory"]()
                self._active_llm = llm
                self._active_name = provider["name"]
                logger.info("Selected provider: %s", provider["name"])
                return llm, provider["name"]
            except Exception as exc:
                logger.warning("Failed to instantiate %s: %s", provider["name"], exc)
                continue

        raise RuntimeError(
            "All LLM providers failed or are unconfigured. "
            "Please add at least one valid API key to your .env file."
        )

    def try_next_provider(self) -> tuple[BaseChatModel, str]:
        """
        Skip the current cached provider and activate the next available one.
        Used when the cached provider fails (rate limit, quota, etc.).

        Returns:
            (llm_instance, provider_name) for the next available provider.

        Raises:
            RuntimeError if no further providers are available.
        """
        failed_name = self._active_name
        logger.info("Falling through from %s to next provider.", failed_name)
        self._active_llm = None
        self._active_name = None

        # Skip past the failed provider
        past_failed = False
        for provider in self._provider_defs:
            if provider["name"] == failed_name:
                past_failed = True
                continue
            if not past_failed:
                continue
            if not provider["available"]:
                continue
            try:
                llm = provider["factory"]()
                self._active_llm = llm
                self._active_name = provider["name"]
                logger.info("Switched to provider: %s", provider["name"])
                return llm, provider["name"]
            except Exception as exc:
                logger.warning("Failed to instantiate %s: %s", provider["name"], exc)
                continue

        raise RuntimeError(
            f"No further LLM providers available after {failed_name} failed. "
            "Please add more API keys to your .env file."
        )

    def invalidate_cache(self) -> None:
        """Force re-selection on next get_llm() call (resets to first provider)."""
        logger.info("LLM cache invalidated. Will re-select on next request.")
        self._active_llm = None
        self._active_name = None
