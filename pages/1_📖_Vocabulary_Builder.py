import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Vocabulary Builder", page_icon="📖")

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #e0f7fa 0%, #ede7f6 55%, #fff9c4 100%);
        }
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
        .stApp, .stApp p, .stApp span, .stApp div,
        .stApp label, .stApp li, .stApp ol, .stApp ul,
        .stMarkdown, .stMarkdown p { color: #1a1a2e !important; }
        h1 {
            font-size: 2.8rem !important; text-align: center; color: #6a0dad !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important;
            text-shadow: 2px 3px 0px #d1c4e9;
        }
        h2, h3, h4 { color: #4527a0 !important; font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important; }
        .subtitle { text-align: center; font-size: 1.25rem; color: #4527a0 !important;
                    font-family: 'Comic Sans MS', 'Chalkboard SE', cursive; margin-bottom: 1.5rem; }
        .stTextInput > div > div > input {
            border-radius: 20px !important; border: 3px solid #7c4dff !important;
            font-size: 1.2rem !important; padding: 10px 18px !important;
            background-color: #ffffff !important; color: #1a1a2e !important;
        }
        .stTextInput > div > div > input::placeholder { color: #9e9e9e !important; }
        .stTextInput label { font-size: 1.1rem !important; font-weight: bold; color: #4527a0 !important; }
        .stButton > button {
            background: linear-gradient(90deg, #ffca28, #ff7043) !important;
            color: #1a1a2e !important; font-size: 1.3rem !important; font-weight: bold !important;
            font-family: 'Comic Sans MS', cursive !important; border: none !important;
            border-radius: 30px !important; padding: 10px 40px !important;
            box-shadow: 0 4px 14px rgba(255,112,67,0.35); transition: transform 0.15s ease;
        }
        .stButton > button:hover { transform: scale(1.07); }
        .result-box {
            background: #fffde7; border-radius: 22px; border: 3px solid #7c4dff;
            padding: 22px 30px; font-size: 1.15rem; line-height: 1.85; color: #1a1a2e !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive;
            box-shadow: 0 4px 18px rgba(124,77,255,0.18); margin-top: 1rem;
        }
        hr { border: none; border-top: 2px dashed #b39ddb; margin: 1.5rem 0; }
        .stSpinner > div { font-size: 1.1rem !important; color: #6a0dad !important; }
        .stAlert p { color: #1a1a2e !important; font-size: 1rem !important; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 Kids Word Adventure! 🌟")
st.markdown('<p class="subtitle">Learn new words every day — it\'s super fun! 🎉</p>', unsafe_allow_html=True)
st.markdown("### 👋 Hi there, Word Explorer!")
st.markdown("Type any word below and I'll explain it just for **YOU**! 🦄")

@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8)

llm = get_llm()

template = """
You are a super fun, friendly, and encouraging teacher for 6 to 7-year-old kids.
A child wants to learn about the word: {word}

Please provide in a very cheerful and simple way:
1. 🔤 A super simple definition that a 6-year-old can easily understand (no hard words!).
2. 🔁 Two easy-to-understand synonyms (words that mean the same thing), with a tiny explanation of each.
3. ✏️ A short, fun example sentence using the word that kids will enjoy.
4. 🌟 One fun fact or a mini challenge to help the child remember the word!

Rules:
- Use LOTS of emojis to make it exciting!
- Keep every sentence short and easy.
- Sound like an enthusiastic, kind friend, not a boring textbook.
- Do NOT use any complex vocabulary or advanced grammar.
"""
prompt = PromptTemplate.from_template(template)

st.markdown("---")
word_input = st.text_input(
    "🔍 Which word do you want to explore today?",
    placeholder="Try: happy, enormous, brave, sparkle..."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    learn_button = st.button("🚀 Let's Learn It!")

if learn_button:
    if word_input.strip():
        with st.spinner("🤔 Hmm, let me think about that... ✨"):
            try:
                formatted_prompt = prompt.format(word=word_input.strip())
                response = llm.invoke(formatted_prompt)
                st.balloons()
                st.markdown("### 🎉 Woohoo! Here's what I found!")
                st.markdown(f'<div class="result-box">{response.content}</div>', unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("💪 **Great job exploring a new word today!** Come back tomorrow for another adventure! 🌈")
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    st.error("😴 **Yawn!** My brain is taking a quick 1-minute nap because I answered too many questions!\n\nTake a deep breath, stretch your arms, and try asking me again in a minute! 🌈")
                else:
                    st.error(f"😬 Uh oh! Something went a little wrong. Let's try again! (Error: {e})")
    else:
        st.warning("🙈 Oops! You forgot to type a word! Try typing something in the box above. 😄")
