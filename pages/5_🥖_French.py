import streamlit as st
import streamlit.components.v1 as components
from utils.french_words import get_french_categories, get_french_words_by_category
import io
from gtts import gTTS
import base64

st.set_page_config(page_title="French Language", page_icon="🥖", layout="centered")

# ── Modern CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* ── Base ── */
    .stApp {
        background: linear-gradient(160deg, #7c3aed 0%, #6366f1 25%, #3b82f6 50%, #06b6d4 75%, #14b8a6 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stApp, .stApp p, .stApp span, .stApp div,
    .stApp label, .stApp li, .stMarkdown p {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9fe 0%, #e0f2fe 50%, #ccfbf1 100%) !important;
        border-right: none;
    }
    section[data-testid="stSidebar"] * {
        color: #4a5568 !important;
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] a { color: #6d28d9 !important; font-weight: 600; }
    section[data-testid="stSidebar"] a:hover { color: #4c1d95 !important; }
    button[data-testid="collapsedControl"] { display: none !important; }

    /* ── Hide top bar ── */
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Narrow sidebar ── */
    section[data-testid="stSidebar"] { width: 180px !important; min-width: 180px !important; }
    section[data-testid="stSidebar"] > div { width: 180px !important; }

    /* ── Push content to top ── */
    .block-container { padding-top: 1rem !important; }

    /* ── Page Header ── */
    .page-header {
        text-align: center; padding: 0.2rem 0 0.3rem 0;
    }
    .page-header h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important; font-size: 2rem !important;
        color: #ffffff !important; letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-size: 1rem; color: rgba(255,255,255,0.85) !important;
        font-weight: 400; margin-bottom: 1rem;
    }

    /* ── Flashcard ── */
    .flashcard {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 40px 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin: 1.5rem auto;
        position: relative;
    }
    .emoji-circle {
        font-size: 4rem;
        background: rgba(139,92,246,0.1);
        width: 120px;
        height: 120px;
        line-height: 120px;
        border-radius: 50%;
        margin: 0 auto 1.5rem auto;
        display: flex; align-items: center; justify-content: center;
    }
    .word-fr {
        font-size: 2.2rem;
        font-weight: 700;
        color: #5a67d8 !important;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    .word-en {
        font-size: 1.2rem;
        color: #718096 !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Primary action buttons ── */
    .nav-btn .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: 100%;
    }
    .nav-btn .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
        background: linear-gradient(135deg, #6d28d9, #4f46e5) !important;
    }
    .nav-btn .stButton > button p {
        color: #ffffff !important;
    }
    
    .play-btn {
        margin-top: 2rem;
        display: flex; justify-content: center;
    }
    .play-btn button {
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white; border: none; padding: 12px 32px;
        border-radius: 999px; font-size: 1.1rem; font-weight: 600;
        cursor: pointer; display: flex; align-items: center; gap: 8px;
        box-shadow: 0 4px 16px rgba(124,58,237,0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .play-btn button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox label {
        color: rgba(255,255,255,0.9) !important; font-weight: 600;
    }
    .stSelectbox > div > div {
        border-radius: 12px !important;
    }

    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Inject CSS override for white card text
components.html("""
<script>
(function() {
    var d = window.parent.document;
    if (!d.getElementById('french-style-fix')) {
        var s = d.createElement('style');
        s.id = 'french-style-fix';
        s.textContent = `
            .stApp .flashcard, .stApp .flashcard * { color: inherit !important; }
            .stApp .flashcard { color: #1a202c !important; }
            .stApp .word-fr { color: #5a67d8 !important; }
            .stApp .word-en { color: #718096 !important; }
            .stApp .nav-btn button p { color: #4a5568 !important; }
        `;
        d.head.appendChild(s);
    }
})();
</script>
""", height=0)


# ══════════════════════════════════════════════════════════════════════════════
# STATE & DATA
# ══════════════════════════════════════════════════════════════════════════════
cats = ["All"] + get_french_categories()

if "fr_category" not in st.session_state:
    st.session_state.fr_category = "All"
if "fr_idx" not in st.session_state:
    st.session_state.fr_idx = 0

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <h1>Learn French</h1>
    <p class="page-subtitle">Learn basic words and how to say them</p>
</div>
""", unsafe_allow_html=True)


colA, colB, colC = st.columns([1,2,1])
with colB:
    # Handle category change explicitly to reset index
    selected_cat = st.selectbox("Choose a category:", cats, index=cats.index(st.session_state.fr_category))
    if selected_cat != st.session_state.fr_category:
        st.session_state.fr_category = selected_cat
        st.session_state.fr_idx = 0
        st.rerun()

words = get_french_words_by_category(st.session_state.fr_category)
total_words = len(words)
idx = st.session_state.fr_idx
current_word = words[idx]

# ══════════════════════════════════════════════════════════════════════════════
# FLASHCARD
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="flashcard">
    <div class="emoji-circle">{current_word['emoji']}</div>
    <div class="word-fr">{current_word['fr']}</div>
    <div class="word-en">{current_word['en']}</div>
</div>
""", unsafe_allow_html=True)

# Audio button via isolated component iframe using gTTS
def get_audio_html(text):
    tts = gTTS(text=text, lang="fr")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    return f'''
    <style>
        .audio-container {{
            background: linear-gradient(135deg, #7c3aed, #6366f1);
            border-radius: 999px; padding: 6px 16px; margin: 0 auto;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(124,58,237,0.3);
            width: fit-content; margin-top: 1rem;
        }}
        .audio-container span {{ color: white; font-weight: 600; font-family: 'Inter', sans-serif; margin-right: 12px; font-size: 1.1rem; }}
        audio {{ height: 36px; border-radius: 20px; outline: none; }}
    </style>
    <div class="audio-container">
        <span>▶️ Hear it:</span>
        <audio controls src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>
    </div>
    '''

st.markdown(get_audio_html(current_word['fr']), unsafe_allow_html=True)

# ── Navigation Buttons ──
nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Previous", disabled=(idx == 0), use_container_width=True):
        st.session_state.fr_idx -= 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with nav2:
    st.markdown(f"<div style='text-align:center; padding-top: 14px; color: rgba(255,255,255,0.8); font-size: 0.9rem;'>Word {idx + 1} of {total_words}</div>", unsafe_allow_html=True)
with nav3:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("Next ➡️", disabled=(idx == total_words - 1), use_container_width=True):
        st.session_state.fr_idx += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
