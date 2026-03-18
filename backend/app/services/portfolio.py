"""
Portfolio service — loads portfolio data from CSV and manages the ChromaDB vector store.

The collection is seeded on first run from my_portfolio.csv.
Subsequent runs reuse the persisted store.
"""
import uuid
import logging
import pandas as pd
import chromadb
from pathlib import Path
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PortfolioManager:
    """
    Manages the ChromaDB collection that stores portfolio entries.
    Each entry maps a tech stack string to a portfolio project URL.
    """

    def __init__(self):
        self._client: chromadb.ClientAPI | None = None
        self._collection: chromadb.Collection | None = None

    def _get_collection(self) -> chromadb.Collection:
        if self._collection is not None:
            return self._collection

        vectorstore_path = settings.vectorstore_path
        csv_path = settings.portfolio_csv_path

        logger.info("Initialising ChromaDB at path: %s", vectorstore_path)
        self._client = chromadb.PersistentClient(path=vectorstore_path)
        self._collection = self._client.get_or_create_collection(name="portfolio")

        # Seed with CSV data on first run (when collection is empty)
        if self._collection.count() == 0:
            logger.info("Portfolio collection is empty. Seeding from %s ...", csv_path)
            if not Path(csv_path).exists():
                logger.warning("Portfolio CSV not found at %s. Skipping seed.", csv_path)
                return self._collection

            df = pd.read_csv(csv_path)
            if "Techstack" not in df.columns or "Links" not in df.columns:
                raise ValueError("Portfolio CSV must have columns: 'Techstack', 'Links'")

            ids, docs, metas = [], [], []
            for _, row in df.iterrows():
                if pd.isna(row["Techstack"]) or pd.isna(row["Links"]):
                    continue
                ids.append(str(uuid.uuid4()))
                docs.append(str(row["Techstack"]))
                metas.append({"links": str(row["Links"])})

            if ids:
                self._collection.add(documents=docs, metadatas=metas, ids=ids)
                logger.info("Seeded %d portfolio entries into ChromaDB.", len(ids))

        return self._collection

    def query_links(self, skills: list[str], n_results: int = 2) -> list[str]:
        """
        Query the portfolio vector store for the most relevant project links
        given a list of required skills.

        Args:
            skills:    List of skill strings extracted from the job description.
            n_results: How many links to return per skill query.

        Returns:
            Flat, deduplicated list of portfolio URLs.
        """
        if not skills:
            return []

        collection = self._get_collection()
        if collection.count() == 0:
            logger.warning("Portfolio collection is empty — returning no links.")
            return []

        query_texts = skills[:5]  # Cap to avoid very long queries
        try:
            results = collection.query(
                query_texts=query_texts,
                n_results=min(n_results, collection.count()),
            )
            metadatas = results.get("metadatas", [])
        except Exception as exc:
            logger.error("ChromaDB query failed: %s", exc)
            return []

        seen: set[str] = set()
        links: list[str] = []
        for meta_group in metadatas:
            for meta in meta_group:
                link = meta.get("links", "")
                if link and link not in seen:
                    seen.add(link)
                    links.append(link)
        return links


# Module-level singleton — shared across the app lifetime
portfolio_manager = PortfolioManager()
