# Policy Desk Deployment Guide

## Streamlit Cloud deployment

The application runs as a standalone Streamlit app. It does not require FastAPI for the hosted Streamlit deployment.

### 1. Open the app settings

1. Open https://share.streamlit.io/.
2. Select the Policy Desk app.
3. Open the app menu and choose **Settings**.
4. Select **Secrets**.

### 2. Add the secrets

Paste this TOML configuration into the Secrets editor:

```toml
GEMINI_API_KEY = "your-new-gemini-api-key"
JWT_SECRET = "replace-with-a-long-random-secret"
DATABASE_URL = "sqlite:///./support_ai.db"
```

Replace `GEMINI_API_KEY` with the newly generated Gemini key. Do not commit this value to GitHub.

### 3. Confirm the app entry point

Use these deployment settings:

```text
Repository: Arunchand19/Decision-Desk_AI
Branch: main
Main file: streamlit_app.py
```

Save the settings, then click **Reboot app** or **Re-run**.

### 4. Test the application

1. Open the deployed Streamlit URL.
2. Select **Register**.
3. Create an account with an email and password of at least 8 characters.
4. Select **Log in**.
5. Submit a support ticket.
6. Confirm that the decision, confidence, reasoning, next steps, rules, and policy sources appear.

## Local development

Create a local `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your-new-gemini-api-key
JWT_SECRET=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./support_ai.db
```

Start the standalone app:

```powershell
cd C:\Users\arunc\Documents\AI_backend_Project
.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Open http://localhost:8501.

The standalone app does not need `API_URL` and does not call `localhost:8000`.

## Security warning

The Gemini key previously placed in `.env` was exposed in chat and should be revoked in Google AI Studio. Generate a replacement key and configure it only in:

- Streamlit Cloud Secrets for the hosted app
- The local ignored `.env` file for development

Never commit `.env`, `.streamlit/secrets.toml`, API keys, JWT secrets, or passwords.

## Verification commands

Run the tests and compile checks locally:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m py_compile streamlit_app.py
```
