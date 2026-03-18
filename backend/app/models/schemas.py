"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel
from typing import Any


class GenerateEmailRequest(BaseModel):
    url: str
    applicant_name: str = "Abhay Kumar"
    applicant_skills: str = "Python, Machine Learning, LangChain, FastAPI, LLMs"
    applicant_experience: str = (
        "A passionate ML Engineer with hands-on experience building AI-powered applications, "
        "including LLM-based agents, RAG pipelines, and full-stack ML products."
    )
    applicant_github: str = "https://github.com/kabhay0120"
    applicant_linkedin: str = ""

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if isinstance(obj, dict) and "url" in obj:
            obj["url"] = obj["url"].strip()
            if not obj["url"].startswith(("http://", "https://")):
                raise ValueError("URL must start with http:// or https://")
        return super().model_validate(obj, *args, **kwargs)


class JobPosting(BaseModel):
    role: str = ""
    experience: str = ""
    skills: list[str] = []
    description: str = ""


class GenerateEmailResponse(BaseModel):
    email: str
    job: JobPosting
    provider_used: str
    portfolio_links: list[str]


class HealthResponse(BaseModel):
    status: str
    providers: list[dict[str, Any]]


class ErrorResponse(BaseModel):
    detail: str
    provider_attempted: str = ""
