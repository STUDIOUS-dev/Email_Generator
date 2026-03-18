"""
Web scraper — loads raw text content from a URL using LangChain's WebBaseLoader.
"""
import logging
from langchain_community.document_loaders import WebBaseLoader

logger = logging.getLogger(__name__)


def scrape_page(url: str) -> str:
    """
    Load and return the page text content from the given URL.

    Args:
        url: A publicly accessible job posting URL.

    Returns:
        Plain text content of the page.

    Raises:
        ValueError: If the page content is empty or could not be loaded.
    """
    logger.info("Scraping URL: %s", url)
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        if not docs:
            raise ValueError("No content loaded from URL.")
        page_content = docs[0].page_content.strip()
        if not page_content:
            raise ValueError("Page content is empty after loading.")
        logger.info("Scraped %d characters from %s", len(page_content), url)
        return page_content
    except Exception as exc:
        logger.error("Failed to scrape %s: %s", url, exc)
        raise ValueError(f"Could not scrape the URL. Ensure it is a public, accessible page. ({exc})")
