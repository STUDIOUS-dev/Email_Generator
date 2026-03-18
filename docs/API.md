# API Reference — Cold Email Generator

Base URL: `http://localhost:8000`

Interactive Swagger docs: `http://localhost:8000/api/docs`

---

## Endpoints

### `GET /api/health`

Returns service status and configured LLM providers.

**Response `200`:**
```json
{
  "status": "ok",
  "providers": [
    { "name": "Gemini (gemini-1.5-flash)", "available": true },
    { "name": "Groq (llama-3.1-70b-versatile)", "available": false }
  ]
}
```

---

### `POST /api/generate`

Runs the full pipeline: scrape → extract job → query portfolio → generate email.

**Request body:**
```json
{
  "url": "https://jobs.nike.com/job/R-33460",
  "sender_name": "Mohan",
  "company_name": "AtliQ",
  "company_description": "an AI & Software Consulting company..."
}
```

| Field | Type | Required | Default |
|-------|------|----------|---------|
| `url` | string | ✅ | — |
| `sender_name` | string | ❌ | `"Mohan"` |
| `company_name` | string | ❌ | `"AtliQ"` |
| `company_description` | string | ❌ | AtliQ default desc |

**Response `200`:**
```json
{
  "email": "Dear Hiring Team,\n\n...",
  "job": {
    "role": "Senior Software Engineer",
    "experience": "5+ years",
    "skills": ["Python", "React", "AWS"],
    "description": "..."
  },
  "provider_used": "Gemini (gemini-1.5-flash)",
  "portfolio_links": [
    "https://example.com/portfolio/python-fastapi"
  ]
}
```

**Error responses:**

| Code | Meaning |
|------|---------|
| `422` | Invalid URL or scraping failed |
| `503` | All LLM providers failed or unconfigured |
| `500` | Unexpected internal error |

---

## Pipeline Flow

```
POST /api/generate
  │
  ├─ 1. Scrape URL (WebBaseLoader)
  ├─ 2. Get LLM (Gemini → Groq → ... fallback)
  ├─ 3. Extract job JSON via LLM prompt
  ├─ 4. Query ChromaDB portfolio (by skills)
  └─ 5. Generate cold email via LLM prompt
```
