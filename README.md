# Policy Desk

A small support-ticket decision assistant built with Streamlit, SQLite, JWT, local retrieval, and Gemini. The Streamlit app can run standalone without a FastAPI server.

<img width="1917" height="892" alt="image" src="https://github.com/user-attachments/assets/a34b0308-edf4-4766-8e39-2884dfc7a145" />
<img width="1892" height="892" alt="image" src="https://github.com/user-attachments/assets/2a8436c8-54cd-436f-9c83-9c0549e8d48b" />



## Features

- User registration and login with Argon2 password hashes and JWT bearer tokens
- Ticket creation, persisted decisions, history, and ownership-protected detail access
- Local policy retrieval using chunked Markdown, TF-IDF weighting, and cosine KNN
- Structured decision output validated with Pydantic
- Gemini support when `GEMINI_API_KEY` is configured, with a deterministic policy-grounded fallback for local development
- Offline API tests and an evaluation runner

## Setup

Use Python 3.11+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `GEMINI_API_KEY` and a long random `JWT_SECRET` in `.env` for Gemini-backed decisions. The application works without the Gemini key using the local fallback.

## Run

Start the API:

```powershell
python -m src
```

In another terminal, start Streamlit:

```powershell
streamlit run streamlit_app.py
```

Open `http://localhost:8501`, register, log in, and submit a ticket.

## Test and evaluate

```powershell
pytest -q
python evaluate.py
```

The API is available at `http://localhost:8000`; interactive docs are at `/docs`. The Streamlit client communicates with the API over HTTP and never accesses SQLite directly.

## Deploying the standalone Streamlit app

Deploy `streamlit_app.py` directly on Streamlit Community Cloud. In the app settings, add these secrets:

```toml
GEMINI_API_KEY = "your-new-gemini-key"
JWT_SECRET = "your-long-random-secret"
DATABASE_URL = "sqlite:///./support_ai.db"
```

The standalone app performs registration, login, ticket persistence, retrieval, and Gemini decisions directly. It does not call `localhost:8000` or require FastAPI to be running. Do not put the Gemini key in GitHub, `.env.example`, or Streamlit source files.

The FastAPI backend and included `Dockerfile`/`render.yaml` remain available as an optional REST deployment when API separation is required.

## Design notes

The retriever stores its generated local index in `retrieval_index.pkl`, which is ignored by Git and rebuilt from `knowledge_base/*.md` when absent. Gemini output is parsed as JSON, checked against the allowed action enum, confidence range, and retrieved source names. Invalid or unavailable model output falls back to `NEEDS_MORE_INFORMATION` or a small deterministic policy workflow rather than inventing an answer.
