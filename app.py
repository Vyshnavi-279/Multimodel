import streamlit as st
from llm import ask, MODELS, PRICES

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS (The "Beauty")
# ==========================================
st.set_page_config(page_title="LLM Arena", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* Clean up default Streamlit padding/menus for a custom app feel */
    .stApp { background-color: #f8f9fa; }
    header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
    #MainMenu, footer { visibility: hidden; }

    /* Card Styling */
    .model-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        height: 100%;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease;
    }
    .model-card:hover { transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0,0,0,0.08); }
    
    /* Error Card Styling (FR-6) */
    .model-card-error {
        background: #fff5f5;
        border: 1px solid #ffc9c9;
    }

    /* Typography */
    .model-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #212529;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 3px solid #0d6efd;
    }
    
    /* Scrollable Answer Box */
    .answer-box {
        flex-grow: 1;
        max-height: 350px;
        overflow-y: auto;
        padding-right: 10px;
        line-height: 1.6;
        color: #495057;
        margin-bottom: 15px;
    }
    .answer-box::-webkit-scrollbar { width: 6px; }
    .answer-box::-webkit-scrollbar-thumb { background: #ced4da; border-radius: 3px; }
    
    /* Metrics Footer */
    .metrics-row {
        display: flex;
        justify-content: space-around;
        background: #f1f3f5;
        border-radius: 8px;
        padding: 12px;
        margin-top: auto;
    }
    .metric { text-align: center; }
    .metric-val { font-size: 1.25rem; font-weight: 700; color: #0d6efd; }
    .metric-lbl { font-size: 0.75rem; color: #868e96; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HEADER & INPUT (Prompt A & D)
# ==========================================
st.title("⚡ Multi-Model Comparison Tool")
st.caption("Ask one question. Compare answers, speed, and cost across leading LLMs side-by-side.")

with st.container():
    question = st.text_area(
        "Your Question",
        placeholder="e.g., Explain the difference between TCP and UDP in 3 bullet points.",
        height=100,
        label_visibility="collapsed"
    )
    
    # Layout: Models selection on the left, Button on the right
    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        selected_models = st.multiselect(
            "Models to compare",
            MODELS,
            default=MODELS,
            label_visibility="collapsed"
        )
    with col_btn:
        # Prompt D: Disable button if question is empty or no models selected
        is_disabled = not question.strip() or not selected_models
        compare_clicked = st.button(
            "🚀 Compare Models", 
            type="primary", 
            use_container_width=True, 
            disabled=is_disabled
        )

# ==========================================
# 3. RESULTS & ERROR HANDLING (Prompts B & C, FR-6)
# ==========================================
if compare_clicked:
    # Prompt B: Show spinner while calls run
    with st.spinner("Consulting the models... ⏳"):
        # Create dynamic columns based on how many models were selected
        cols = st.columns(len(selected_models))
        
        for i, model in enumerate(selected_models):
            with cols[i]:
                try:
                    # Prompt B: Call the engine
                    result = ask(question, model)
                    
                    # Prompt C: Lay out as beautiful cards
                    st.markdown(f'<div class="model-card">', unsafe_allow_html=True)
                    
                    # Clean up model name for display (e.g., "anthropic/claude-opus-4.8" -> "Claude Opus 4.8")
                    display_name = model.split("/")[-1].replace("-", " ").title()
                    st.markdown(f'<div class="model-name">{display_name}</div>', unsafe_allow_html=True)
                    
                    # Answer text (rendered as markdown for beautiful formatting)
                    st.markdown(f'<div class="answer-box">', unsafe_allow_html=True)
                    st.markdown(result["answer"])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Metrics
                    st.markdown(f"""
                        <div class="metrics-row">
                            <div class="metric">
                                <div class="metric-val">{result['latency']:.2f}s</div>
                                <div class="metric-lbl">Latency</div>
                            </div>
                            <div class="metric">
                                <div class="metric-val">${result['cost']:.5f}</div>
                                <div class="metric-lbl">Est. Cost</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    # FR-6: Handle each model's errors independently
                    # If one model fails, it shows a red error card, but the others still render!
                    st.markdown(f'<div class="model-card model-card-error">', unsafe_allow_html=True)
                    display_name = model.split("/")[-1].replace("-", " ").title()
                    st.markdown(f'<div class="model-name" style="border-color: #e03131; color: #e03131;">{display_name}</div>', unsafe_allow_html=True)
                    st.error(f"**Model Failed:** {str(e)}")
                    st.markdown('</div>', unsafe_allow_html=True)