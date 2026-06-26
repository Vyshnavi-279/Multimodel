import streamlit as st
from llm import ask, MODELS, PRICES

st.set_page_config(page_title="AI Model Arena", page_icon="⚡", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0E1117;
    color: #E2E8F0;
}

/* ── Hide Streamlit chrome ── */
header[data-testid="stHeader"],
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { visibility: hidden; height: 0; }

.block-container {
    max-width: 1400px;
    padding: 3rem 2rem 4rem !important;
}

/* ════════════════════════════════════
   HERO SECTION
════════════════════════════════════ */
.arena-hero {
    text-align: center;
    padding: 3rem 0 2.5rem;
}
.arena-logo {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 1.5rem;
}
.arena-logo-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #06B6D4;
    box-shadow: 0 0 8px #06B6D4;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}
.arena-title {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.1;
    background: linear-gradient(135deg, #E2E8F0 0%, #94A3B8 40%, #06B6D4 70%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.arena-subtitle {
    font-size: 1.05rem;
    color: #64748B;
    font-weight: 400;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.6;
}

/* ════════════════════════════════════
   INPUT PANEL
════════════════════════════════════ */
.input-wrapper {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px 28px 20px;
    margin-bottom: 2rem;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 0 0 1px rgba(6,182,212,0.04), 0 20px 60px rgba(0,0,0,0.4);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.input-wrapper:focus-within {
    border-color: rgba(6,182,212,0.35);
    box-shadow: 0 0 0 1px rgba(6,182,212,0.15), 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(6,182,212,0.06);
}
.input-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}

/* Text area — force dark bg so typed text (light) stays visible */
.stTextArea textarea,
.stTextArea > div > div > textarea,
[data-testid="stTextArea"] textarea {
    background: #1A1F2E !important;
    color: #E2E8F0 !important;
    caret-color: #06B6D4 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
    padding: 14px 16px !important;
    resize: none !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(6,182,212,0.50) !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,0.12) !important;
    outline: none !important;
    background: #1E2438 !important;
}
.stTextArea textarea::placeholder,
[data-testid="stTextArea"] textarea::placeholder { color: #4B5563 !important; }

/* Multiselect */
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}
[data-baseweb="tag"] {
    background: rgba(129,140,248,0.18) !important;
    border: 1px solid rgba(129,140,248,0.35) !important;
    border-radius: 6px !important;
    color: #A5B4FC !important;
}
[data-baseweb="tag"] span { color: #A5B4FC !important; }

/* Compare button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C3AED 0%, #2563EB 50%, #06B6D4 100%) !important;
    background-size: 200% 200% !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    padding: 0.65rem 1.4rem !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.35), 0 4px 14px rgba(0,0,0,0.4) !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease !important;
    animation: gradient-shift 4s ease infinite !important;
}
@keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton > button[kind="primary"]:hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(124,58,237,0.55), 0 8px 24px rgba(0,0,0,0.5) !important;
}
.stButton > button:disabled {
    background: rgba(255,255,255,0.06) !important;
    color: #374151 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}

/* ════════════════════════════════════
   SECTION LABEL
════════════════════════════════════ */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,0.08) 0%, transparent 100%);
}

/* ════════════════════════════════════
   MODEL CARDS
════════════════════════════════════ */
.model-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 22px 22px 18px;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 420px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    position: relative;
    overflow: hidden;
}
.model-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(6,182,212,0.4), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.model-card:hover {
    transform: translateY(-5px);
    border-color: rgba(6,182,212,0.22);
    box-shadow: 0 12px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(6,182,212,0.10), inset 0 1px 0 rgba(255,255,255,0.08);
}
.model-card:hover::before { opacity: 1; }

/* Error card */
.model-card-error {
    background: rgba(239,68,68,0.06);
    border-color: rgba(239,68,68,0.25);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), 0 0 0 1px rgba(239,68,68,0.08);
}
.model-card-error:hover {
    border-color: rgba(239,68,68,0.40);
    box-shadow: 0 12px 40px rgba(0,0,0,0.45), 0 0 20px rgba(239,68,68,0.08);
}

/* Card header */
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.card-model-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #E2E8F0;
    letter-spacing: -0.2px;
}
.card-model-sub {
    font-size: 0.7rem;
    color: #475569;
    font-weight: 400;
    margin-top: 2px;
}
.card-provider-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* Answer body */
.card-body {
    flex-grow: 1;
    max-height: 300px;
    overflow-y: auto;
    padding-right: 6px;
    margin-bottom: 16px;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #94A3B8;
}
.card-body::-webkit-scrollbar { width: 4px; }
.card-body::-webkit-scrollbar-track { background: transparent; }
.card-body::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.10);
    border-radius: 2px;
}
.card-body::-webkit-scrollbar-thumb:hover { background: rgba(6,182,212,0.35); }

