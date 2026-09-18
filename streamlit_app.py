import requests
import streamlit as st

st.set_page_config(page_title="Policy Desk", page_icon="P", layout="wide")
API_URL = st.sidebar.text_input("API URL", "http://localhost:8000").rstrip("/")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --ink: #17243b;
    --muted: #65728a;
    --paper: #f6f7fb;
    --panel: rgba(255, 255, 255, 0.84);
    --line: #dfe5ef;
    --coral: #e76f51;
    --teal: #0f8b8d;
    --yellow: #f4c95d;
}

.stApp {
    color: var(--ink);
    background:
        linear-gradient(rgba(15, 139, 141, .035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15, 139, 141, .035) 1px, transparent 1px),
        linear-gradient(135deg, #f8fafc 0%, #eef3f6 56%, #fff8f1 100%);
    background-size: 28px 28px, 28px 28px, auto;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #17243b; border-right: 0; }
[data-testid="stSidebar"] * { color: #eaf1f4 !important; }
[data-testid="stSidebar"] input { color: var(--ink) !important; background: #ffffff !important; }
[data-testid="stSidebar"] button { border-color: rgba(255,255,255,.28) !important; }

.block-container { max-width: 1180px; padding: 2.2rem 2.2rem 4rem; }
h1, h2, h3, p, label, button { font-family: 'Space Grotesk', sans-serif !important; }
h1 { letter-spacing: 0 !important; font-weight: 700 !important; }
h2, h3 { letter-spacing: 0 !important; }

.brandbar { display: flex; justify-content: space-between; align-items: center; gap: 1rem; margin: .25rem 0 2.2rem; }
.brandmark { display: flex; align-items: center; gap: .8rem; }
.brand-symbol { display: grid; place-items: center; width: 42px; height: 42px; border-radius: 12px; color: white; background: var(--coral); font-family: 'DM Mono', monospace; font-weight: 500; box-shadow: 7px 7px 0 var(--yellow); animation: floatMark 4s ease-in-out infinite; }
.brand-name { font-size: 1.1rem; font-weight: 700; line-height: 1; }
.brand-kicker { color: var(--muted); font-family: 'DM Mono', monospace; font-size: .67rem; letter-spacing: .12em; text-transform: uppercase; margin-top: .35rem; }
.live-pill { color: var(--teal); border: 1px solid rgba(15,139,141,.25); background: rgba(255,255,255,.65); border-radius: 99px; padding: .45rem .7rem; font-family: 'DM Mono', monospace; font-size: .7rem; }
.live-dot { display: inline-block; width: 7px; height: 7px; margin-right: .35rem; border-radius: 50%; background: var(--teal); animation: pulseDot 1.8s ease-in-out infinite; }

.login-intro { padding: 1.5rem 0 1.1rem; max-width: 650px; }
.login-intro .eyebrow { color: var(--coral); font-family: 'DM Mono', monospace; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; }
.login-intro h1 { font-size: clamp(2.6rem, 6vw, 5.2rem); line-height: .95; margin: .75rem 0 1rem; }
.login-intro p { color: var(--muted); font-size: 1.05rem; max-width: 520px; }
.workspace-intro { border-left: 4px solid var(--coral); padding-left: 1rem; margin: .4rem 0 1.8rem; }
.workspace-intro h1 { margin: 0; font-size: clamp(2rem, 4vw, 3.3rem); }
.workspace-intro p { color: var(--muted); margin: .45rem 0 0; }

[data-testid="stForm"], [data-testid="stExpander"] { background: var(--panel); border: 1px solid rgba(223,229,239,.92); border-radius: 16px; box-shadow: 0 15px 45px rgba(23,36,59,.07); }
[data-testid="stForm"] { padding: .8rem; }
.decision-summary { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(150px, .6fr); gap: 1rem; align-items: stretch; margin: .4rem 0 1rem; }
.decision-summary > div { padding: 1rem 1.1rem; border: 1px solid #dce4ee; border-radius: 13px; background: rgba(255,255,255,.9); box-shadow: 0 8px 22px rgba(23,36,59,.06); }
.decision-summary-label { color: #65728a; font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; }
.decision-summary-title { color: #17243b !important; font-size: 1.2rem; font-weight: 700; margin-top: .45rem; }
.decision-summary-action { color: #b94f39 !important; font-size: 1.45rem; font-weight: 700; line-height: 1.15; margin-top: .45rem; }
.decision-summary-confidence { color: #0f8b8d !important; font-family: 'DM Mono', monospace; font-size: 1.55rem; font-weight: 600; margin-top: .35rem; }
[data-testid="stMarkdownContainer"] .decision-summary * { opacity: 1 !important; }
[data-testid="stTextInput"] label, [data-testid="stTextArea"] label { color: var(--ink) !important; font-weight: 600 !important; font-size: .88rem !important; }
[data-testid="stTextInput"] [data-baseweb="input"], [data-testid="stTextInput"] [data-baseweb="input"] > div, [data-testid="stTextArea"] [data-baseweb="textarea"], [data-testid="stTextArea"] [data-baseweb="textarea"] > div { background: #ffffff !important; background-color: #ffffff !important; border: 2px solid #c7d2df !important; border-radius: 12px !important; box-shadow: 0 5px 14px rgba(23,36,59,.06); color-scheme: light; transition: border-color .18s ease, box-shadow .18s ease, transform .18s ease; }
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within, [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within { border-color: var(--teal) !important; box-shadow: 0 0 0 4px rgba(15,139,141,.15), 0 7px 18px rgba(23,36,59,.08); transform: translateY(-1px); }
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { min-height: 48px; border: 0 !important; border-radius: 10px; background: #ffffff !important; background-color: #ffffff !important; color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; caret-color: var(--coral) !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 1rem !important; }
[data-testid="stTextArea"] textarea { min-height: 150px; padding-top: .8rem; }
[data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder { color: #7a879b !important; opacity: 1 !important; -webkit-text-fill-color: #7a879b !important; }
[data-testid="stTextInput"] button { color: #ffffff !important; background: var(--ink) !important; border-radius: 0 10px 10px 0 !important; }
button[kind="primary"] { background: var(--coral) !important; border: 0 !important; color: white !important; box-shadow: 0 7px 0 #b94f39; transition: transform .18s ease, box-shadow .18s ease; }
button[kind="primary"]:hover { background: #d85e42 !important; transform: translateY(-2px); box-shadow: 0 9px 0 #b94f39; }
[data-testid="stTabs"] [role="tab"] { min-height: 42px; margin-right: .45rem; padding: .55rem 1rem !important; border: 1px solid #c7d2df !important; border-radius: 10px 10px 0 0 !important; background: rgba(255,255,255,.92) !important; color: var(--ink) !important; font-family: 'DM Mono', monospace !important; text-transform: uppercase; font-size: .73rem; letter-spacing: .08em; opacity: 1 !important; transition: background .18s ease, color .18s ease, transform .18s ease; }
[data-testid="stTabs"] [role="tab"] p { color: var(--ink) !important; font-weight: 500 !important; }
[data-testid="stTabs"] [role="tab"]:hover { color: var(--coral) !important; transform: translateY(-2px); }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { background: var(--coral) !important; border-color: var(--coral) !important; color: #ffffff !important; box-shadow: 0 4px 0 #b94f39; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] p { color: #ffffff !important; }
[data-testid="stTabs"] [data-baseweb="tab-border"] { background: var(--teal) !important; height: 3px !important; }
[data-testid="stAlert"] { border: 1px solid #ef8b79 !important; border-left: 5px solid #c83d2a !important; background: #fff0ed !important; color: #8d251b !important; border-radius: 10px !important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] span { color: #8d251b !important; font-weight: 600 !important; }
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, var(--teal), var(--yellow), var(--coral)); }
.decision-rail { height: 5px; border-radius: 99px; margin: .25rem 0 1.35rem; background: linear-gradient(90deg, var(--teal), var(--yellow), var(--coral)); background-size: 180% 100%; animation: driftRail 5s ease-in-out infinite; }
.source-chip { display: inline-block; border-radius: 99px; padding: .25rem .55rem; margin: .15rem .25rem .15rem 0; background: #e7f4f3; color: #176b6c; font-family: 'DM Mono', monospace; font-size: .68rem; }
.section-label { color: var(--muted); font-family: 'DM Mono', monospace; font-size: .7rem; text-transform: uppercase; letter-spacing: .12em; }

@keyframes floatMark { 0%, 100% { transform: translateY(0) rotate(0); } 50% { transform: translateY(-4px) rotate(3deg); } }
@keyframes pulseDot { 0%, 100% { box-shadow: 0 0 0 0 rgba(15,139,141,.25); } 50% { box-shadow: 0 0 0 6px rgba(15,139,141,0); } }
@keyframes driftRail { 0%, 100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }

@media (max-width: 700px) {
    .block-container { padding: 1.25rem 1rem 3rem; }
    .brandbar { margin-bottom: 1.2rem; }
    .live-pill { display: none; }
    .login-intro h1 { font-size: 3rem; }
    [data-testid="stMetricValue"] { font-size: 1.35rem; }
    .decision-summary { grid-template-columns: 1fr; gap: .7rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


def api_request(method: str, path: str, **kwargs):
    headers = kwargs.pop("headers", {})
    if st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state['token']}"
    try:
        response = requests.request(method, f"{API_URL}{path}", headers=headers, timeout=90, **kwargs)
        if response.status_code >= 400:
            st.error(response.json().get("detail", response.text))
            return None
        return response.json()
    except requests.RequestException as error:
        st.error(f"Could not reach the API: {error}")
        return None


ACTION_GUIDANCE = {
    "REQUEST_PHOTOS": {
        "recommendation": "Request clear photos of the package and the damaged item before promising a refund or replacement.",
        "steps": ["Ask for the order number.", "Ask for clear photos of the package and item.", "Review the evidence before choosing a refund or replacement."],
        "rules": ["Do not promise an outcome before damage is verified.", "Use the damaged-goods policy as the evidence source."],
    },
    "REQUEST_ORDER_DETAILS": {
        "recommendation": "Collect the missing order details and item information before taking action.",
        "steps": ["Ask for the order number.", "Confirm the delivery or shipping status.", "Ask for item-condition details or a photo when the policy requires it."],
        "rules": ["Do not confirm a refund, cancellation, or replacement without the required facts.", "Escalate when the policy window or shipping status is unclear."],
    },
    "REFUND": {
        "recommendation": "Proceed with a refund review under the applicable policy.",
        "steps": ["Verify the order number and return eligibility.", "Confirm the item condition.", "Issue the refund to the original payment method after inspection."],
        "rules": ["Refund shipping fees only for defective or wrong items.", "Do not invent eligibility when policy facts are missing."],
    },
    "REPLACE": {
        "recommendation": "Proceed with a replacement review under the applicable policy.",
        "steps": ["Verify the order and problem evidence.", "Check replacement stock.", "Provide return instructions when required."],
        "rules": ["Do not promise replacement before verification.", "Use a refund when policy or stock rules require it."],
    },
    "ESCALATE": {
        "recommendation": "Escalate the ticket to the appropriate support team for review.",
        "steps": ["Record the order number and all evidence.", "Summarize the policy issue.", "Send the case to the shipping or support team."],
        "rules": ["Escalate outside-policy-window cases.", "Do not promise an outcome before review."],
    },
    "DENY": {
        "recommendation": "Explain the policy-based denial clearly and provide any available alternative.",
        "steps": ["Confirm the relevant policy facts.", "Explain the reason in customer-friendly language.", "Offer the return or escalation route when applicable."],
        "rules": ["Base the denial on retrieved policy evidence.", "Do not deny when required facts are missing."],
    },
    "NEEDS_MORE_INFORMATION": {
        "recommendation": "Ask the customer for the missing facts before making a final decision.",
        "steps": ["Identify the missing order or item details.", "Ask one concise follow-up request.", "Reassess the ticket after the customer replies."],
        "rules": ["Do not invent an answer when policy evidence is insufficient.", "Keep the case open until the required information is available."],
    },
}


def render_decision(ticket: dict) -> None:
    decision = ticket["decision"]
    action = decision["action"]
    confidence = max(0.0, min(1.0, float(decision["confidence"])))
    guidance = ACTION_GUIDANCE.get(action, ACTION_GUIDANCE["NEEDS_MORE_INFORMATION"])
    st.markdown('<div class="decision-rail"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="decision-summary"><div><div class="decision-summary-label">Decision for ticket #{ticket["id"]}</div><div class="decision-summary-title">Recommended action</div><div class="decision-summary-action">{action.replace("_", " ").title()}</div></div><div><div class="decision-summary-label">Confidence</div><div class="decision-summary-confidence">{confidence:.1%}</div></div></div>',
        unsafe_allow_html=True,
    )
    st.progress(confidence, text=f"Decision confidence: {confidence:.1%}")
    st.info(guidance["recommendation"])
    st.write(f"**Evidence-based reasoning:** {decision['reason']}")
    steps_col, rules_col = st.columns(2)
    with steps_col:
        st.markdown("**Suggested steps**")
        for step in guidance["steps"]:
            st.markdown(f"- {step}")
    with rules_col:
        st.markdown("**Rules to follow**")
        for rule in guidance["rules"]:
            st.markdown(f"- {rule}")
    source_html = "".join(f'<span class="source-chip">{source}</span>' for source in decision["sources"])
    st.markdown(f'<div class="section-label">Retrieved policy evidence</div>{source_html}', unsafe_allow_html=True)


if "token" not in st.session_state:
    st.session_state.token = None
if "selected_ticket" not in st.session_state:
    st.session_state.selected_ticket = None

st.markdown(
    '<div class="brandbar"><div class="brandmark"><div class="brand-symbol">PD</div><div><div class="brand-name">Policy Desk</div><div class="brand-kicker">Decision intelligence / support ops</div></div></div><div class="live-pill"><span class="live-dot"></span>LOCAL WORKSPACE</div></div>',
    unsafe_allow_html=True,
)

if not st.session_state.token:
    st.markdown('<div class="login-intro"><div class="eyebrow">Evidence, not guesswork</div><h1>Make every support decision feel considered.</h1><p>Bring a customer message. Policy Desk finds the relevant rules, explains the recommendation, and keeps the evidence attached.</p></div>', unsafe_allow_html=True)
    login_tab, register_tab = st.tabs(["Log in", "Register"])
    with login_tab:
        with st.form("login"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log in", type="primary")
        if submitted:
            result = api_request("POST", "/login", json={"email": email, "password": password})
            if result:
                st.session_state.token = result["access_token"]
                st.rerun()
    with register_tab:
        with st.form("register"):
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password (8+ characters)", type="password", key="register_password")
            submitted = st.form_submit_button("Create account", type="primary")
        if submitted:
            result = api_request("POST", "/register", json={"email": email, "password": password})
            if result:
                st.success("Account created. You can now log in.")
    st.stop()

user = api_request("GET", "/me")
st.sidebar.write(f"Signed in as {user['email'] if user else 'user'}")
if st.sidebar.button("Log out"):
    st.session_state.token = None
    st.rerun()

st.markdown('<div class="workspace-intro"><h1>Good decisions, documented.</h1><p>Turn the next customer message into a grounded action plan.</p></div>', unsafe_allow_html=True)
new_tab, history_tab = st.tabs(["New decision", "History"])
with new_tab:
    st.markdown('<div class="section-label">Intake / new case</div>', unsafe_allow_html=True)
    st.subheader("What happened?")
    with st.form("ticket"):
        message = st.text_area("Customer message", height=180, placeholder="Example: My package arrived damaged, what should I send?")
        submitted = st.form_submit_button("Generate decision", type="primary")
    if submitted:
        result = api_request("POST", "/tickets", json={"message": message})
        if result:
            st.session_state.selected_ticket = result
    if st.session_state.selected_ticket:
        result = st.session_state.selected_ticket
        st.divider()
        render_decision(result)

with history_tab:
    st.markdown('<div class="section-label">Archive / decision trail</div>', unsafe_allow_html=True)
    st.subheader("Previous tickets")
    tickets = api_request("GET", "/tickets") or []
    if not tickets:
        st.info("No decisions yet.")
    for ticket in tickets:
        decision = ticket["decision"]
        with st.expander(f"#{ticket['id']} · {decision['action'] if decision else 'Pending'} · {ticket['created_at'][:10]}"):
            st.write(ticket["message"])
            if decision:
                render_decision(ticket)
