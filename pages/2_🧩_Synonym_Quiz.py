import streamlit as st
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
import random

load_dotenv()

st.set_page_config(page_title="Synonym Quiz", page_icon="🧩", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
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

        /* ── Fix #1: Nuke the sidebar collapse toggle completely ── */
        [data-testid="collapsedControl"],
        button[data-testid="collapsedControl"],
        [data-testid="baseButton-headerNoPadding"] {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            pointer-events: none !important;
            position: absolute !important;
            visibility: hidden !important;
        }

        /* ── Global text ── */
        .stApp, .stApp p, .stApp span, .stApp div,
        .stApp label, .stApp li, .stMarkdown p { color: #1a1a2e !important; }
        h1 {
            font-size: 2.6rem !important; text-align: center; color: #6a0dad !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important;
            text-shadow: 2px 3px 0px #d1c4e9; margin-bottom: 0 !important;
        }
        h2, h3, h4 { color: #4527a0 !important; font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important; }

        /* ── Level badge pill ── */
        .level-easy   { background: #c8e6c9; color: #1b5e20 !important; border: 2px solid #43a047; }
        .level-medium { background: #fff9c4; color: #e65100 !important; border: 2px solid #fbc02d; }
        .level-hard   { background: #ffcdd2; color: #b71c1c !important; border: 2px solid #e53935; }
        .level-badge {
            display: inline-block; border-radius: 20px; padding: 5px 20px;
            font-family: 'Comic Sans MS', cursive; font-weight: bold; font-size: 1rem;
            margin-bottom: 0.8rem;
        }

        /* ── Section heading centred ── */
        .section-heading {
            text-align: center; font-size: 1.4rem; font-weight: bold;
            color: #4527a0 !important; font-family: 'Comic Sans MS', cursive;
            margin: 0.5rem 0 1rem 0;
        }

        /* ── Default button style (level cards + answer tiles) ── */
        .stButton > button {
            background: #ffffff !important; color: #1a1a2e !important;
            font-size: 1.2rem !important; font-family: 'Comic Sans MS', cursive !important;
            font-weight: bold !important; border: 3px solid #b39ddb !important;
            border-radius: 22px !important; padding: 18px 10px !important;
            min-height: 90px !important; width: 100%;
            white-space: pre-wrap !important; line-height: 1.6 !important;
            text-align: center !important;
            transition: background 0.15s ease, transform 0.12s ease, border-color 0.15s ease;
            box-shadow: 0 3px 12px rgba(0,0,0,0.1); margin-bottom: 8px;
        }
        .stButton > button:hover {
            border-color: #7c4dff !important; transform: scale(1.04);
        }

        /* ── Fix #4: Level tile colours via column position in 3rd horizontal block ──
           The start screen renders 3 stHorizontalBlocks:
             1st = title + restart button
             2nd = name input columns
             3rd = level cards  ← target this one
           st.stop() means quiz elements never enter the DOM on the start screen.
        ── */
        [data-testid="stHorizontalBlock"]:nth-of-type(3)
            [data-testid="column"]:nth-child(1) .stButton > button {
            background: #c8e6c9 !important;
            border-color: #43a047 !important;
            color: #1b5e20 !important;
            font-size: 1.6rem !important;
            font-weight: 900 !important;
        }
        [data-testid="stHorizontalBlock"]:nth-of-type(3)
            [data-testid="column"]:nth-child(2) .stButton > button {
            background: #fff9c4 !important;
            border-color: #fbc02d !important;
            color: #e65100 !important;
            font-size: 1.6rem !important;
            font-weight: 900 !important;
        }
        [data-testid="stHorizontalBlock"]:nth-of-type(3)
            [data-testid="column"]:nth-child(3) .stButton > button {
            background: #ffcdd2 !important;
            border-color: #e53935 !important;
            color: #b71c1c !important;
            font-size: 1.6rem !important;
            font-weight: 900 !important;
        }
        [data-testid="stHorizontalBlock"]:nth-of-type(3)
            [data-testid="column"]:nth-child(1) .stButton > button:hover {
            background: #a5d6a7 !important; transform: scale(1.06);
        }
        [data-testid="stHorizontalBlock"]:nth-of-type(3)
            [data-testid="column"]:nth-child(2) .stButton > button:hover {
            background: #fff176 !important; transform: scale(1.06);
        }
        [data-testid="stHorizontalBlock"]:nth-of-type(3)
            [data-testid="column"]:nth-child(3) .stButton > button:hover {
            background: #ef9a9a !important; transform: scale(1.06);
        }

        /* ── Big action buttons (next / play again) ── */
        .big-btn > div > button {
            background: linear-gradient(90deg, #ffca28, #ff7043) !important;
            color: #1a1a2e !important; font-size: 1.2rem !important;
            font-family: 'Comic Sans MS', cursive !important; border-radius: 30px !important;
            border: none !important; padding: 12px 40px !important; font-weight: bold !important;
            box-shadow: 0 4px 14px rgba(255,112,67,0.35);
            min-height: auto !important; width: auto !important;
        }
        .big-btn > div > button:hover { transform: scale(1.07) !important; }

        /* ── Small restart button ── */
        .small-restart > div > button {
            background: #ede7f6 !important; color: #4527a0 !important;
            font-size: 0.8rem !important; font-family: 'Comic Sans MS', cursive !important;
            border-radius: 20px !important; border: 2px solid #b39ddb !important;
            padding: 4px 14px !important; font-weight: bold !important;
            min-height: 32px !important; width: auto !important; box-shadow: none;
        }
        .small-restart > div > button:hover {
            background: #d1c4e9 !important; border-color: #7c4dff !important;
            transform: scale(1.05) !important;
        }

        /* ── Teal change-level button ── */
        .refresh-btn > div > button {
            background: linear-gradient(90deg, #26c6da, #00897b) !important;
            color: #ffffff !important; font-size: 1rem !important;
            font-family: 'Comic Sans MS', cursive !important; border-radius: 30px !important;
            border: none !important; padding: 8px 24px !important; font-weight: bold !important;
            min-height: auto !important; width: auto !important;
        }
        .refresh-btn > div > button:hover { transform: scale(1.05) !important; }

        /* ── Name input ── */
        .stTextInput > div > div > input {
            border-radius: 20px !important; border: 3px solid #7c4dff !important;
            font-size: 1.2rem !important; padding: 12px 20px !important;
            background-color: #ffffff !important; color: #1a1a2e !important;
            font-family: 'Comic Sans MS', cursive !important;
        }
        .stTextInput > div > div > input::placeholder { color: #9e9e9e !important; }
        .stTextInput label {
            font-size: 1.05rem !important; font-weight: bold;
            color: #4527a0 !important; font-family: 'Comic Sans MS', cursive !important;
        }

        /* ── Score banner ── */
        .score-banner {
            background: linear-gradient(90deg, #7c4dff, #448aff);
            border-radius: 18px; padding: 14px 28px; text-align: center;
            color: #ffffff !important; font-size: 1.25rem;
            font-family: 'Comic Sans MS', cursive; font-weight: bold;
            box-shadow: 0 4px 16px rgba(124,77,255,0.3); margin-bottom: 1.2rem;
        }

        /* ── Question card ── */
        .question-card {
            background: #fffde7; border-radius: 22px; border: 3px solid #7c4dff;
            padding: 28px 36px; font-size: 1.5rem; font-weight: bold;
            color: #1a1a2e !important; font-family: 'Comic Sans MS', 'Chalkboard SE', cursive;
            text-align: center; box-shadow: 0 4px 18px rgba(124,77,255,0.15);
            margin-bottom: 1.8rem;
        }

        /* ── Feedback boxes ── */
        .feedback-correct {
            background: #e8f5e9; border: 3px solid #43a047; border-radius: 18px;
            padding: 18px 24px; color: #1b5e20 !important; font-size: 1.1rem;
            font-family: 'Comic Sans MS', cursive; margin-top: 1rem; line-height: 1.7;
        }
        .feedback-wrong {
            background: #fce4ec; border: 3px solid #e53935; border-radius: 18px;
            padding: 18px 24px; color: #b71c1c !important; font-size: 1.1rem;
            font-family: 'Comic Sans MS', cursive; margin-top: 1rem;
        }

        /* ── How to play box ── */
        .how-to-play {
            background: #f3e5f5; border-radius: 18px; border: 2px dashed #b39ddb;
            padding: 16px 24px; margin-top: 1rem;
            font-family: 'Comic Sans MS', cursive; font-size: 1rem;
            color: #1a1a2e !important;
        }
        .how-to-play li { margin-bottom: 6px; color: #1a1a2e !important; }

        /* ── End screen ── */
        .end-card {
            background: linear-gradient(135deg, #e8eaf6, #fff9c4);
            border-radius: 24px; border: 3px solid #7c4dff; padding: 2.5rem;
            text-align: center; font-family: 'Comic Sans MS', cursive;
            box-shadow: 0 6px 24px rgba(124,77,255,0.2);
        }
        .end-score { font-size: 3.5rem; font-weight: bold; color: #6a0dad !important; }
        .end-name  { font-size: 2rem; color: #4527a0 !important; font-weight: bold; margin-bottom: 0.3rem; }
        .end-msg   { font-size: 1.25rem; color: #4527a0 !important; margin-top: 0.5rem; }

        hr { border: none; border-top: 2px dashed #b39ddb; margin: 1rem 0; }
        .stAlert p { color: #1a1a2e !important; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── Fix #1 also via JS (belt-and-braces) ─────────────────────────────────────
components.html("""
<script>
function hideToggle() {
    try {
        var d = window.parent.document;
        // Hide by data-testid
        ['collapsedControl','baseButton-headerNoPadding'].forEach(function(id) {
            var el = d.querySelector('[data-testid="'+id+'"]');
            if (el) { el.style.display='none'; el.style.visibility='hidden'; }
        });
        // Hide any button whose icon text contains 'keyboard_double'
        d.querySelectorAll('button').forEach(function(btn) {
            if (btn.textContent.indexOf('keyboard_double') > -1) {
                btn.style.display='none';
            }
        });
    } catch(e) {}
}
hideToggle();
setTimeout(hideToggle, 600);
setTimeout(hideToggle, 1500);
</script>
""", height=0)


# ── LLM ───────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=1.0)

llm = get_llm()


# ── Level config — Fix #3 & #4: no description in card, animals kept for badge ─
LEVELS = {
    "Easy": {
        "animal": "🐱",
        "badge_class": "level-easy",
        "card_bg": "#e8f5e9", "card_border": "#43a047", "card_color": "#1b5e20",
        "desc": "Simple everyday words for beginners!",
        "prompt_instruction": (
            "Use very simple, common words that a 6-year-old knows every day "
            "(e.g. happy, big, fast, kind, loud). Words should be 3–5 letters long "
            "and found in basic picture books."
        ),
    },
    "Medium": {
        "animal": "🦅",
        "badge_class": "level-medium",
        "card_bg": "#fffde7", "card_border": "#fbc02d", "card_color": "#e65100",
        "desc": "A bit more tricky — no tiny 4-letter words!",
        "prompt_instruction": (
            "Use medium-difficulty words for a 6-year-old who is a good reader. "
            "Words must be at least 5 letters long. Examples: brave, shiny, gentle, quiet."
        ),
    },
    "Hard": {
        "animal": "🐯",
        "badge_class": "level-hard",
        "card_bg": "#ffebee", "card_border": "#e53935", "card_color": "#b71c1c",
        "desc": "Long, tricky words for Word Champions!",
        "prompt_instruction": (
            "Use longer advanced words for a smart 6–7 year old. "
            "Words should be 7+ letters. Examples: enormous, cheerful, frightened, wonderful."
        ),
    },
}

# Map levels to JS color-injection values
LEVEL_COLORS = {
    "Easy":   {"bg": "#e8f5e9", "border": "#43a047", "color": "#1b5e20"},
    "Medium": {"bg": "#fffde7", "border": "#fbc02d", "color": "#e65100"},
    "Hard":   {"bg": "#ffebee", "border": "#e53935", "color": "#b71c1c"},
}


# ── JS backup: color level buttons by innerText + interval retry ─────────────
def apply_level_colors():
    components.html("""
    <script>
    (function() {
        var colors = {
            'Easy':   {bg:'#c8e6c9', border:'#43a047', color:'#1b5e20'},
            'Medium': {bg:'#fff9c4', border:'#fbc02d', color:'#e65100'},
            'Hard':   {bg:'#ffcdd2', border:'#e53935', color:'#b71c1c'}
        };
        function applyColors() {
            try {
                var d = window.parent.document;
                var matched = 0;
                d.querySelectorAll('button').forEach(function(btn) {
                    var txt = (btn.innerText || btn.textContent || '').trim();
                    if (colors[txt]) {
                        var c = colors[txt];
                        btn.style.setProperty('background', c.bg, 'important');
                        btn.style.setProperty('border-color', c.border, 'important');
                        btn.style.setProperty('color', c.color, 'important');
                        btn.style.setProperty('font-size', '1.6rem', 'important');
                        btn.style.setProperty('font-weight', '900', 'important');
                        btn.style.setProperty('min-height', '100px', 'important');
                        matched++;
                    }
                });
                return matched;
            } catch(e) { return 0; }
        }
        // Immediate + interval until all 3 found or 20 tries
        var tries = 0;
        var iv = setInterval(function() {
            if (applyColors() >= 3 || ++tries > 20) clearInterval(iv);
        }, 150);
    })();
    </script>
    """, height=0)


# ── Fix #5: Celebration engine ─────────────────────────────────────────────────
def _inject_js(code: str):
    components.html(f"<script>{code}</script>", height=0)

def celebrate(correct_count: int):
    cel = correct_count % 5

    if cel == 0:
        # 🎈 Balloons (Streamlit built-in)
        st.balloons()

    elif cel == 1:
        # 🚀 Rockets flying up
        _inject_js("""
        (function() {
            var d = window.parent.document;
            [10,22,35,50,64,78,90].forEach(function(left, i) {
                var el = d.createElement('div');
                el.textContent = '🚀';
                var dur = 1700 + i * 120;
                el.style.cssText = 'position:fixed;left:'+left+'%;bottom:-80px;font-size:'+(2.2+i%3*0.4)+'rem;'
                    +'z-index:99999;pointer-events:none;'
                    +'transition:bottom '+dur+'ms ease-out;';
                d.body.appendChild(el);
                setTimeout(function(){ el.style.bottom='110vh'; }, 80 + i*60);
                setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, dur+700);
            });
        })();
        """)

    elif cel == 2:
        # ❄️ Snow burst (Fix #5: replaces old JS fireworks)
        st.snow()

    elif cel == 3:
        # 🦋 Butterflies + hearts floating up
        _inject_js("""
        (function() {
            var d = window.parent.document;
            var items = ['🦋','❤️','🦋','💛','🦋','�','�','🦋','�','�'];
            items.forEach(function(r, i) {
                var el = d.createElement('div');
                el.textContent = r;
                var left = 5 + i * 9.5;
                var dur  = 2000 + i*100;
                var sway = (i%2===0?1:-1)*30;
                el.style.cssText = 'position:fixed;left:'+left+'%;bottom:-80px;font-size:'+(2+i%3*0.4)+'rem;'
                    +'z-index:99999;pointer-events:none;'
                    +'transition:bottom '+dur+'ms ease-out, left '+(dur*0.8)+'ms ease-in-out;';
                d.body.appendChild(el);
                setTimeout(function(){ el.style.bottom='110vh'; el.style.left=(left+sway)+'%'; }, 80+i*40);
                setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, dur+700);
            });
        })();
        """)

    else:
        # 🌸 Fix #5 NEW: Roses & flowers dropping from the sky
        _inject_js("""
        (function() {
            var d = window.parent.document;
            var flowers = ['🌹','🌸','🌺','🌻','🌷','�','🌹','🌸','🌷','🌺','🌹','💐'];
            flowers.forEach(function(f, i) {
                var el = d.createElement('div');
                el.textContent = f;
                var left = Math.random()*90;
                var dur  = 2200 + i*100;
                var sway = (Math.random()-0.5)*40;
                el.style.cssText = 'position:fixed;left:'+left+'%;top:-80px;font-size:'+(2+Math.random()*1.5)+'rem;'
                    +'z-index:99999;pointer-events:none;'
                    +'transition:top '+dur+'ms ease-in, left '+(dur*0.7)+'ms ease-in-out;';
                d.body.appendChild(el);
                setTimeout(function(){ el.style.top='110vh'; el.style.left=(left+sway)+'%'; }, 80+i*50);
                setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, dur+700);
            });
        })();
        """)


# ── Session state ─────────────────────────────────────────────────────────────
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


# ── Quiz generation ───────────────────────────────────────────────────────────
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
- "explanation": short cheerful 1-2 sentence explanation for a young child (use emojis!)
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
# HEADER — title + tiny restart button on one row
# ══════════════════════════════════════════════════════════════════════════════
title_col, restart_col = st.columns([8, 2])
with title_col:
    st.title("🧩 Synonym Quiz Challenge!")
with restart_col:
    st.write("")
    st.markdown('<div class="small-restart">', unsafe_allow_html=True)
    if st.button("🔄 Restart", key="header_refresh"):
        init_quiz_state()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# START SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.quiz_started:

    # ── Name input directly under header ──────────────────────────────────────
    nc1, nc2, nc3 = st.columns([1, 4, 1])
    with nc2:
        st.markdown('<p class="section-heading">👋 What\'s your name?</p>',
                    unsafe_allow_html=True)
        name_val = st.text_input(
            "name", placeholder="e.g. Zayn, Emma, Leo...",
            label_visibility="collapsed", key="name_field",
        )
        st.session_state.player_name = name_val.strip()

    st.markdown("---")

    # ── Fix #4: Level cards — coloured, NO emoji, NO description ──────────────
    st.markdown('<p class="section-heading">🎚️ Tap a level to start playing!</p>',
                unsafe_allow_html=True)

    lcols = st.columns(3, gap="medium")
    for lk in LEVELS:
        with lcols[list(LEVELS.keys()).index(lk)]:
            # Label is just the level name — JS will color each button
            if st.button(lk, key=f"lvl_start_{lk}", use_container_width=True):
                if not st.session_state.player_name:
                    st.warning("🙈 Please type your name first! 😄")
                else:
                    st.session_state.selected_level = lk
                    with st.spinner(f"🤔 Building your {lk} quiz... ✨"):
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
                                st.error("😴 **Yawn!** I've played so many games today that my brain needs a quick 1-minute nap!\n\nStretch your arms, count to 60, and tap the level button to try again! 🌈")
                            else:
                                st.error(f"😬 Oops! Couldn't generate the quiz. Try again! ({e})")

    # Apply colors to the level buttons via JS
    apply_level_colors()

    # ── Fix #2: How to play — plain text, NOT a dropdown ──────────────────────
    st.markdown("---")
    st.markdown('<p class="section-heading">📖 How to play</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="how-to-play">
    <ul>
      <li>You'll get <b>10 questions</b> about synonyms (words that mean the same thing!)</li>
      <li>Pick the correct synonym from 4 big tiles 🖱️</li>
      <li>✅ Right answer = <b>+10 points</b> + a fun surprise celebration!</li>
      <li>❌ Wrong answer = try again — same question stays!</li>
      <li>Score as many points as you can out of <b>100</b>! 🏆</li>
    </ul>
    <b>Levels:</b> &nbsp; 🐱 Easy — 🦅 Medium — 🐯 Hard
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
        emoji, headline = "🏆", f"PERFECT SCORE, {name}!!"
        msg = "You are an absolute Word Champion! Incredible! 🎊"
    elif score >= 70:
        emoji, headline = "🌟", f"Amazing job, {name}!"
        msg = "You're a Synonym Superstar — keep it up! ⭐"
    elif score >= 40:
        emoji, headline = "👏", f"Well done, {name}!"
        msg = "Great effort! Keep practising and you'll be a pro! 💪"
    else:
        emoji, headline = "💪", f"Good try, {name}!"
        msg = "Practice makes perfect — you've got this! 🌈"

    st.balloons()
    st.markdown(f"""
        <div class="end-card">
            <div class="level-badge {cfg['badge_class']}" style="margin-bottom:1rem;">
                {cfg['animal']} {level_key} Level
            </div>
            <div style="font-size:4rem;">{emoji}</div>
            <div class="end-name">{headline}</div>
            <div class="end-score">{score} / 100</div>
            <div class="end-msg">{msg}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown('<div class="big-btn">', unsafe_allow_html=True)
        if st.button("🔄 Play Again!", key="end_play_again"):
            saved = st.session_state.used_words
            init_quiz_state()
            st.session_state.used_words = saved
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="refresh-btn">', unsafe_allow_html=True)
        if st.button("🎚️ Change Level", key="end_change_level"):
            saved = st.session_state.used_words
            init_quiz_state()
            st.session_state.used_words = saved
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cc:
        st.markdown(
            f'<p style="color:#6a0dad;font-family:Comic Sans MS,cursive;'
            f'text-align:center;font-size:0.85rem;padding-top:10px;">'
            f'📚 {len(st.session_state.used_words)} unique words<br>learned!</p>',
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

# Score + level banner
st.markdown(
    f'<div class="score-banner">'
    f'{cfg["animal"]} {level_key} &nbsp;|&nbsp; '
    f'👤 {name} &nbsp;|&nbsp; '
    f'⭐ {st.session_state.score} / 100 &nbsp;|&nbsp; '
    f'Q {idx + 1} / {total_q}'
    f'</div>',
    unsafe_allow_html=True)

st.progress(idx / total_q)

st.markdown(
    f'<div class="question-card">'
    f'🔤 What is a synonym for &nbsp;<u>{q["word"].upper()}</u> ?'
    f'</div>',
    unsafe_allow_html=True)

# ── Answer tiles ──────────────────────────────────────────────────────────────
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

# ── Feedback ──────────────────────────────────────────────────────────────────
if st.session_state.last_correct is not None:

    if st.session_state.last_correct:
        celebrate(st.session_state.correct_count - 1)
        st.markdown(
            f'<div class="feedback-correct">'
            f'✅ <b>Correct, {name}! Well done!</b> +10 points 🎉<br><br>'
            f'{q["explanation"]}'
            f'</div>',
            unsafe_allow_html=True)
        st.markdown("")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="big-btn">', unsafe_allow_html=True)
            next_label = "➡️ Next Question!" if idx + 1 < total_q else "🏁 See My Results!"
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
            f'❌ <b>Oops! "{chosen}" is not quite right.</b><br>'
            f'Try again, {name} — you can do it! 💪'
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