/* Metrics footer */
.card-footer {
    display: flex;
    gap: 8px;
    margin-top: auto;
    flex-wrap: wrap;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 6px;
    letter-spacing: 0.2px;
    font-family: 'Inter', monospace;
}
.badge-latency-fast  { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.30); color: #34D399; }
.badge-latency-med   { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.30); color: #FCD34D; }
.badge-latency-slow  { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.30);  color: #FCA5A5; }
.badge-cost-cheap    { background: rgba(6,182,212,0.10);  border: 1px solid rgba(6,182,212,0.28);  color: #67E8F9; }
.badge-cost-med      { background: rgba(129,140,248,0.10);border: 1px solid rgba(129,140,248,0.28);color: #A5B4FC; }
.badge-cost-high     { background: rgba(245,158,11,0.10); border: 1px solid rgba(245,158,11,0.28); color: #FCD34D; }
.badge-tokens        { background: rgba(255,255,255,0.05);border: 1px solid rgba(255,255,255,0.10);color: #64748B; }
.badge-error         { background: rgba(239,68,68,0.10);  border: 1px solid rgba(239,68,68,0.25);  color: #FCA5A5; }

/* Error body */
.card-error-msg {
    font-size: 0.85rem;
    line-height: 1.65;
    color: #F87171;
    margin-bottom: 16px;
    padding: 12px 14px;
    background: rgba(239,68,68,0.06);
    border-radius: 8px;
    border-left: 3px solid rgba(239,68,68,0.50);
    flex-grow: 1;
}

/* Spinner */
.stSpinner > div { color: #06B6D4 !important; }

/* Horizontal rule */
hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
PROVIDER_META = {
    "openai":    {"name": "OpenAI",    "color": "#10B981", "short": "GPT"},
    "anthropic": {"name": "Anthropic", "color": "#818CF8", "short": "Claude"},
    "google":    {"name": "Google",    "color": "#06B6D4", "short": "Gemini"},
    "qwen":      {"name": "Alibaba",   "color": "#F59E0B", "short": "Qwen"},
}

def latency_badge(sec: float) -> str:
    cls = "badge-latency-fast" if sec < 2 else ("badge-latency-med" if sec < 5 else "badge-latency-slow")
    return f'<span class="badge {cls}">⚡ {sec:.2f}s</span>'

def cost_badge(usd: float) -> str:
    cls = "badge-cost-cheap" if usd < 0.001 else ("badge-cost-med" if usd < 0.005 else "badge-cost-high")
    return f'<span class="badge {cls}">💰 ${usd:.5f}</span>'

def token_badge(inp: int, out: int) -> str:
    return f'<span class="badge badge-tokens">🔢 {inp}↑ {out}↓</span>'

def model_display(model: str):
    provider_key = model.split("/")[0]
    short_name   = model.split("/")[-1].replace("-", " ").title()
    meta = PROVIDER_META.get(provider_key, {"name": provider_key.title(), "color": "#64748B", "short": ""})
    return short_name, meta

def render_card(model: str, result: dict):
    short_name, meta = model_display(model)
    return f"""
    <div class="model-card">
        <div class="card-header">
            <div>
                <div class="card-model-name">{short_name}</div>
                <div class="card-model-sub">{meta['name']} · OpenRouter</div>
            </div>
            <div class="card-provider-dot" style="background:{meta['color']};
                box-shadow:0 0 8px {meta['color']};"></div>
        </div>
        <div class="card-body">{result['answer']}</div>
        <div class="card-footer">
            {latency_badge(result['latency'])}
            {cost_badge(result['cost'])}
            {token_badge(result.get('in_tokens', 0), result.get('out_tokens', 0))}
        </div>
    </div>"""

def render_error_card(model: str, err: str):
    short_name, meta = model_display(model)
    return f"""
    <div class="model-card model-card-error">
        <div class="card-header">
            <div>
                <div class="card-model-name" style="color:#F87171;">{short_name}</div>
                <div class="card-model-sub">{meta['name']} · OpenRouter</div>
            </div>
            <div class="card-provider-dot" style="background:#EF4444;box-shadow:0 0 8px #EF4444;"></div>
        </div>
        <div class="card-error-msg">{err}</div>
        <div class="card-footer">
            <span class="badge badge-error">✕ Model Failed</span>
        </div>
    </div>"""


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="arena-hero">
    <div class="arena-logo">
        <span class="arena-logo-dot"></span>
        AI Model Arena
        <span class="arena-logo-dot"></span>
    </div>
    <div class="arena-title">Compare Every Model.<br>Find the Best Answer.</div>
    <div class="arena-subtitle">
        Send one question to the world's top LLMs simultaneously.
        Measure speed, cost, and quality — side by side.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input Panel ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Your Question</div>', unsafe_allow_html=True)

question = st.text_area(
    "q",
    placeholder="Ask anything… e.g. 'Explain the CAP theorem in 3 bullet points.'",
    height=90,
    label_visibility="collapsed",
)

col_sel, col_gap, col_btn = st.columns([3, 0.15, 1])
with col_sel:
    selected_models = st.multiselect(
        "m",
        MODELS,
        default=MODELS,
        label_visibility="collapsed",
    )
with col_btn:
    is_disabled = not question.strip() or not selected_models
    run_clicked = st.button(
        "⚡ Run Arena",
        type="primary",
        use_container_width=True,
        disabled=is_disabled,
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if run_clicked:
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    with st.spinner("Querying models…"):
        cols = st.columns(len(selected_models), gap="medium")
        for i, model in enumerate(selected_models):
            with cols[i]:
                try:
                    result = ask(question, model)
                    st.markdown(render_card(model, result), unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(render_error_card(model, str(e)), unsafe_allow_html=True)
