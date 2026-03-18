# Cold Email Generator

An AI-powered cold email generator that converts job posting URLs into personalised outreach emails. Built with **FastAPI** (backend) + **React + Vite + Tailwind CSS** (frontend).

---

## Architecture at a Glance

```
Email_Generator/
├── backend/              # FastAPI Python API
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # pydantic-settings (.env reader)
│   │   ├── llm_manager.py    # LLM fallback router
│   │   ├── models/           # Pydantic schemas
│   │   ├── routers/          # API route handlers
│   │   └── services/         # scraper, job extractor, portfolio, email gen
│   ├── my_portfolio.csv      # Portfolio data (customise this!)
│   ├── .env.example          # .env template
│   └── requirements.txt
├── frontend/             # React + Vite + Tailwind SPA
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api/emailApi.js
│   │   └── components/
│   └── tailwind.config.js
└── README.md
```

### How It Works

```
User (URL) → Scraper → Job Extractor (LLM) → ChromaDB Portfolio Query → Email Generator (LLM) → Response
```

### LLM Fallback Chain

| Order | Provider | Key |
|-------|----------|-----|
| 1 (Primary) | Gemini 1.5 Flash | `GEMINI_API_KEY` |
| 2 (Fallback) | Groq llama-3.1-70b | `GROQ_API_KEY` |
| 3 (Placeholder) | OpenAI GPT-4o-mini | `OPENAI_API_KEY` |
| 4 (Placeholder) | Anthropic Claude | `ANTHROPIC_API_KEY` |

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Backend

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
Copy-Item .env.example .env
# Then edit .env and fill in your API keys
notepad .env
```

**Required `.env` keys:**

```env
GEMINI_API_KEY=your_gemini_api_key_here   # Get from: https://aistudio.google.com/app/apikey
GROQ_API_KEY=your_groq_api_key_here       # Get from: https://console.groq.com/keys
```

> **Tip:** At minimum, one of the two keys above must be set. The app automatically uses whichever is available.

### 2. Customise Your Portfolio

Edit `backend/my_portfolio.csv` — replace the sample rows with your actual projects:

| Column | Description |
|--------|-------------|
| `Techstack` | Technologies used (e.g., `React, Node.js, MongoDB`) |
| `Links` | URL to your project or portfolio page |

The ChromaDB vector store is seeded automatically on first run.

### 3. Frontend

```powershell
cd frontend
npm install
```

---

## Running the Application

Start both the backend and frontend locally using a single command.

### Quick Start (Single Command)
From the **project root**:
```powershell
# Install concurrent tools (only needed once)
npm install

# Run both servers
npm run dev
```
This single command launches both the **FastAPI backend** (port `8000`) and the **React frontend** (port `5173`) concurrently.

### Alternative: Start Individually

Open **two terminals**:

**Terminal 1 — Backend:**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```powershell
cd frontend
npm run dev
```

Then open your browser at **http://localhost:5173**

Interactive API docs are available at **http://localhost:8000/api/docs**

---

## Adding a New LLM Provider

1. Install the provider's LangChain package (see commented lines in `requirements.txt`)
2. Add the API key to `.env` and `app/config.py`
3. Uncomment the corresponding block in `app/llm_manager.py`
4. Restart the backend

---

## Color Palette — `solid-pink`

| Token | Hex | Usage |
|-------|-----|-------|
| `pink-100` | `#f8ebeb` | App background, card surfaces |
| `pink-400` | `#d79599` | Borders, hover states, secondary text |
| `pink-700` | `#913f4d` | Primary buttons, active highlights |
| `pink-950` | `#3a171f` | Headings, body text |

---

## API Reference

See [`docs/API.md`](docs/API.md) for full endpoint documentation.
