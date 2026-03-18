"""
Email generator — uses LLM + PromptTemplate to draft a personalised job application email.
"""
import logging
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from app.models.schemas import JobPosting

logger = logging.getLogger(__name__)

APPLICATION_EMAIL_PROMPT = PromptTemplate.from_template(
    """
### JOB DESCRIPTION:
{job_description}

### APPLICANT PROFILE:
- Name: {applicant_name}
- Key Skills: {applicant_skills}
- Background & Experience: {applicant_experience}
- GitHub: {applicant_github}
- LinkedIn: {applicant_linkedin}

### RELEVANT PROJECTS / PORTFOLIO:
{portfolio_links}

### INSTRUCTION:
You are writing a professional job application email on behalf of {applicant_name}, who is applying for the role described above.

Your goal is to craft a compelling, concise, and highly personalised job application email addressed to the Hiring Manager. The email must:

1. Open with a strong hook that references the specific role and company.
2. Clearly and confidently connect the applicant's skills and experience to the job's key requirements — use specific examples or project references where possible.
3. Highlight 2-3 of the most relevant portfolio links (if provided) as proof of work.
4. Express genuine enthusiasm for the role and the company.
5. End with a clear call-to-action (e.g., requesting an interview/call).
6. Be professional yet personable in tone.
7. Stay under 300 words.
8. Do NOT include a subject line. Start directly with the salutation (e.g., "Dear Hiring Manager,").
9. Do NOT add any preamble, explanation, or markdown formatting — output the email text only.

### JOB APPLICATION EMAIL (NO PREAMBLE, START WITH SALUTATION):
"""
)


def generate_email(
    job: JobPosting,
    portfolio_links: list[str],
    llm: BaseChatModel,
    applicant_name: str = "Abhay Kumar",
    applicant_skills: str = "Python, Machine Learning, LangChain, FastAPI, LLMs",
    applicant_experience: str = "An ML Engineer with experience in AI-powered applications.",
    applicant_github: str = "https://github.com/kabhay0120",
    applicant_linkedin: str = "",
) -> str:
    """
    Generate a job application email for the given job posting.

    Args:
        job:                  Structured job posting data extracted from the URL.
        portfolio_links:      Relevant portfolio/project URLs matched to the job skills.
        llm:                  An initialised LangChain chat model.
        applicant_name:       Full name of the job applicant.
        applicant_skills:     Comma-separated list of the applicant's skills.
        applicant_experience: A short paragraph describing the applicant's background.
        applicant_github:     GitHub profile URL.
        applicant_linkedin:   LinkedIn profile URL.

    Returns:
        The generated job application email as a plain string.
    """
    logger.info(
        "Generating application email for role: %s | applicant: %s",
        job.role,
        applicant_name,
    )

    # Format portfolio links for the prompt
    if portfolio_links:
        link_list = "\n".join(f"- {link}" for link in portfolio_links)
    else:
        link_list = "No specific project links available."

    # Append GitHub/LinkedIn as additional contacts if provided
    contact_links = []
    if applicant_github:
        contact_links.append(f"GitHub: {applicant_github}")
    if applicant_linkedin:
        contact_links.append(f"LinkedIn: {applicant_linkedin}")
    if contact_links:
        link_list += "\n" + "\n".join(f"- {c}" for c in contact_links)

    chain = APPLICATION_EMAIL_PROMPT | llm
    res = chain.invoke(
        {
            "job_description": job.model_dump_json(indent=2),
            "applicant_name": applicant_name,
            "applicant_skills": applicant_skills,
            "applicant_experience": applicant_experience,
            "applicant_github": applicant_github,
            "applicant_linkedin": applicant_linkedin,
            "portfolio_links": link_list,
        }
    )
    email_text = res.content.strip()
    logger.info("Application email generated (%d characters).", len(email_text))
    return email_text
