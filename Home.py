import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Learning Hub", page_icon="📚", layout="centered")

# ── Helper: encode icon for clickable HTML ───────────────────────────────────
def img_b64(name: str) -> str:
    return base64.b64encode(Path(f"assets/{name}").read_bytes()).decode()

icons = {
    "vocab":     img_b64("icon_vocabulary.png"),
    "quiz":      img_b64("icon_synonym_quiz.png"),
    "maths":     img_b64("icon_maths.png"),
    "reasoning": img_b64("icon_reasoning.png"),
    "french":    img_b64("icon_french.png"),
}

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: linear-gradient(160deg, #7c3aed 0%, #6366f1 25%, #3b82f6 50%, #06b6d4 75%, #14b8a6 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stApp, .stApp p, .stApp span, .stApp div,
    .stApp label, .stApp li, .stMarkdown p {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Soothing gradient sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9fe 0%, #e0f2fe 50%, #ccfbf1 100%) !important;
        border-right: none;
    }
    section[data-testid="stSidebar"] * {
        color: #4a5568 !important;
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] a {
        color: #6d28d9 !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] a:hover { color: #4c1d95 !important; }
    button[data-testid="collapsedControl"] { display: none !important; }

    /* ── Hide top bar ── */
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Narrow sidebar ── */
    section[data-testid="stSidebar"] { width: 180px !important; min-width: 180px !important; }
    section[data-testid="stSidebar"] > div { width: 180px !important; }

    /* ── Fix header top cut-off ── */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* ── Header ── */
    .app-header {
        text-align: center;
        padding: 0.5rem 0 0.2rem 0;
    }
    .app-header h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.6rem !important;
        color: #ffffff !important;
        margin-bottom: 0.1rem;
        letter-spacing: -0.02em;
    }
    .app-subtitle {
        font-size: 0.88rem;
        color: rgba(255,255,255,0.85) !important;
        font-weight: 400;
        margin-bottom: 0.3rem;
    }

    hr { border: none; border-top: 1px solid rgba(255,255,255,0.18); margin: 0.4rem 0; }

    /* ── Clickable card grid ── */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        padding: 0.3rem 0;
    }
    .card-grid.row2 {
        grid-template-columns: repeat(3, 1fr);
    }
    .card-link {
        text-decoration: none !important;
        display: block;
    }
    .exercise-card {
        background: rgba(255,255,255,0.93);
        border-radius: 18px;
        padding: 12px 8px 10px 8px;
        text-align: center;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .exercise-card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 12px 40px rgba(0,0,0,0.18);
    }
    .card-icon-img {
        width: 100%;
        max-width: 130px;
        height: auto;
        margin-bottom: 6px;
    }
    .card-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        color: #1e293b;
        margin-bottom: 3px;
    }
    .card-badge {
        display: inline-block;
        font-size: 0.58rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
        margin-top: 2px;
    }
    .badge-live { background: linear-gradient(135deg,#d1fae5,#a7f3d0); color: #065f46; }
    .badge-soon { background: linear-gradient(135deg,#e0e7ff,#c7d2fe); color: #4338ca; }

    /* ── Hide ALL buttons on the home page ── */
    .stButton {
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .stButton > button {
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
        overflow: hidden !important;
        font-size: 0 !important;
        color: transparent !important;
    }

    .footer-text {
        text-align: center;
        color: rgba(255,255,255,0.55) !important;
        font-size: 0.72rem;
        padding: 0.2rem 0;
    }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>Learning Hub</h1>
    <p class="app-subtitle">Choose an exercise and start learning today</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ── Card data ────────────────────────────────────────────────────────────────
cards = [
    {"key": "vocab",     "icon": icons["vocab"],     "title": "Vocabulary Builder", "badge": "Available",   "cls": "badge-live",  "page": "pages/1_📖_Vocabulary_Builder.py"},
    {"key": "quiz",      "icon": icons["quiz"],      "title": "Synonym Quiz",       "badge": "Available",   "cls": "badge-live",  "page": "pages/2_🧩_Synonym_Quiz.py"},
    {"key": "maths",     "icon": icons["maths"],     "title": "Maths Practice",     "badge": "Available",   "cls": "badge-live",  "page": "pages/3_Maths.py"},
    {"key": "reasoning", "icon": icons["reasoning"], "title": "Reasoning",          "badge": "Available",   "cls": "badge-live",  "page": "pages/4_Reasoning.py"},
    {"key": "french",    "icon": icons["french"],    "title": "French Language",    "badge": "Available",   "cls": "badge-live",  "page": "pages/5_French.py"},
]

def card_html(c: dict) -> str:
    return (
        f'<div class="exercise-card">'
        f'<img class="card-icon-img" src="data:image/png;base64,{c["icon"]}" alt="{c["title"]}">'
        f'<div class="card-title">{c["title"]}</div>'
        f'<span class="card-badge {c["cls"]}">{c["badge"]}</span>'
        f'</div>'
    )


# ── Row 1 — 3 cards (clickable icons, no button) ────────────────────────────
st.markdown(
    '<div class="card-grid">'
    + card_html(cards[0]) + card_html(cards[1]) + card_html(cards[2])
    + '</div>',
    unsafe_allow_html=True,
)

# Hidden Streamlit buttons for actual page navigation
r1a, r1b, r1c = st.columns(3)
with r1a:
    if st.button("a", key="nav_vocab"):
        st.switch_page(cards[0]["page"])
with r1b:
    if st.button("b", key="nav_quiz"):
        st.switch_page(cards[1]["page"])
with r1c:
    if st.button("c", key="nav_maths"):
        st.switch_page(cards[2]["page"])


# ── Row 2 — 2 cards ─────────────────────────────────────────────────────────
st.markdown(
    '<div class="card-grid row2">'
    + card_html(cards[3]) + card_html(cards[4])
    + '</div>',
    unsafe_allow_html=True,
)

r2a, r2b, _ = st.columns(3)
with r2a:
    if st.button("d", key="nav_reasoning"):
        st.switch_page(cards[3]["page"])
with r2b:
    if st.button("e", key="nav_french"):
        st.switch_page(cards[4]["page"])


# ── JavaScript: make HTML cards click the hidden buttons ─────────────────────
import streamlit.components.v1 as components
components.html("""
<script>
(function() {
    var pd = window.parent.document;

    // Map card index (in DOM order) to button key label
    var cardMap = [
        {row: 0, idx: 0, label: 'a'},
        {row: 0, idx: 1, label: 'b'},
        {row: 0, idx: 2, label: 'c'},
        {row: 1, idx: 0, label: 'd'},
        {row: 1, idx: 1, label: 'e'},
    ];

    function wireUp() {
        var allCards = pd.querySelectorAll('.exercise-card');
        var allBtns  = pd.querySelectorAll('button[kind="secondary"]');
        if (allCards.length < 5 || allBtns.length < 5) {
            setTimeout(wireUp, 400);
            return;
        }
        for (var i = 0; i < allCards.length && i < allBtns.length; i++) {
            (function(card, btn) {
                card.style.cursor = 'pointer';
                card.addEventListener('click', function() { btn.click(); });
            })(allCards[i], allBtns[i]);
        }
    }
    setTimeout(wireUp, 600);
})();
</script>
""", height=0)


# ── API Usage Tracker ──────────────────────────────────────────────────────────
from utils.usage import get_usage, get_remaining, DAILY_LIMIT
usage_data = get_usage()
remaining = get_remaining()
used = usage_data["used"]
pct = min(100, int((used / DAILY_LIMIT) * 100))

st.markdown("---")

st.markdown(f"""
<style>
.usage-container {{
    display: flex; justify-content: center; margin: 1rem 0;
}}
.usage-card {{
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    padding: 12px 24px;
    display: flex; align-items: center; gap: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    color: white; font-family: 'Inter', sans-serif;
}}
.usage-item {{
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}}
.usage-label {{ font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9; }}
.usage-val {{ font-size: 1.25rem; font-weight: 800; }}
.usage-divider {{ width: 1px; height: 30px; background: rgba(255,255,255,0.3); }}
</style>
<div class="usage-container">
    <div class="usage-card">
        <div class="usage-item">
            <span class="usage-label">Daily Limit</span>
            <span class="usage-val">{DAILY_LIMIT}</span>
        </div>
        <div class="usage-divider"></div>
        <div class="usage-item">
            <span class="usage-label">Used</span>
            <span class="usage-val" style="color: {'#fca5a5' if pct > 90 else '#ffffff'};">{used}</span>
        </div>
        <div class="usage-divider"></div>
        <div class="usage-item">
            <span class="usage-label">Remaining</span>
            <span class="usage-val" style="color: {'#86efac' if remaining > 0 else '#fca5a5'};">{remaining}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="footer-text">Learning Hub — Built for curious young minds</p>', unsafe_allow_html=True)
