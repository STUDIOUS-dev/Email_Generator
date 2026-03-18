"""
Job extractor — uses LLM + LangChain prompt to extract structured job posting data from raw page text.
"""
import json
import logging
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.models.schemas import JobPosting

logger = logging.getLogger(__name__)

EXTRACT_PROMPT = PromptTemplate.from_template(
    """
### SCRAPED TEXT FROM WEBSITE:
{page_data}

### INSTRUCTION:
The scraped text is from the career's page of a website.
Your job is to extract the job postings and return them in JSON format containing the
following keys: `role`, `experience`, `skills` and `description`.
- `skills` must be a JSON array of strings.
- Return only a single job posting (the most relevant one if multiple exist).
- Only return the valid JSON. No preamble, no explanation.

### VALID JSON (NO PREAMBLE):
"""
)


def extract_job(page_data: str, llm: BaseChatModel) -> JobPosting:
    """
    Extract structured job posting data from raw scraped text.

    Args:
        page_data: Raw text content from a job posting page.
        llm:       An initialised LangChain chat model.

    Returns:
        A JobPosting instance with role, experience, skills, description.

    Raises:
        ValueError: If the LLM output cannot be parsed into a valid JobPosting.
    """
    logger.info("Extracting job data from page content (%d chars)", len(page_data))
    chain = EXTRACT_PROMPT | llm
    res = chain.invoke({"page_data": page_data[:12000]})  # truncate to avoid token overflows

    # Try parsing via LangChain's JSON parser first, fall back to raw json.loads
    try:
        json_parser = JsonOutputParser()
        parsed = json_parser.parse(res.content)
    except Exception:
        try:
            parsed = json.loads(res.content)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse LLM response as JSON: %s", res.content[:500])
            raise ValueError(f"LLM did not return valid JSON for job extraction: {exc}")

    # Handle both dict and list responses
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}

    # Normalise skills field
    if isinstance(parsed.get("skills"), str):
        parsed["skills"] = [s.strip() for s in parsed["skills"].split(",") if s.strip()]

    try:
        job = JobPosting(**parsed)
        logger.info("Extracted job: role=%s, skills=%s", job.role, job.skills)
        return job
    except Exception as exc:
        raise ValueError(f"Job data doesn't match expected schema: {exc}")
