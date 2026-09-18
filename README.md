# Policy Desk

A small end-to-end support-ticket decision assistant built with FastAPI, SQLite, JWT, Streamlit, local retrieval, and Gemini.

<img width="1917" height="892" alt="image" src="https://github.com/user-attachments/assets/a34b0308-edf4-4766-8e39-2884dfc7a145" />


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

## Deploying the hosted app

Streamlit Cloud cannot reach `localhost:8000`. Deploy the FastAPI service separately, for example with the included `Dockerfile` and `render.yaml`. Set `GEMINI_API_KEY` and `JWT_SECRET` as backend service environment variables, then add this secret to Streamlit Cloud:

```toml
API_URL = "https://your-public-fastapi-service.example.com"
```

Do not put the Gemini key in GitHub, `.env.example`, or Streamlit source files. The hosted frontend only needs `API_URL`; the Gemini key belongs on the backend service.

## Design notes

The retriever stores its generated local index in `retrieval_index.pkl`, which is ignored by Git and rebuilt from `knowledge_base/*.md` when absent. Gemini output is parsed as JSON, checked against the allowed action enum, confidence range, and retrieved source names. Invalid or unavailable model output falls back to `NEEDS_MORE_INFORMATION` or a small deterministic policy workflow rather than inventing an answer.
