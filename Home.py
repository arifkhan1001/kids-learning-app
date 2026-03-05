import streamlit as st

st.set_page_config(page_title="Kids Learning Hub", page_icon="🌈", layout="centered")

st.markdown("""
    <style>
        /* ── Background ── */
        .stApp {
            background: linear-gradient(135deg, #e0f7fa 0%, #ede7f6 55%, #fff9c4 100%);
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ede7f6 0%, #e8eaf6 100%) !important;
            border-right: 2px solid #b39ddb;
        }
        section[data-testid="stSidebar"] * {
            color: #1a1a2e !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important;
        }
        section[data-testid="stSidebar"] a { color: #6a0dad !important; font-weight: bold; }
        section[data-testid="stSidebar"] a:hover { color: #4527a0 !important; }

        /* ── Fix #1: Hide the collapse toggle button (removes tooltip) ── */
        button[data-testid="collapsedControl"] { display: none !important; }

        /* ── Global text ── */
        .stApp, .stApp p, .stApp span, .stApp div,
        .stApp label, .stApp li, .stMarkdown p { color: #1a1a2e !important; }
        h1 {
            font-size: 3rem !important; text-align: center; color: #6a0dad !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important;
            text-shadow: 2px 3px 0px #d1c4e9;
        }
        h2, h3 { color: #4527a0 !important; font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important; }
        .hero-sub {
            text-align: center; font-size: 1.2rem; color: #4527a0 !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive; margin-bottom: 2rem;
        }

        /* ── Fix #2: Big card-style buttons (the WHOLE card is clickable) ── */
        .stButton > button {
            background: #ffffff !important;
            color: #1a1a2e !important;
            font-size: 1.15rem !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important;
            font-weight: bold !important;
            border: 3px solid #b39ddb !important;
            border-radius: 24px !important;
            padding: 28px 20px !important;
            min-height: 220px !important;
            width: 100%;
            white-space: pre-wrap !important;
            line-height: 1.7 !important;
            text-align: center !important;
            box-shadow: 0 6px 24px rgba(106,13,173,0.12);
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.15s ease;
        }
        .stButton > button:hover {
            background: #f3e5f5 !important;
            border-color: #7c4dff !important;
            transform: translateY(-4px);
            box-shadow: 0 10px 30px rgba(106,13,173,0.22);
        }

        hr { border: none; border-top: 2px dashed #b39ddb; margin: 1.5rem 0; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.title("🌈 Kids Learning Hub 🌈")
st.markdown('<p class="hero-sub">Choose your adventure and start learning today! 🚀</p>',
            unsafe_allow_html=True)
st.markdown("---")

# ── Fix #2: Full card-size buttons — the entire tile is clickable ─────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button(
        "📖\n\nVocabulary Builder\n\nType any word and get a fun, simple explanation, synonyms & an example sentence! 🦄",
        use_container_width=True,
        key="nav_vocab",
    ):
        st.switch_page("pages/1_📖_Vocabulary_Builder.py")

with col2:
    if st.button(
        "🧩\n\nSynonym Quiz\n\n10 fun synonym questions! Pick the right answer, earn points, and become a Word Champion! 🏆",
        use_container_width=True,
        key="nav_quiz",
    ):
        st.switch_page("pages/2_🧩_Synonym_Quiz.py")

st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#9575cd;font-family:\'Comic Sans MS\',cursive;font-size:0.9rem;">'
    'Made with ❤️ for young word explorers everywhere!</p>',
    unsafe_allow_html=True,
)
