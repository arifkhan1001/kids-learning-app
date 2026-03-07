import streamlit as st
import streamlit.components.v1 as components
from utils.reasoning_questions import get_reasoning_questions
import random

st.set_page_config(page_title="Reasoning", page_icon="🧩", layout="centered")

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
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border: 1.5px solid rgba(139,92,246,0.15) !important;
        border-radius: 14px !important;
        padding: 12px 14px !important;
        min-height: 54px !important;
        width: 100%;
        text-align: center !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        box-shadow: 0 2px 8px rgba(139,92,246,0.06);
        margin-bottom: 2px;
    }
    .stButton > button:hover {
        border-color: #8b5cf6 !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(139,92,246,0.15);
        background: rgba(255,255,255,1) !important;
    }

    /* ── Primary action buttons ── */
    .action-btn > div > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 0.95rem !important;
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

    /* ── Result card and score ── */
    .score-banner {
        background: linear-gradient(135deg, #7c3aed, #3b82f6, #06b6d4);
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        text-align: center;
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(124,58,237,0.2);
        margin-bottom: 0.5rem;
    }
    .score-banner strong { color: #ffffff; }

    /* ── Question card ── */
    .question-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a202c !important;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    /* ── Progress bar ── */
    .stProgress > div > div > div > div {
        background: #5a67d8 !important;
        border-radius: 999px;
    }

    /* ── Feedback ── */
    .feedback-correct {
        background: #f0fff4;
        border: 1px solid #c6f6d5;
        border-radius: 12px;
        padding: 12px 20px;
        color: #276749 !important;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        margin-top: 0.5rem;
    }
    .feedback-wrong {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        border-radius: 12px;
        padding: 12px 20px;
        color: #9b2c2c !important;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        margin-top: 0.5rem;
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
        color: #1a202c !important;
    }
    .end-headline {
        font-size: 1.6rem; font-weight: 700; color: #1a202c !important;
        margin-bottom: 8px;
    }
    .end-score {
        font-size: 2.5rem; font-weight: 700; color: #5a67d8 !important;
        margin: 12px 0;
    }
    .end-msg {
        font-size: 1rem; color: #718096 !important; font-weight: 400;
        margin-top: 8px;
    }
    
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Celebration animations ──
CELEBRATIONS = [
    """
    (function(){
        var d=window.parent.document;
        for(var i=0;i<30;i++){
            var s=d.createElement('div');
            var size=18+Math.random()*28;
            var left=Math.random()*100;
            var dur=1500+Math.random()*2000;
            var delay=Math.random()*1200;
            s.textContent='⭐';
            s.style.cssText='position:fixed;left:'+left+'%;top:-40px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:0.9;transition:top '+dur+'ms ease-in, left 0.5s ease, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(s);
            setTimeout(function(el,l){el.style.top='105vh';el.style.left=(l+Math.random()*10-5)+'%';el.style.opacity='0';}.bind(null,s,left),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,s),dur+2000);
        }
    })();
    """,
    """
    (function(){
        var d=window.parent.document, c=d.createElement('canvas');
        c.id='fw_canvas'; c.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:99999;pointer-events:none;';
        d.body.appendChild(c); var ctx=c.getContext('2d');
        c.width=window.innerWidth; c.height=window.innerHeight;
        var particles=[];
        var colors=['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#ff6fb6','#c792ea','#45f3ff'];
        for(var b=0;b<6;b++){
            var bx=Math.random()*c.width,by=Math.random()*c.height*0.5;
            for(var i=0;i<40;i++){
                var angle=Math.random()*Math.PI*2, speed=2+Math.random()*6;
                particles.push({x:bx,y:by,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,
                    life:60+Math.random()*40,age:0,color:colors[Math.floor(Math.random()*colors.length)],
                    size:3+Math.random()*5});
            }
        }
        var frame=0;
        function anim(){
            ctx.clearRect(0,0,c.width,c.height);
            var alive=false;
            particles.forEach(function(p){
                p.age++; if(p.age>p.life) return;
                alive=true; p.x+=p.vx; p.y+=p.vy; p.vy+=0.08;
                var alpha=1-p.age/p.life;
                ctx.beginPath(); ctx.arc(p.x,p.y,p.size*alpha,0,Math.PI*2);
                ctx.fillStyle=p.color; ctx.globalAlpha=alpha; ctx.fill();
            });
            ctx.globalAlpha=1;
            if(alive&&frame<180){frame++;requestAnimationFrame(anim);}
            else{c.remove();}
        }
        anim();
    })();
    """
]
def celebrate(correct_count: int):
    effect_index = correct_count % len(CELEBRATIONS)
    components.html(f"<script>{CELEBRATIONS[effect_index]}</script>", height=0)


# ── Session state ────────────────────────────────────────────────────────────
def init_quiz_state():
    st.session_state.reason_questions = []
    st.session_state.reason_current_q = 0
    st.session_state.reason_score = 0
    st.session_state.reason_correct = 0
    st.session_state.reason_answered = False
    st.session_state.reason_last_correct = None
    st.session_state.reason_last_chosen = None
    st.session_state.reason_started = False
    st.session_state.reason_done = False
    st.session_state.reason_level = None

if "reason_started" not in st.session_state:
    init_quiz_state()

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
    <h1>Reasoning Quiz</h1>
    <p class="page-subtitle">Test your logic and problem-solving skills</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# START SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.reason_started:
    st.markdown('<p class="section-label">Choose a difficulty level</p>', unsafe_allow_html=True)

    lcols = st.columns(3, gap="medium")
    levels = ["Easy", "Medium", "Hard"]
    
    for idx, lk in enumerate(levels):
        with lcols[idx]:
            if st.button(lk, key=f"lvl_start_{lk}", use_container_width=True):
                st.session_state.reason_level = lk
                st.session_state.reason_questions = get_reasoning_questions(lk, 10)
                st.session_state.reason_started = True
                st.session_state.reason_current_q = 0
                st.session_state.reason_score = 0
                st.session_state.reason_correct = 0
                st.session_state.reason_answered = False
                st.session_state.reason_done = False
                st.rerun()

    components.html("""
    <script>
    (function() {
        var d = window.parent.document;
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
    })();
    </script>
    """, height=0)

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# END SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.reason_done:
    score = st.session_state.reason_score

    if score == 100:
        headline = "Perfect score!"
        msg = "You are a master of logic! Excellent job."
    elif score >= 70:
        headline = "Great work!"
        msg = "Your reasoning skills are sharp. Keep it up!"
    elif score >= 40:
        headline = "Good try!"
        msg = "You're getting better at solving these puzzles!"
    else:
        headline = "Keep practicing!"
        msg = "Puzzles can be tricky, but practice makes perfect."

    st.markdown(f"""
    <div class="end-card" style="color: #1a202c !important;">
        <div class="end-headline" style="color: #1a202c !important;">{headline}</div>
        <div class="end-score" style="color: #5a67d8 !important;">{score} / 100</div>
        <div class="end-msg" style="color: #718096 !important;">{msg}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        st.markdown('<div class="action-btn" style="text-align: center;">', unsafe_allow_html=True)
        if st.button("Play Again", use_container_width=True):
            init_quiz_state()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    components.html("""
    <script>
    (function() {
        var d = window.parent.document;
        if (!d.getElementById('quiz-style-fix')) {
            var s = d.createElement('style');
            s.id = 'quiz-style-fix';
            s.textContent = `
                .stApp .end-card, .stApp .end-card * { color: inherit !important; }
                .stApp .end-card { color: #1a202c !important; }
                .stApp .end-headline { color: #1a202c !important; }
                .stApp .end-score { color: #5a67d8 !important; }
                .stApp .end-msg { color: #718096 !important; }
                .stApp .action-btn button, .stApp .action-btn button * { color: #ffffff !important; }
            `;
            d.head.appendChild(s);
        }
    })();
    </script>
    """, height=0)

    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# QUIZ SCREEN
# ══════════════════════════════════════════════════════════════════════════════
idx = st.session_state.reason_current_q
total = len(st.session_state.reason_questions)
q_data = st.session_state.reason_questions[idx]

# Progress + Restart
c1, c2 = st.columns([4, 1])
with c1:
    prog = (idx) / total
    st.progress(prog, text=f"Question {idx + 1} of {total}")
with c2:
    st.markdown('<div class="restart-btn" style="text-align:right;">', unsafe_allow_html=True)
    if st.button("Restart"):
        init_quiz_state()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Score banner
st.markdown(
    f'<div class="score-banner">Score: <strong>{st.session_state.reason_score}</strong></div>',
    unsafe_allow_html=True
)

# Question
st.markdown(f"""
<div class="question-card">
    {q_data['question']}
</div>
""", unsafe_allow_html=True)

# Answer check logic
def handle_answer(opt):
    st.session_state.reason_answered = True
    st.session_state.reason_last_chosen = opt
    if opt == q_data["answer"]:
        st.session_state.reason_last_correct = True
        st.session_state.reason_score += 10
        st.session_state.reason_correct += 1
    else:
        st.session_state.reason_last_correct = False

# Options
opts = q_data["options"]
c_left, c_right = st.columns(2, gap="medium")

# Option buttons
if not st.session_state.reason_answered:
    for i, opt in enumerate(opts):
        col = c_left if i % 2 == 0 else c_right
        with col:
            if st.button(opt, key=f"opt_{idx}_{opt}", use_container_width=True):
                handle_answer(opt)
                st.rerun()
else:
    # Disabled buttons to show chosen answer
    for i, opt in enumerate(opts):
        col = c_left if i % 2 == 0 else c_right
        with col:
            st.button(opt, key=f"opt_{idx}_{opt}_disabled", disabled=True, use_container_width=True)

# Feedback
if st.session_state.reason_answered:
    if st.session_state.reason_last_correct:
        celebrate(st.session_state.reason_correct)
        st.markdown(f'<div class="feedback-correct">✅ Sharp thinking! That is correct.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="feedback-wrong">❌ Not exactly. The correct answer was <strong>{q_data["answer"]}</strong>. Try the next one!</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        st.markdown('<div class="action-btn" style="text-align: center;">', unsafe_allow_html=True)
        btn_label = "Next Question" if idx < total - 1 else "See Results"
        if st.button(btn_label, use_container_width=True):
            if idx < total - 1:
                st.session_state.reason_current_q += 1
                st.session_state.reason_answered = False
            else:
                st.session_state.reason_done = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

components.html("""
<script>
(function() {
    var d = window.parent.document;
    if (!d.getElementById('quiz-style-fix')) {
        var s = d.createElement('style');
        s.id = 'quiz-style-fix';
        s.textContent = `
            .stApp .question-card, .stApp .question-card * { color: inherit !important; }
            .stApp .question-card { color: #1a202c !important; }
            .stApp .feedback-correct, .stApp .feedback-correct * { color: inherit !important; }
            .stApp .feedback-correct { color: #276749 !important; }
            .stApp .feedback-wrong, .stApp .feedback-wrong * { color: inherit !important; }
            .stApp .feedback-wrong { color: #9b2c2c !important; }
            .stApp button[kind="secondary"], .stApp button[kind="secondary"] * { color: #1a202c !important; }
            .stApp .action-btn button, .stApp .action-btn button * { color: #ffffff !important; }
            .stApp .restart-btn button, .stApp .restart-btn button * { color: #1a202c !important; background: rgba(255,255,255,0.85) !important; }
        `;
        d.head.appendChild(s);
    }
})();
</script>
""", height=0)
