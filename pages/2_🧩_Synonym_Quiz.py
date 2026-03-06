import streamlit as st
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
import random

load_dotenv()

st.set_page_config(page_title="Synonym Quiz", page_icon="📝", layout="centered")

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
    .section-label {
        font-size: 0.95rem; font-weight: 600; color: rgba(255,255,255,0.9) !important;
        font-family: 'Inter', sans-serif; margin-bottom: 0.5rem;
    }

    /* ── Answer Tiles ── */
    .stButton > button {
        background: rgba(255,255,255,0.9) !important;
        color: #2d3748 !important;
        font-size: 1.05rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border: 1.5px solid rgba(139,92,246,0.15) !important;
        border-radius: 14px !important;
        padding: 18px 16px !important;
        min-height: 70px !important;
        width: 100%;
        text-align: center !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        box-shadow: 0 2px 8px rgba(139,92,246,0.06);
        margin-bottom: 8px;
    }
    .stButton > button:hover {
        border-color: #8b5cf6 !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(139,92,246,0.15);
        background: rgba(255,255,255,1) !important;
    }

    /* ── Level Cards ── */
    .level-card {
        background: #ffffff;
        border-radius: 14px;
        border: 1.5px solid #e2e8f0;
        padding: 20px 16px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        min-height: 110px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    .level-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.07);
    }
    .level-card.easy {
        border-left: 4px solid #48bb78;
    }
    .level-card.medium {
        border-left: 4px solid #ecc94b;
    }
    .level-card.hard {
        border-left: 4px solid #fc8181;
    }
    .level-name { font-weight: 600; font-size: 1.1rem; color: #1a202c; }
    .level-desc { font-size: 0.82rem; color: #a0aec0; margin-top: 4px; }

    /* ── Level buttons — base override for colored buttons ── */
    .level-btn-easy .stButton > button,
    button[kind="secondary"] { transition: transform 0.2s ease, box-shadow 0.2s ease; }

    /* ── Primary action buttons ── */
    .action-btn > div > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .action-btn > div > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(124,58,237,0.4);
        background: linear-gradient(135deg, #6d28d9, #4f46e5) !important;
    }

    /* ── Restart btn ── */
    .restart-btn > div > button {
        background: rgba(255,255,255,0.9) !important;
        color: #4a5568 !important;
        border: 1.5px solid rgba(255,255,255,0.5) !important;
        border-radius: 10px !important;
        padding: 6px 16px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        min-height: 36px !important;
        box-shadow: none !important;
    }
    .restart-btn > div > button:hover {
        border-color: #cbd5e0 !important;
        background: #ffffff !important;
    }

    /* ── Input ── */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 12px 18px !important;
        background-color: #ffffff !important;
        color: #2d3748 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #5a67d8 !important;
        box-shadow: 0 0 0 3px rgba(90,103,216,0.1) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #a0aec0 !important; }

    /* ── Score banner ── */
    .score-banner {
        background: linear-gradient(135deg, #7c3aed, #3b82f6, #06b6d4);
        border: none;
        border-radius: 14px;
        padding: 14px 24px;
        text-align: center;
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(124,58,237,0.2);
        margin-bottom: 1rem;
    }
    .score-banner strong { color: #ffffff; }

    /* ── Question card ── */
    .question-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 28px 32px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a202c !important;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
    }
    .question-card u { text-decoration-color: #5a67d8; text-underline-offset: 4px; }

    /* ── Feedback ── */
    .feedback-correct {
        background: #f0fff4;
        border: 1px solid #c6f6d5;
        border-radius: 14px;
        padding: 18px 24px;
        color: #276749 !important;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        margin-top: 1rem;
    }
    .feedback-wrong {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        border-radius: 14px;
        padding: 18px 24px;
        color: #9b2c2c !important;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        margin-top: 1rem;
    }

    /* ── End screen ── */
    .end-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 40px 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin: 1rem auto;
        max-width: 480px;
    }
    .end-headline {
        font-size: 1.6rem; font-weight: 700; color: #1a202c;
        margin-bottom: 8px;
    }
    .end-score {
        font-size: 2.5rem; font-weight: 700; color: #5a67d8;
        margin: 12px 0;
    }
    .end-msg {
        font-size: 1rem; color: #718096; font-weight: 400;
        margin-top: 8px;
    }
    .level-badge {
        display: inline-block; font-size: 0.8rem; font-weight: 600;
        padding: 4px 14px; border-radius: 20px;
    }
    .badge-easy   { background: #c6f6d5; color: #276749; }
    .badge-medium { background: #fefcbf; color: #975a16; }
    .badge-hard   { background: #fed7d7; color: #9b2c2c; }

    /* ── How to play ── */
    .how-to-play {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 28px;
        margin-top: 1rem;
        font-size: 0.92rem;
        line-height: 1.8;
        color: #4a5568 !important;
    }
    .how-to-play, .how-to-play * {
        color: #4a5568 !important;
    }
    .how-to-play ul { padding-left: 18px; }
    .how-to-play li { margin-bottom: 4px; }

    /* ── Progress bar ── */
    .stProgress > div > div > div > div {
        background: #5a67d8 !important;
        border-radius: 999px;
    }

    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
    .stAlert p { color: #2d3748 !important; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── LLM ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.0)

llm = get_llm()

# ── Level config ─────────────────────────────────────────────────────────────
LEVELS = {
    "Easy": {
        "badge_class": "badge-easy",
        "desc": "Simple everyday words",
        "prompt_instruction": (
            "Use very simple, common words that a 6-year-old knows every day "
            "(e.g. happy, big, fast, kind, loud). Words should be 3-5 letters long "
            "and found in basic picture books."
        ),
    },
    "Medium": {
        "badge_class": "badge-medium",
        "desc": "More challenging vocabulary",
        "prompt_instruction": (
            "Use medium-difficulty words for a 6-year-old who is a good reader. "
            "Words must be at least 5 letters long. Examples: brave, shiny, gentle, quiet."
        ),
    },
    "Hard": {
        "badge_class": "badge-hard",
        "desc": "Advanced words for strong readers",
        "prompt_instruction": (
            "Use longer advanced words for a smart 6-7 year old. "
            "Words should be 7+ letters. Examples: enormous, cheerful, frightened, wonderful."
        ),
    },
}


# ── Celebration engine (subtle, professional) ────────────────────────────────
def _inject_js(code: str):
    components.html(f"<script>{code}</script>", height=0)

def celebrate(correct_count: int):
    """Subtle celebration — soft confetti dots falling from top."""
    _inject_js("""
    (function() {
        var d = window.parent.document;
        var colors = ['#5a67d8','#48bb78','#ecc94b','#ed8936','#9f7aea','#fc8181','#4fd1c5'];
        for (var i = 0; i < 40; i++) {
            var dot = d.createElement('div');
            var left = Math.random() * 100;
            var size = 4 + Math.random() * 6;
            var dur = 1200 + Math.random() * 1200;
            var delay = Math.random() * 600;
            var color = colors[Math.floor(Math.random() * colors.length)];
            dot.style.cssText = 'position:fixed;left:'+left+'%;top:-20px;'
                +'width:'+size+'px;height:'+size+'px;border-radius:50%;'
                +'background:'+color+';z-index:99999;pointer-events:none;opacity:0.85;'
                +'transition:top '+dur+'ms ease-in, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(dot);
            setTimeout(function(el){ el.style.top='105vh'; el.style.opacity='0'; }.bind(null,dot), 50+delay);
            setTimeout(function(el){ if(el.parentNode) el.parentNode.removeChild(el); }.bind(null,dot), dur+800);
        }
    })();
    """)


# ── Session state ────────────────────────────────────────────────────────────
def init_quiz_state():
    st.session_state.questions     = []
    st.session_state.current_q     = 0
    st.session_state.score         = 0
    st.session_state.correct_count = 0
    st.session_state.answered      = False
    st.session_state.last_correct  = None
    st.session_state.last_chosen   = None
    st.session_state.quiz_started  = False
    st.session_state.quiz_done     = False
    st.session_state.player_name   = ""

if "quiz_started"   not in st.session_state: init_quiz_state()
if "used_words"     not in st.session_state: st.session_state.used_words = []
if "selected_level" not in st.session_state: st.session_state.selected_level = None
if "correct_count"  not in st.session_state: st.session_state.correct_count = 0


# ── Quiz generation ──────────────────────────────────────────────────────────
def build_prompt(level_key: str, used_words: list) -> str:
    cfg = LEVELS[level_key]
    used_str = ", ".join(used_words[-60:]) if used_words else "none yet"
    return f"""
You are creating a word synonym quiz for 6-8 year old children.
Generate exactly 10 quiz questions. Each question asks for the synonym of a given word.
Difficulty level: {level_key}
Word-selection rules: {cfg['prompt_instruction']}
IMPORTANT — do NOT reuse these already-used words: {used_str}
Return ONLY a valid JSON array with exactly 10 objects, each with:
- "word": the quiz word
- "correct": the correct synonym (one word)
- "options": array of exactly 4 strings — correct + 3 wrong options, random order
- "explanation": short, encouraging 1-2 sentence explanation for a young child
Return ONLY the JSON array, no extra text or markdown.
"""

def generate_quiz(level_key: str, used_words: list) -> list:
    response = llm.invoke(build_prompt(level_key, used_words))
    raw = response.content.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    questions = json.loads(raw.strip())
    for q in questions:
        random.shuffle(q["options"])
    return questions[:10]


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <h1>Synonym Quiz</h1>
    <p class="page-subtitle">Test your vocabulary knowledge</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# START SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.quiz_started:

    # Name input
    st.markdown('<p class="section-label">Your name</p>', unsafe_allow_html=True)
    name_val = st.text_input(
        "name", placeholder="e.g. Zayn, Emma, Leo...",
        label_visibility="collapsed", key="name_field",
    )
    st.session_state.player_name = name_val.strip()

    st.markdown("---")

    # Level selection
    st.markdown('<p class="section-label">Choose a difficulty level</p>', unsafe_allow_html=True)

    lcols = st.columns(3, gap="medium")
    btn_classes = {"Easy": "easy-btn", "Medium": "medium-btn", "Hard": "hard-btn"}
    for lk in LEVELS:
        with lcols[list(LEVELS.keys()).index(lk)]:
            st.markdown(f'<div class="{btn_classes[lk]}">', unsafe_allow_html=True)
            if st.button(lk, key=f"lvl_start_{lk}", use_container_width=True):
                if not st.session_state.player_name:
                    st.warning("Please enter your name first.")
                else:
                    st.session_state.selected_level = lk
                    with st.spinner(f"Generating {lk} quiz..."):
                        try:
                            qs = generate_quiz(lk, st.session_state.used_words)
                            new_words = [q["word"] for q in qs]
                            st.session_state.used_words = (
                                st.session_state.used_words + new_words)[-120:]
                            st.session_state.questions     = qs
                            st.session_state.quiz_started  = True
                            st.session_state.current_q     = 0
                            st.session_state.score         = 0
                            st.session_state.correct_count = 0
                            st.session_state.answered      = False
                            st.session_state.quiz_done     = False
                            st.rerun()
                        except Exception as e:
                            err_str = str(e)
                            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                                st.warning("The service is briefly paused due to high usage. Please wait about a minute and try again.")
                            else:
                                st.error(f"Could not generate the quiz. Please try again. ({e})")
            st.markdown('</div>', unsafe_allow_html=True)

    # Inject JS to color the difficulty buttons + fix restart & how-to-play text
    components.html("""
    <script>
    (function() {
        var d = window.parent.document;

        // Inject a style tag into parent to override Streamlit's white text
        if (!d.getElementById('quiz-style-fix')) {
            var s = d.createElement('style');
            s.id = 'quiz-style-fix';
            s.textContent = `
                .stApp .how-to-play,
                .stApp .how-to-play *,
                .stApp .how-to-play li,
                .stApp .how-to-play ul,
                .stApp .how-to-play p,
                .stApp .how-to-play span,
                .stApp .how-to-play strong {
                    color: #4a5568 !important;
                }
                .stApp .restart-btn button,
                .stApp .restart-btn button p,
                .stApp .restart-btn button span {
                    background: rgba(255,255,255,0.9) !important;
                    color: #4a5568 !important;
                    border: 1px solid rgba(255,255,255,0.5) !important;
                    border-radius: 10px !important;
                    font-size: 0.85rem !important;
                    font-weight: 500 !important;
                }
                .stApp .restart-btn button:hover {
                    background: #ffffff !important;
                }
            `;
            d.head.appendChild(s);
        }

        var colors = {
            'Easy':   {bg: 'linear-gradient(135deg, #10b981, #059669)', shadow: '0 4px 16px rgba(16,185,129,0.35)'},
            'Medium': {bg: 'linear-gradient(135deg, #f59e0b, #d97706)', shadow: '0 4px 16px rgba(245,158,11,0.35)'},
            'Hard':   {bg: 'linear-gradient(135deg, #ef4444, #dc2626)', shadow: '0 4px 16px rgba(239,68,68,0.35)'}
        };
        function applyColors() {
            var btns = d.querySelectorAll('button[kind="secondary"]');
            btns.forEach(function(btn) {
                var txt = btn.textContent.trim();
                if (colors[txt]) {
                    btn.style.cssText = 'background: ' + colors[txt].bg + ' !important; color: #fff !important; border: none !important; font-weight: 700 !important; font-size: 1.1rem !important; box-shadow: ' + colors[txt].shadow + '; border-radius: 14px !important; padding: 18px 16px !important; min-height: 70px !important; width: 100%; transition: transform 0.2s ease, box-shadow 0.2s ease;';
                }
            });
        }
        applyColors();
        setTimeout(applyColors, 300);
        setTimeout(applyColors, 800);
        var obs = new MutationObserver(function() { applyColors(); });
        obs.observe(d.body, {childList: true, subtree: true});
        setTimeout(function() { obs.disconnect(); }, 5000);
    })();
    </script>
    """, height=0)

    # How to play
    st.markdown("---")
    st.markdown('<p class="section-label">How to play</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="how-to-play">
    <ul>
      <li>You will answer <strong>10 questions</strong> about synonyms (words that mean the same thing)</li>
      <li>Select the correct synonym from 4 answer tiles</li>
      <li>Correct answer = <strong>+10 points</strong></li>
      <li>Wrong answer = try again on the same question</li>
      <li>Aim for a perfect score of <strong>100</strong></li>
    </ul>
    <strong>Levels:</strong> &nbsp; Easy &middot; Medium &middot; Hard
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# END SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.quiz_done:
    score     = st.session_state.score
    name      = st.session_state.player_name or "Champion"
    level_key = st.session_state.selected_level or "Easy"
    cfg       = LEVELS[level_key]

    if score == 100:
        headline = f"Perfect score, {name}!"
        msg = "Outstanding performance. You got every single question right."
    elif score >= 70:
        headline = f"Great work, {name}!"
        msg = "Excellent vocabulary skills. Keep practising to reach a perfect score."
    elif score >= 40:
        headline = f"Well done, {name}!"
        msg = "Good effort. With more practice you will improve even further."
    else:
        headline = f"Nice try, {name}!"
        msg = "Practice makes perfect. Try again and you will do better."

    celebrate(0)
    st.markdown(f"""
        <div class="end-card">
            <span class="level-badge {cfg['badge_class']}">{level_key} Level</span>
            <div class="end-headline" style="margin-top:16px;">{headline}</div>
            <div class="end-score">{score} / 100</div>
            <div class="end-msg">{msg}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("Play Again", key="end_play_again"):
            saved = st.session_state.used_words
            init_quiz_state()
            st.session_state.used_words = saved
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
        if st.button("Change Level", key="end_change_level"):
            saved = st.session_state.used_words
            init_quiz_state()
            st.session_state.used_words = saved
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cc:
        st.markdown(
            f'<p style="color:#718096;text-align:center;font-size:0.85rem;'
            f'padding-top:10px;font-family:Inter,sans-serif;">'
            f'{len(st.session_state.used_words)} unique words learned</p>',
            unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# QUIZ IN PROGRESS
# ══════════════════════════════════════════════════════════════════════════════
questions = st.session_state.questions
idx       = st.session_state.current_q
q         = questions[idx]
total_q   = len(questions)
level_key = st.session_state.selected_level or "Easy"
cfg       = LEVELS[level_key]
name      = st.session_state.player_name or "Explorer"

# Score banner
st.markdown(
    f'<div class="score-banner">'
    f'<strong>{level_key}</strong> &nbsp;·&nbsp; '
    f'{name} &nbsp;·&nbsp; '
    f'Score: <strong>{st.session_state.score}</strong> / 100 &nbsp;·&nbsp; '
    f'Question {idx + 1} of {total_q}'
    f'</div>',
    unsafe_allow_html=True)

st.progress(idx / total_q)

# Question
st.markdown(
    f'<div class="question-card">'
    f'What is a synonym for <u>{q["word"].upper()}</u>?'
    f'</div>',
    unsafe_allow_html=True)

# Answer tiles
if not st.session_state.answered:
    cols = st.columns(2)
    for i, option in enumerate(q["options"]):
        with cols[i % 2]:
            if st.button(f"  {option}  ", key=f"opt_{idx}_{i}", use_container_width=True):
                st.session_state.last_chosen = option
                if option.strip().lower() == q["correct"].strip().lower():
                    st.session_state.score        += 10
                    st.session_state.correct_count += 1
                    st.session_state.answered      = True
                    st.session_state.last_correct  = True
                else:
                    st.session_state.last_correct = False
                st.rerun()

# Feedback
if st.session_state.last_correct is not None:

    if st.session_state.last_correct:
        celebrate(st.session_state.correct_count - 1)
        st.markdown(
            f'<div class="feedback-correct">'
            f'<strong>Correct!</strong> Well done, {name}. +10 points<br><br>'
            f'{q["explanation"]}'
            f'</div>',
            unsafe_allow_html=True)
        st.markdown("")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="action-btn">', unsafe_allow_html=True)
            next_label = "Next Question" if idx + 1 < total_q else "See Results"
            if st.button(next_label, key="next_btn"):
                if idx + 1 < total_q:
                    st.session_state.current_q   += 1
                    st.session_state.answered     = False
                    st.session_state.last_correct = None
                    st.session_state.last_chosen  = None
                else:
                    st.session_state.quiz_done = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        chosen = st.session_state.last_chosen
        st.markdown(
            f'<div class="feedback-wrong">'
            f'<strong>Not quite.</strong> "{chosen}" is not the right answer.<br>'
            f'Try again, {name}.'
            f'</div>',
            unsafe_allow_html=True)
        st.markdown("")
        st.session_state.last_correct = None
        st.session_state.last_chosen  = None
        cols = st.columns(2)
        for i, option in enumerate(q["options"]):
            with cols[i % 2]:
                if st.button(f"  {option}  ", key=f"retry_{idx}_{i}", use_container_width=True):
                    st.session_state.last_chosen = option
                    if option.strip().lower() == q["correct"].strip().lower():
                        st.session_state.score        += 10
                        st.session_state.correct_count += 1
                        st.session_state.answered      = True
                        st.session_state.last_correct  = True
                    else:
                        st.session_state.last_correct = False
                    st.rerun()
