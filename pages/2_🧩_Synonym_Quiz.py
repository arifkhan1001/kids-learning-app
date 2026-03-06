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


# ── Celebration engine — diverse effects for each question ────────────────────
def _inject_js(code: str):
    components.html(f"<script>{code}</script>", height=0)

CELEBRATIONS = [
    # 0: BALLOONS — colorful balloons rising up (first answer!)
    """
    (function(){
        var d=window.parent.document;
        for(var i=0;i<35;i++){
            var b=d.createElement('div');
            var size=35+Math.random()*40;
            var left=Math.random()*100;
            var dur=2500+Math.random()*2500;
            var delay=Math.random()*1500;
            var hue=Math.floor(Math.random()*360);
            b.textContent='🎈';
            b.style.cssText='position:fixed;left:'+left+'%;bottom:-60px;font-size:'+size+'px;z-index:99999;pointer-events:none;filter:hue-rotate('+hue+'deg);transition:bottom '+dur+'ms ease-out, opacity '+(dur*0.8)+'ms ease-in;opacity:0.9;';
            d.body.appendChild(b);
            setTimeout(function(el){el.style.bottom='110vh';el.style.opacity='0';}.bind(null,b),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,b),dur+2000);
        }
    })();
    """,
    # 1: FIREWORKS — colorful bursts from random positions
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
    """,
    # 1: SNOWFLAKES — big white flakes drifting down
    """
    (function(){
        var d=window.parent.document;
        var flakes=['❄','❅','❆','✦','✧'];
        for(var i=0;i<35;i++){
            var s=d.createElement('div');
            var size=16+Math.random()*28;
            var left=Math.random()*100;
            var dur=2000+Math.random()*3000;
            var delay=Math.random()*1500;
            s.textContent=flakes[Math.floor(Math.random()*flakes.length)];
            s.style.cssText='position:fixed;left:'+left+'%;top:-40px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:0.85;color:#fff;text-shadow:0 0 8px #b3e0ff;transition:top '+dur+'ms ease-in, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(s);
            setTimeout(function(el){el.style.top='105vh';el.style.opacity='0';}.bind(null,s),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,s),dur+2000);
        }
    })();
    """,
    # 2: FLOWERS — petals and flowers drifting down
    """
    (function(){
        var d=window.parent.document;
        var flowers=['🌸','🌺','🌼','🌻','🌷','💐','🌹','🏵️'];
        for(var i=0;i<30;i++){
            var f=d.createElement('div');
            var size=18+Math.random()*26;
            var left=Math.random()*100;
            var dur=2000+Math.random()*2500;
            var delay=Math.random()*1200;
            var rot=Math.random()*360;
            f.textContent=flowers[Math.floor(Math.random()*flowers.length)];
            f.style.cssText='position:fixed;left:'+left+'%;top:-50px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:0.9;transform:rotate('+rot+'deg);transition:top '+dur+'ms ease-in, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(f);
            setTimeout(function(el){el.style.top='105vh';el.style.opacity='0';}.bind(null,f),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,f),dur+2000);
        }
    })();
    """,
    # 4: THUNDERSTORM — lightning flashes with thunder emoji rain
    """
    (function(){
        var d=window.parent.document;
        var overlay=d.createElement('div');
        overlay.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:99998;pointer-events:none;background:transparent;';
        d.body.appendChild(overlay);
        var flashes=[200,600,800,1400,1800];
        flashes.forEach(function(t){
            setTimeout(function(){
                overlay.style.background='rgba(255,255,255,0.7)';
                setTimeout(function(){overlay.style.background='transparent';},100);
            },t);
        });
        setTimeout(function(){overlay.remove();},3000);
        var emojis=['⚡','🌩️','⛈️','💨','🌊'];
        for(var i=0;i<20;i++){
            var e=d.createElement('div');
            var size=22+Math.random()*24;
            var left=Math.random()*100;
            var dur=1500+Math.random()*2000;
            var delay=Math.random()*1500;
            e.textContent=emojis[Math.floor(Math.random()*emojis.length)];
            e.style.cssText='position:fixed;left:'+left+'%;top:-40px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:0.85;transition:top '+dur+'ms ease-in, opacity '+(dur*0.7)+'ms ease-in;';
            d.body.appendChild(e);
            setTimeout(function(el){el.style.top='105vh';el.style.opacity='0';}.bind(null,e),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,e),dur+2000);
        }
    })();
    """,
    # 5: RAINBOW RAIN — colored drops falling
    """
    (function(){
        var d=window.parent.document;
        var rainbow=['#ff0000','#ff7700','#ffdd00','#00cc00','#0077ff','#8800ff','#ff00aa'];
        for(var i=0;i<50;i++){
            var drop=d.createElement('div');
            var left=Math.random()*100;
            var w=3+Math.random()*5;
            var h=12+Math.random()*20;
            var dur=1000+Math.random()*2000;
            var delay=Math.random()*1500;
            var color=rainbow[Math.floor(Math.random()*rainbow.length)];
            drop.style.cssText='position:fixed;left:'+left+'%;top:-30px;width:'+w+'px;height:'+h+'px;border-radius:'+w+'px;background:'+color+';z-index:99999;pointer-events:none;opacity:0.7;transition:top '+dur+'ms linear, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(drop);
            setTimeout(function(el){el.style.top='105vh';el.style.opacity='0';}.bind(null,drop),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,drop),dur+2000);
        }
    })();
    """,
    # 6: STARS — shooting stars and sparkles
    """
    (function(){
        var d=window.parent.document;
        var stars=['⭐','🌟','✨','💫','🌠','⚡'];
        for(var i=0;i<30;i++){
            var s=d.createElement('div');
            var size=18+Math.random()*28;
            var left=Math.random()*100;
            var dur=1500+Math.random()*2000;
            var delay=Math.random()*1200;
            s.textContent=stars[Math.floor(Math.random()*stars.length)];
            s.style.cssText='position:fixed;left:'+left+'%;top:-40px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:0.9;transition:top '+dur+'ms ease-in, left 0.5s ease, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(s);
            setTimeout(function(el,l){el.style.top='105vh';el.style.left=(l+Math.random()*10-5)+'%';el.style.opacity='0';}.bind(null,s,left),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,s),dur+2000);
        }
    })();
    """,
    # 7: HEARTS — red and pink hearts rising
    """
    (function(){
        var d=window.parent.document;
        var hearts=['❤️','💖','💗','💕','💝','💘','💓','🩷'];
        for(var i=0;i<28;i++){
            var h=d.createElement('div');
            var size=20+Math.random()*30;
            var left=Math.random()*100;
            var dur=2000+Math.random()*2500;
            var delay=Math.random()*1500;
            h.textContent=hearts[Math.floor(Math.random()*hearts.length)];
            h.style.cssText='position:fixed;left:'+left+'%;bottom:-50px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:0.85;transition:bottom '+dur+'ms ease-out, opacity '+(dur*0.7)+'ms ease-in;';
            d.body.appendChild(h);
            setTimeout(function(el){el.style.bottom='110vh';el.style.opacity='0';}.bind(null,h),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,h),dur+2000);
        }
    })();
    """,
    # 8: BUBBLES — translucent circles rising
    """
    (function(){
        var d=window.parent.document;
        var colors=['rgba(100,180,255,0.5)','rgba(180,100,255,0.4)','rgba(100,255,200,0.4)','rgba(255,180,100,0.4)','rgba(255,100,180,0.4)'];
        for(var i=0;i<30;i++){
            var b=d.createElement('div');
            var size=20+Math.random()*50;
            var left=Math.random()*100;
            var dur=2500+Math.random()*2500;
            var delay=Math.random()*1500;
            var color=colors[Math.floor(Math.random()*colors.length)];
            b.style.cssText='position:fixed;left:'+left+'%;bottom:-60px;width:'+size+'px;height:'+size+'px;border-radius:50%;background:'+color+';border:2px solid rgba(255,255,255,0.6);z-index:99999;pointer-events:none;transition:bottom '+dur+'ms ease-out, opacity '+(dur*0.7)+'ms ease-in;opacity:0.8;';
            d.body.appendChild(b);
            setTimeout(function(el){el.style.bottom='110vh';el.style.opacity='0';}.bind(null,b),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,b),dur+2000);
        }
    })();
    """,
    # 9: SPARKLE BURST — big emoji explosion from center
    """
    (function(){
        var d=window.parent.document;
        var emojis=['🎉','🎊','🥳','🏆','👏','💯','🔥','✅','🙌','👑'];
        var cx=window.innerWidth/2, cy=window.innerHeight/2;
        for(var i=0;i<35;i++){
            var e=d.createElement('div');
            var size=22+Math.random()*30;
            var angle=Math.random()*Math.PI*2;
            var dist=100+Math.random()*300;
            var dur=1500+Math.random()*1500;
            var delay=Math.random()*400;
            e.textContent=emojis[Math.floor(Math.random()*emojis.length)];
            e.style.cssText='position:fixed;left:'+cx+'px;top:'+cy+'px;font-size:'+size+'px;z-index:99999;pointer-events:none;opacity:1;transition:left '+dur+'ms ease-out, top '+dur+'ms ease-out, opacity '+(dur*0.8)+'ms ease-in;';
            d.body.appendChild(e);
            var fx=cx+Math.cos(angle)*dist;
            var fy=cy+Math.sin(angle)*dist;
            setTimeout(function(el,x,y){el.style.left=x+'px';el.style.top=y+'px';el.style.opacity='0';}.bind(null,e,fx,fy),50+delay);
            setTimeout(function(el){if(el.parentNode)el.parentNode.removeChild(el);}.bind(null,e),dur+2000);
        }
    })();
    """,
]

def celebrate(correct_count: int):
    """Pick a different celebration effect for each question."""
    effect_index = correct_count % len(CELEBRATIONS)
    _inject_js(CELEBRATIONS[effect_index])


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
                /* Force dark text inside white cards */
                .stApp .question-card,
                .stApp .question-card *,
                .stApp .feedback-correct,
                .stApp .feedback-correct *,
                .stApp .feedback-wrong,
                .stApp .feedback-wrong *,
                .stApp .end-card,
                .stApp .end-card *,
                .stApp .how-to-play,
                .stApp .how-to-play * {
                    color: inherit !important;
                }
                .stApp .question-card { color: #1a202c !important; }
                .stApp .feedback-correct { color: #276749 !important; }
                .stApp .feedback-wrong { color: #9b2c2c !important; }
                .stApp .end-card { color: #1a202c !important; }
                .stApp .end-headline { color: #1a202c !important; }
                .stApp .end-score { color: #5a67d8 !important; }
                .stApp .end-msg { color: #718096 !important; }
                .stApp .how-to-play,
                .stApp .how-to-play li,
                .stApp .how-to-play ul,
                .stApp .how-to-play strong { color: #4a5568 !important; }
                .stApp .section-label { color: rgba(255,255,255,0.9) !important; }
                .stApp .score-banner { color: rgba(255,255,255,0.9) !important; }
                .stApp .score-banner strong { color: #ffffff !important; }
                .stApp .action-btn button,
                .stApp .action-btn button p,
                .stApp .action-btn button span { color: #ffffff !important; }
                .stApp .restart-btn button,
                .stApp .restart-btn button p,
                .stApp .restart-btn button span { color: #1a202c !important; background: rgba(255,255,255,0.85) !important; }
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
