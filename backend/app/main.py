import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers.email import router as email_router

# ── Logging config ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle hook."""
    logger.info("Cold Email Generator API starting up...")
    yield
    logger.info("Cold Email Generator API shutting down.")


# ── App factory ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Cold Email Generator API",
    description=(
        "AI-powered cold email generator. "
        "Scrapes job postings, extracts structured data, "
        "matches portfolio links via vector search, "
        "and drafts personalised outreach emails."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(email_router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Cold Email Generator API",
        "docs": "/api/docs",
        "health": "/api/health",
    }
