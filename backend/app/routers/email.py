"""
API router for email generation endpoints.
"""
import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateEmailRequest, GenerateEmailResponse, HealthResponse
from app.llm_manager import LLMManager
from app.services.scraper import scrape_page
from app.services.job_extractor import extract_job
from app.services.portfolio import portfolio_manager
from app.services.email_generator import generate_email

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Email Generator"])

# Re-use the same manager instance for the app lifetime
_llm_manager = LLMManager()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """
    Returns the service health status and the configured/available LLM providers.
    """
    return HealthResponse(status="ok", providers=_llm_manager.providers_status)


@router.post("/generate", response_model=GenerateEmailResponse, summary="Generate job application email")
async def generate_application_email(request: GenerateEmailRequest):
    """
    Full pipeline:
    1. Scrape the job posting URL
    2. Extract structured job data via LLM
    3. Query ChromaDB for relevant portfolio links matching the job's required skills
    4. Generate a personalised job application email via LLM

    All LLM calls use the active provider with automatic fallback.
    """
    provider_used = "unknown"
    try:
        # ── Step 1: Scrape ────────────────────────────────────────────────────
        page_data = scrape_page(request.url)

        # ── Step 2: Get LLM (returns cached provider — fast) ─────────────────
        llm, provider_used = _llm_manager.get_llm()

        # ── Step 3: Extract job (with automatic provider fallback) ────────────
        try:
            job = extract_job(page_data, llm)
        except Exception as llm_exc:
            logger.warning(
                "Provider %s failed during extraction (%s: %s). Trying next provider.",
                provider_used, type(llm_exc).__name__, llm_exc,
            )
            llm, provider_used = _llm_manager.try_next_provider()
            job = extract_job(page_data, llm)

        # ── Step 4: Portfolio links — match applicant projects to job skills ──
        # Combine job skills with applicant skills for a richer similarity search
        query_skills = list(job.skills)
        if request.applicant_skills:
            query_skills += [s.strip() for s in request.applicant_skills.split(",")]
        portfolio_links = portfolio_manager.query_links(query_skills, n_results=3)

        # ── Step 5: Generate application email (with provider fallback) ───────
        email_kwargs = dict(
            job=job,
            portfolio_links=portfolio_links,
            llm=llm,
            applicant_name=request.applicant_name,
            applicant_skills=request.applicant_skills,
            applicant_experience=request.applicant_experience,
            applicant_github=request.applicant_github,
            applicant_linkedin=request.applicant_linkedin,
        )
        try:
            email_text = generate_email(**email_kwargs)
        except Exception as llm_exc:
            logger.warning(
                "Provider %s failed during email generation (%s: %s). Trying next provider.",
                provider_used, type(llm_exc).__name__, llm_exc,
            )
            llm, provider_used = _llm_manager.try_next_provider()
            email_kwargs["llm"] = llm
            email_text = generate_email(**email_kwargs)

        return GenerateEmailResponse(
            email=email_text,
            job=job,
            provider_used=provider_used,
            portfolio_links=portfolio_links,
        )

    except ValueError as exc:
        logger.warning("Validation/scraping error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except RuntimeError as exc:
        logger.error("LLM provider error: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected error during email generation")
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")
