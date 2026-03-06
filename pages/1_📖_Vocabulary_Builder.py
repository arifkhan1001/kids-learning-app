import streamlit as st
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Vocabulary Builder", page_icon="📖", layout="centered")

# ── Modern CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: linear-gradient(160deg, #7c3aed 0%, #6366f1 25%, #3b82f6 50%, #06b6d4 75%, #14b8a6 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stApp, .stApp p, .stApp span, .stApp div,
    .stApp label, .stApp li, .stApp ol, .stApp ul,
    .stMarkdown, .stMarkdown p {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar */
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

    /* Hide top bar */
    header[data-testid="stHeader"] { background: transparent !important; }

    /* Narrow sidebar */
    section[data-testid="stSidebar"] { width: 180px !important; min-width: 180px !important; }
    section[data-testid="stSidebar"] > div { width: 180px !important; }

    /* Push content to top */
    .block-container { padding-top: 1rem !important; }

    /* Header */
    .page-header {
        text-align: center; padding: 1.5rem 0 0.5rem 0;
    }
    .page-header h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important; font-size: 2rem !important;
        color: #ffffff !important; margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 1rem; color: rgba(255,255,255,0.85) !important;
        font-weight: 400; margin-bottom: 1.5rem;
    }

    /* Input */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 12px 18px !important;
        background-color: #ffffff !important;
        color: #2d3748 !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #5a67d8 !important;
        box-shadow: 0 0 0 3px rgba(90,103,216,0.1) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #a0aec0 !important; }
    .stTextInput label {
        font-size: 0.95rem !important; font-weight: 600;
        color: rgba(255,255,255,0.9) !important; font-family: 'Inter', sans-serif !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(124,58,237,0.4);
        background: linear-gradient(135deg, #6d28d9, #4f46e5) !important;
    }

    /* Result card */
    .result-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        padding: 28px 32px;
        font-size: 1rem;
        line-height: 1.8;
        color: #2d3748 !important;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        margin-top: 1.5rem;
    }

    /* Success banner */
    .success-bar {
        background: #f0fff4;
        border: 1px solid #c6f6d5;
        border-radius: 12px;
        padding: 12px 20px;
        color: #276749 !important;
        font-weight: 500;
        font-size: 0.95rem;
        margin-top: 1rem;
        text-align: center;
    }

    /* Encouragement */
    .encourage-text {
        text-align: center;
        color: #718096 !important;
        font-size: 0.92rem;
        padding: 1rem 0;
    }

    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }
    .stSpinner > div { font-size: 1rem !important; color: #5a67d8 !important; }
    .stAlert p { color: #2d3748 !important; font-size: 0.95rem !important; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Inject JS to fix text colors inside cards (overrides Streamlit's global white)
components.html("""
<script>
(function() {
    var d = window.parent.document;
    if (!d.getElementById('vocab-style-fix')) {
        var s = d.createElement('style');
        s.id = 'vocab-style-fix';
        s.textContent = `
            .stApp .result-card,
            .stApp .result-card *,
            .stApp .result-card p,
            .stApp .result-card strong,
            .stApp .result-card em,
            .stApp .result-card li,
            .stApp .result-card ul,
            .stApp .result-card ol,
            .stApp .result-card span,
            .stApp .result-card h1,
            .stApp .result-card h2,
            .stApp .result-card h3,
            .stApp .result-card h4 {
                color: #2d3748 !important;
            }
            .stApp .result-card strong {
                color: #1a202c !important;
            }
            .stApp .success-bar,
            .stApp .success-bar * {
                color: #276749 !important;
            }
            .stApp .encourage-text,
            .stApp .encourage-text * {
                color: #1a202c !important;
            }
        `;
        d.head.appendChild(s);
    }
})();
</script>
""", height=0)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>Vocabulary Builder</h1>
    <p class="page-subtitle">Explore any word and discover its meaning, synonyms, and usage</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── LLM ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.8)

llm = get_llm()

template = """
You are a friendly and encouraging teacher for 6 to 8-year-old children.
A child wants to learn about the word: {word}

Please provide clearly and simply:
1. Definition — A very simple definition that a young child can easily understand.
2. Synonyms — Two easy-to-understand synonyms (words that mean the same thing), with a brief explanation of each.
3. Example — A short, engaging example sentence using the word.
4. Fun Fact — One fun fact or a mini challenge to help remember the word.

Rules:
- Keep every sentence short and clear
- Sound like a kind, encouraging friend
- Do NOT use complex vocabulary or advanced grammar
- Use simple formatting with bold headings
"""
prompt = PromptTemplate.from_template(template)

# ── Input ────────────────────────────────────────────────────────────────────
word_input = st.text_input(
    "Which word would you like to explore?",
    placeholder="Try: happy, enormous, brave, sparkle..."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    learn_button = st.button("Explore this word")

if learn_button:
    if word_input.strip():
        with st.spinner("Looking up this word..."):
            try:
                formatted_prompt = prompt.format(word=word_input.strip())
                response = llm.invoke(formatted_prompt)
                st.markdown('<div class="success-bar">Great choice! Here\'s what we found.</div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div class="result-card">{response.content}</div>',
                            unsafe_allow_html=True)
                st.markdown("---")
                st.markdown(
                    '<p class="encourage-text">Well done exploring a new word today. Come back tomorrow for another!</p>',
                    unsafe_allow_html=True)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    st.warning("The service is briefly paused due to high usage. Please wait about a minute and try again.")
                else:
                    st.error(f"Something went wrong. Please try again. (Error: {e})")
    else:
        st.warning("Please type a word in the field above to get started.")
