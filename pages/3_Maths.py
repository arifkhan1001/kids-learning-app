import streamlit as st

st.set_page_config(page_title="Maths Practice", page_icon="📐", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: linear-gradient(160deg, #7c3aed 0%, #6366f1 25%, #3b82f6 50%, #06b6d4 75%, #14b8a6 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stApp, .stApp p, .stApp span, .stApp div, .stMarkdown p {
        color: #ffffff !important; font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9fe 0%, #e0f2fe 50%, #ccfbf1 100%) !important;
        border-right: none;
    }
    section[data-testid="stSidebar"] * { color: #4a5568 !important; font-family: 'Inter', sans-serif !important; }
    section[data-testid="stSidebar"] a { color: #6d28d9 !important; font-weight: 600; }
    section[data-testid="stSidebar"] a:hover { color: #4c1d95 !important; }
    button[data-testid="collapsedControl"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* Narrow sidebar */
    section[data-testid="stSidebar"] { width: 180px !important; min-width: 180px !important; }
    section[data-testid="stSidebar"] > div { width: 180px !important; }

    /* Push content to top */
    .block-container { padding-top: 1rem !important; }

    .page-header { text-align: center; padding: 0.5rem 0 0.5rem 0; }
    .page-header h1 {
        font-family: 'Inter', sans-serif !important; font-weight: 700 !important;
        font-size: 2rem !important; color: #ffffff !important; letter-spacing: -0.02em;
    }
    .page-subtitle { font-size: 1rem; color: rgba(255,255,255,0.85) !important; font-weight: 400; margin-bottom: 2rem; }
    .coming-soon-card {
        background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
        padding: 48px 32px; text-align: center; max-width: 460px; margin: 2rem auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1); backdrop-filter: blur(12px);
    }
    .cs-icon {
        width: 64px; height: 64px; background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 20px auto; font-size: 1.8rem; color: #ffffff;
        box-shadow: 0 4px 12px rgba(245,158,11,0.3);
    }
    .cs-title { font-size: 1.3rem; font-weight: 600; color: #ffffff; margin-bottom: 8px; }
    .cs-desc { font-size: 0.95rem; color: rgba(255,255,255,0.85); line-height: 1.6; }
    .cs-badge {
        display: inline-block; font-size: 0.75rem; font-weight: 600;
        padding: 4px 14px; border-radius: 20px; margin-top: 16px;
        background: rgba(255,255,255,0.2); color: #ffffff;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>📐 Maths Practice</h1>
    <p class="page-subtitle">Build number skills with interactive exercises</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="coming-soon-card">
    <div class="cs-icon">
        <svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
    </div>
    <div class="cs-title">Coming Soon</div>
    <div class="cs-desc">
        Practice addition, subtraction, multiplication, and problem solving with
        interactive exercises designed for young learners.
    </div>
    <span class="cs-badge">In Development</span>
</div>
""", unsafe_allow_html=True)
