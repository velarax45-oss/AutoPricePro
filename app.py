import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="AutoPricePro", page_icon="🚗", layout="wide")

# ─────────────────────────────────────────────
#  AUTH CONFIG  — change credentials here
# ─────────────────────────────────────────────
USERS = {
    "admin": "autoprice2024",
    "demo":  "demo123",
}

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_error" not in st.session_state:
    st.session_state.login_error = ""

# ─────────────────────────────────────────────
#  CUTE LAMP LOGIN PAGE
# ─────────────────────────────────────────────
def show_login():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Quicksand:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    background: linear-gradient(135deg, #fde8f0 0%, #fff8e7 40%, #ffecd2 100%) !important;
    font-family: 'Nunito', sans-serif !important;
    color: #4a3728 !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Floating blobs background */
.blob1 {
    position: fixed; top: -80px; left: -80px;
    width: 320px; height: 320px; border-radius: 50%;
    background: rgba(255,182,193,0.25);
    animation: blob 9s ease-in-out infinite;
    pointer-events: none; z-index: 0;
}
.blob2 {
    position: fixed; bottom: -60px; right: -60px;
    width: 280px; height: 280px; border-radius: 50%;
    background: rgba(255,222,130,0.28);
    animation: blob 12s ease-in-out infinite reverse;
    pointer-events: none; z-index: 0;
}
.blob3 {
    position: fixed; top: 50%; right: -40px;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,200,170,0.22);
    animation: blob 7s ease-in-out infinite 3s;
    pointer-events: none; z-index: 0;
}
@keyframes blob {
    0%,100% { transform: scale(1) translate(0,0); }
    33%      { transform: scale(1.06) translate(10px,-12px); }
    66%      { transform: scale(0.94) translate(-8px,10px); }
}

/* Sparkles */
.sparkle {
    position: fixed;
    width: 6px; height: 6px;
    background: #f9c74f;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    animation: twinkle 3s ease-in-out infinite;
}
@keyframes twinkle {
    0%,100% { opacity:0; transform: scale(0.5); }
    50%      { opacity:1; transform: scale(1); }
}

/* Login card */
.lamp-card {
    position: relative;
    z-index: 10;
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 28px;
    overflow: hidden;
    box-shadow:
        0 8px 40px rgba(255,160,100,0.18),
        0 2px 12px rgba(0,0,0,0.06),
        inset 0 1px 0 rgba(255,255,255,0.9);
    max-width: 820px;
    width: 100%;
    min-height: 480px;
    animation: cardPop 0.6s cubic-bezier(0.34,1.56,0.64,1) both;
}
@keyframes cardPop {
    from { opacity:0; transform: scale(0.88) translateY(20px); }
    to   { opacity:1; transform: scale(1)    translateY(0); }
}

/* Left panel — lamp side */
.lamp-panel {
    background: linear-gradient(170deg, #fff3cd 0%, #ffe8a0 50%, #ffd166 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 2rem;
    position: relative;
    overflow: hidden;
}
.lamp-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse 70% 60% at 50% 35%, rgba(255,255,200,0.6), transparent 70%);
    pointer-events: none;
}

/* Lamp SVG scene */
.lamp-scene {
    position: relative;
    z-index: 2;
    animation: lampFloat 4s ease-in-out infinite;
}
@keyframes lampFloat {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}

/* Glow ring under lamp */
.lamp-glow {
    width: 120px; height: 24px;
    background: radial-gradient(ellipse, rgba(255,200,60,0.55), transparent 70%);
    border-radius: 50%;
    margin: -4px auto 0;
    animation: glowPulse 2.5s ease-in-out infinite;
}
@keyframes glowPulse {
    0%,100% { opacity:0.6; transform: scaleX(1); }
    50%      { opacity:1;   transform: scaleX(1.12); }
}

.lamp-tagline {
    font-family: 'Quicksand', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #a0742a;
    text-align: center;
    margin-top: 1.6rem;
    letter-spacing: 0.06em;
    z-index: 2;
    position: relative;
}

/* Right panel — form side */
.form-panel {
    padding: 2.8rem 2.6rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.form-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #3d2b1f;
    line-height: 1.1;
    margin-bottom: 0.35rem;
}
.form-sub {
    font-size: 0.88rem;
    color: #9b7b6a;
    margin-bottom: 2rem;
    font-weight: 500;
}

/* Error state */
.form-error {
    background: rgba(255,80,80,0.08);
    border: 1.5px solid rgba(255,80,80,0.25);
    border-radius: 14px;
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    color: #d95353;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 6px;
    animation: shake 0.35s ease;
}
@keyframes shake {
    0%,100%{transform:translateX(0)}
    20%{transform:translateX(-5px)}
    60%{transform:translateX(5px)}
}

/* Streamlit input overrides */
div[data-testid="stTextInput"] label {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    color: #9b7b6a !important;
    text-transform: uppercase !important;
    margin-bottom: 2px !important;
}
div[data-testid="stTextInput"] input {
    background: rgba(255,248,235,0.9) !important;
    border: 2px solid rgba(255,180,80,0.3) !important;
    border-radius: 14px !important;
    color: #3d2b1f !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #f9a825 !important;
    box-shadow: 0 0 0 4px rgba(249,168,37,0.12) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #c4a882 !important;
    font-weight: 500 !important;
}

/* Login button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #f9a825 0%, #fb8c00 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.8rem 0 !important;
    width: 100% !important;
    margin-top: 1.4rem !important;
    box-shadow: 0 4px 18px rgba(249,168,37,0.4) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 28px rgba(249,168,37,0.5) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) scale(0.99) !important;
}

.signup-hint {
    text-align: center;
    margin-top: 1.4rem;
    font-size: 0.82rem;
    color: #9b7b6a;
    font-weight: 600;
}
.signup-hint span {
    color: #e07b00;
    font-weight: 800;
    cursor: pointer;
}
</style>

<div class="blob1"></div>
<div class="blob2"></div>
<div class="blob3"></div>

<script>
(function(){
    const positions = [
        {top:'12%',left:'22%',delay:'0s'},
        {top:'18%',left:'68%',delay:'1.2s'},
        {top:'55%',left:'12%',delay:'0.6s'},
        {top:'72%',left:'55%',delay:'2s'},
        {top:'35%',left:'82%',delay:'0.3s'},
        {top:'85%',left:'30%',delay:'1.6s'},
    ];
    positions.forEach(pos => {
        const s = document.createElement('div');
        s.className = 'sparkle';
        s.style.top = pos.top;
        s.style.left = pos.left;
        s.style.animationDelay = pos.delay;
        document.body.appendChild(s);
    });
})();
</script>
""", unsafe_allow_html=True)

    # Layout: narrow outer cols to center card
    _, center_col, _ = st.columns([0.5, 3, 0.5])

    with center_col:
        # Left panel (lamp illustration) + right panel (form) via sub-columns
        lamp_col, form_col = st.columns([1, 1])

        with lamp_col:
            st.markdown("""
            <div style="background:linear-gradient(170deg,#fff3cd 0%,#ffe8a0 50%,#ffd166 100%);
                 border-radius:28px 0 0 28px;padding:2.5rem 1.5rem;min-height:460px;
                 display:flex;flex-direction:column;align-items:center;justify-content:center;
                 position:relative;overflow:hidden;animation:cardPop 0.6s cubic-bezier(0.34,1.56,0.64,1) both;">

              <!-- Radial glow bg -->
              <div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 55% at 50% 32%,rgba(255,255,180,0.65),transparent 70%);pointer-events:none;"></div>

              <!-- Lamp SVG -->
              <div style="position:relative;z-index:2;animation:lampFloat 4s ease-in-out infinite;">
                <svg width="130" height="180" viewBox="0 0 130 180" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <!-- Lamp shade -->
                  <ellipse cx="65" cy="48" rx="52" ry="12" fill="#f9a825" opacity="0.25"/>
                  <path d="M18 50 Q30 20 65 14 Q100 20 112 50 Q100 80 65 82 Q30 80 18 50Z" fill="#ffd54f"/>
                  <path d="M22 50 Q33 24 65 18 Q97 24 108 50 Q97 76 65 78 Q33 76 22 50Z" fill="#ffe082"/>
                  <!-- Shade rim -->
                  <ellipse cx="65" cy="80" rx="43" ry="9" fill="#f9a825" opacity="0.6"/>
                  <ellipse cx="65" cy="80" rx="43" ry="9" fill="none" stroke="#e07b00" stroke-width="1.5"/>
                  <!-- Inner light glow -->
                  <ellipse cx="65" cy="50" rx="28" ry="22" fill="#fff9c4" opacity="0.7"/>
                  <!-- Bulb -->
                  <circle cx="65" cy="88" r="11" fill="#fff9c4" stroke="#f9a825" stroke-width="2"/>
                  <circle cx="65" cy="88" r="7" fill="#fffde7"/>
                  <!-- Pole -->
                  <rect x="61" y="98" width="8" height="52" rx="4" fill="#a0826d"/>
                  <!-- Base disc -->
                  <ellipse cx="65" cy="152" rx="26" ry="7" fill="#8d6e63"/>
                  <ellipse cx="65" cy="150" rx="22" ry="5" fill="#a0826d"/>
                  <!-- Light rays -->
                  <line x1="65" y1="82" x2="20" y2="112" stroke="#ffe082" stroke-width="1.5" opacity="0.5" stroke-dasharray="3 4"/>
                  <line x1="65" y1="82" x2="110" y2="112" stroke="#ffe082" stroke-width="1.5" opacity="0.5" stroke-dasharray="3 4"/>
                  <line x1="65" y1="82" x2="65" y2="125" stroke="#ffe082" stroke-width="1.5" opacity="0.4" stroke-dasharray="3 4"/>
                  <!-- Stars -->
                  <text x="30" y="36" font-size="14" fill="#f9a825" opacity="0.9">✦</text>
                  <text x="92" y="30" font-size="11" fill="#ffcc02" opacity="0.8">✦</text>
                  <text x="15" y="75" font-size="9"  fill="#f9a825" opacity="0.6">✦</text>
                  <text x="108" y="70" font-size="10" fill="#ffcc02" opacity="0.7">✦</text>
                </svg>
              </div>

              <!-- Glow puddle -->
              <div style="width:110px;height:20px;background:radial-gradient(ellipse,rgba(255,200,50,0.5),transparent 70%);
                   border-radius:50%;margin:-6px auto 0;animation:glowPulse 2.5s ease-in-out infinite;position:relative;z-index:2;"></div>

              <!-- Tagline -->
              <p style="font-family:'Quicksand',sans-serif;font-size:0.85rem;font-weight:700;color:#a0742a;
                   text-align:center;margin-top:1.4rem;z-index:2;position:relative;line-height:1.5;">
                Bright ideas<br>start here ✨
              </p>
            </div>
            """, unsafe_allow_html=True)

        with form_col:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.88);border-radius:0 28px 28px 0;padding:2.8rem 2rem;
                 min-height:460px;display:flex;flex-direction:column;justify-content:center;
                 animation:cardPop 0.6s 0.1s cubic-bezier(0.34,1.56,0.64,1) both;backdrop-filter:blur(12px);">
              <div style="font-family:'Nunito',sans-serif;font-size:1.75rem;font-weight:900;color:#3d2b1f;line-height:1.1;margin-bottom:0.3rem;">
                Welcome Back
              </div>
              <div style="font-size:0.85rem;color:#9b7b6a;font-weight:600;margin-bottom:1.6rem;">
                Sign in to your cozy corner.
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.login_error:
                st.markdown(f"""
                <div class="form-error">⚠ &nbsp;{st.session_state.login_error}</div>
                """, unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", placeholder="••••••••••••", type="password", key="login_pass")

            if st.button("Login ✨", key="login_btn"):
                if username in USERS and USERS[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.login_error = ""
                    st.rerun()
                else:
                    st.session_state.login_error = "Invalid credentials. Please try again."
                    st.rerun()

            st.markdown("""
            <div style="text-align:center;margin-top:1.2rem;font-size:0.8rem;color:#9b7b6a;font-weight:600;">
              No account? <span style="color:#e07b00;font-weight:800;">Sign up</span>
            </div>
            <div style="text-align:center;margin-top:0.8rem;font-size:0.72rem;color:#c4a882;">
              Demo: <b style="color:#e07b00;">demo</b> / <b style="color:#e07b00;">demo123</b>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  GATE
# ─────────────────────────────────────────────
if not st.session_state.authenticated:
    show_login()
    st.stop()

# ── LOGOUT BUTTON (top-right) ──
with st.container():
    _lc1, _lc2 = st.columns([9, 1])
    with _lc2:
        if st.button("LOGOUT", key="logout_btn"):
            st.session_state.authenticated = False
            st.rerun()



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');
:root {
    --bg:#080a0e;--bg-card:#0e1118;--bg-glass:rgba(14,17,24,0.92);
    --gold:#c8a84b;--gold-lt:#e5c96b;--gold-dim:rgba(200,168,75,0.12);
    --gold-glow:rgba(200,168,75,0.30);--silver:#a0a8b8;--text:#edeae4;
    --muted:#5a6070;--border:rgba(200,168,75,0.22);--border-hi:rgba(200,168,75,0.55);
    --red:#e04040;--blue:#4080e0;
}
html,body,[class*="css"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:'Exo 2',sans-serif!important;}
.stApp{background:linear-gradient(rgba(200,168,75,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(200,168,75,0.025) 1px,transparent 1px),radial-gradient(ellipse 80% 50% at 50% -20%,rgba(200,168,75,0.07),transparent),var(--bg)!important;background-size:48px 48px,48px 48px,auto,auto!important;}
.block-container{padding-top:0!important;max-width:1140px!important;}
#MainMenu,footer,header{visibility:hidden!important;}
::-webkit-scrollbar{width:3px;}::-webkit-scrollbar-thumb{background:var(--gold);border-radius:2px;}
.hero{text-align:center;padding:2.8rem 0 1.6rem;position:relative;}
.hero-eyebrow{display:inline-flex;align-items:center;gap:10px;font-family:'Rajdhani',sans-serif;font-size:0.62rem;font-weight:700;letter-spacing:0.42em;color:var(--gold);text-transform:uppercase;background:var(--gold-dim);border:1px solid var(--border);padding:5px 18px 4px;clip-path:polygon(10px 0%,100% 0%,calc(100% - 10px) 100%,0% 100%);margin-bottom:1.1rem;}
.hero-title{font-family:'Rajdhani',sans-serif;font-size:clamp(2.6rem,5vw,4.2rem);font-weight:700;letter-spacing:0.08em;line-height:0.95;margin:0 0 0.5rem;background:linear-gradient(160deg,#f7e8b0 0%,#c8a84b 40%,#7a5a18 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:0.78rem;letter-spacing:0.22em;color:var(--muted);font-weight:300;font-style:italic;}
.hero-rule{width:100px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:1.3rem auto 0;}
.g-card{background:var(--bg-glass);border:1px solid var(--border);border-radius:3px;padding:1.6rem 1.8rem;margin-bottom:1rem;position:relative;overflow:hidden;backdrop-filter:blur(10px);}
.g-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 0%,var(--gold) 40%,var(--gold-lt) 60%,transparent 100%);}
.g-card::after{content:'';position:absolute;bottom:0;right:0;width:80px;height:80px;background:radial-gradient(circle,var(--gold-dim),transparent 70%);pointer-events:none;}
.g-card-title{font-family:'Rajdhani',sans-serif;font-size:0.6rem;font-weight:700;letter-spacing:0.38em;color:var(--gold);text-transform:uppercase;margin-bottom:1.2rem;display:flex;align-items:center;gap:8px;}
.g-card-title::after{content:'';flex:1;height:1px;background:var(--border);}
.result-panel{background:linear-gradient(135deg,rgba(200,168,75,0.10),rgba(200,168,75,0.03));border:1px solid var(--gold);border-radius:3px;padding:2rem 2.2rem 1.8rem;text-align:center;position:relative;overflow:hidden;margin-bottom:1.2rem;}
.result-panel::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--gold-lt),transparent);}
.result-panel::after{content:'';position:absolute;top:-60px;right:-60px;width:160px;height:160px;background:radial-gradient(circle,rgba(200,168,75,0.12),transparent 65%);pointer-events:none;}
.rp-tag{font-family:'Rajdhani',sans-serif;font-size:0.58rem;font-weight:700;letter-spacing:0.4em;color:var(--gold);text-transform:uppercase;margin-bottom:0.5rem;}
.rp-price{font-family:'Rajdhani',sans-serif;font-size:3.4rem;font-weight:700;color:var(--gold-lt);line-height:1;letter-spacing:0.03em;}
.rp-range{font-size:0.78rem;color:var(--muted);margin-top:0.5rem;letter-spacing:0.08em;}
.rp-range b{color:var(--gold);font-weight:600;}
.stat-row{display:flex;gap:10px;margin:1rem 0;}
.stat-chip{flex:1;background:rgba(10,12,18,0.8);border:1px solid var(--border);border-radius:3px;padding:10px 8px;text-align:center;}
.stat-chip .sc-label{font-size:0.58rem;font-weight:700;letter-spacing:0.22em;color:var(--muted);text-transform:uppercase;display:block;margin-bottom:3px;}
.stat-chip .sc-val{font-family:'Rajdhani',sans-serif;font-size:1.15rem;font-weight:700;color:var(--text);}
.sec-label{font-family:'Rajdhani',sans-serif;font-size:0.6rem;font-weight:700;letter-spacing:0.3em;color:var(--gold);text-transform:uppercase;display:flex;align-items:center;gap:8px;margin:1.2rem 0 0.5rem;}
.sec-label::after{content:'';flex:1;height:1px;background:var(--border);}
.placeholder{text-align:center;padding:5rem 2rem;color:var(--muted);}
.placeholder .ico{font-size:3.5rem;opacity:0.3;display:block;margin-bottom:1rem;}
.placeholder p{font-size:0.85rem;letter-spacing:0.1em;line-height:1.7;}
.placeholder b{color:var(--gold);}
.vs-price-card{border-radius:3px;padding:1.5rem;text-align:center;position:relative;overflow:hidden;}
.vpc-a{background:rgba(64,128,224,0.08);border:1px solid rgba(64,128,224,0.4);}
.vpc-b{background:rgba(224,128,40,0.08);border:1px solid rgba(224,128,80,0.4);}
.vpc-tag{font-size:0.6rem;letter-spacing:0.3em;font-weight:700;margin-bottom:4px;text-transform:uppercase;}
.vpc-a .vpc-tag{color:#6ea8f8;}.vpc-b .vpc-tag{color:#f8a06e;}
.vpc-price{font-family:'Rajdhani',sans-serif;font-size:2.2rem;font-weight:700;line-height:1;}
.vpc-a .vpc-price{color:#8ec8ff;}.vpc-b .vpc-price{color:#ffc88e;}
.vpc-sub{font-size:0.72rem;color:var(--muted);margin-top:5px;}
.vs-divider{display:flex;align-items:center;justify-content:center;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.2rem;color:var(--muted);letter-spacing:0.1em;}
.winner-strip{background:var(--gold-dim);border:1px solid var(--border-hi);border-radius:3px;padding:0.9rem 1.5rem;text-align:center;font-family:'Rajdhani',sans-serif;font-size:0.78rem;font-weight:700;letter-spacing:0.2em;color:var(--gold-lt);text-transform:uppercase;margin:0.8rem 0 1.2rem;}
div[data-testid="stSelectbox"] label,div[data-testid="stNumberInput"] label,div[data-testid="stSlider"] label{font-size:0.65rem!important;font-weight:600!important;letter-spacing:0.18em!important;color:var(--muted)!important;text-transform:uppercase!important;font-family:'Exo 2',sans-serif!important;}
div[data-baseweb="select"]>div{background:rgba(8,10,14,0.95)!important;border-color:var(--border)!important;border-radius:3px!important;color:var(--text)!important;}
div[data-baseweb="select"]>div:hover{border-color:var(--gold)!important;}
input[type="number"]{background:rgba(8,10,14,0.95)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:3px!important;}
div[data-testid="stButton"]>button{background:linear-gradient(135deg,#c8a84b 0%,#7a5a18 100%)!important;color:#05060a!important;border:none!important;border-radius:2px!important;font-family:'Rajdhani',sans-serif!important;font-weight:700!important;font-size:0.78rem!important;letter-spacing:0.32em!important;text-transform:uppercase!important;padding:0.65rem 0!important;width:100%!important;clip-path:polygon(12px 0%,100% 0%,calc(100% - 12px) 100%,0% 100%)!important;transition:all 0.18s ease!important;}
div[data-testid="stButton"]>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 28px var(--gold-glow)!important;filter:brightness(1.1)!important;}
div[data-testid="stButton"]>button:active{transform:translateY(0px)!important;}
div[data-testid="stTabs"] [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid var(--border)!important;gap:2px!important;margin-bottom:1.2rem!important;}
div[data-testid="stTabs"] [data-baseweb="tab"]{font-family:'Rajdhani',sans-serif!important;font-weight:600!important;font-size:0.72rem!important;letter-spacing:0.28em!important;text-transform:uppercase!important;color:var(--muted)!important;padding:0.7rem 1.6rem!important;background:transparent!important;border:none!important;border-bottom:2px solid transparent!important;margin-bottom:-1px!important;transition:all 0.15s!important;}
div[data-testid="stTabs"] [aria-selected="true"]{color:var(--gold)!important;border-bottom-color:var(--gold)!important;background:var(--gold-dim)!important;}
div[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:3px!important;}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0.6rem 0 0.8rem;}
.info-item{background:rgba(10,12,18,0.85);border:1px solid var(--border);border-radius:3px;padding:12px 14px;position:relative;overflow:hidden;transition:border-color 0.2s;}
.info-item:hover{border-color:var(--gold);}
.ii-icon{font-size:1.2rem;margin-bottom:4px;}
.ii-label{font-size:0.58rem;font-weight:700;letter-spacing:0.2em;color:var(--muted);text-transform:uppercase;}
.ii-val{font-family:'Rajdhani',sans-serif;font-size:1.35rem;font-weight:700;color:var(--gold-lt);line-height:1.1;margin:3px 0 2px;}
.ii-note{font-size:0.62rem;color:#3a4252;letter-spacing:0.08em;font-style:italic;}
.total-cost-bar{background:linear-gradient(90deg,rgba(200,168,75,0.12),rgba(200,168,75,0.04));border:1px solid var(--border-hi);border-radius:3px;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;}
.tcb-label{font-family:'Rajdhani',sans-serif;font-size:0.6rem;font-weight:700;letter-spacing:0.28em;color:var(--gold);text-transform:uppercase;}
.tcb-val{font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;color:var(--gold-lt);}
.luxury-footer{text-align:center;padding:2.5rem 0 1rem;border-top:1px solid var(--border);margin-top:3rem;font-size:0.65rem;letter-spacing:0.25em;color:var(--muted);text-transform:uppercase;font-family:'Rajdhani',sans-serif;}
.luxury-footer span{color:var(--border);}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_artifacts():
    model       = joblib.load("AutoPricePro.pkl")
    brand_model = joblib.load("brand_model_map.pkl")
    meta        = joblib.load("meta.pkl")
    return model, brand_model, meta

@st.cache_data
def load_year_ranges():
    try:
        df = pd.read_csv("car data.csv")
        df.columns = df.columns.str.lower().str.strip()
        year_col  = next((c for c in df.columns if "year" in c), None)
        name_col  = next((c for c in df.columns if c in ("name","car_name","car name")), None)
        brand_col = next((c for c in df.columns if c == "brand"), None)
        model_col = next((c for c in df.columns if c == "model"), None)
        if year_col is None:
            return {}
        ranges = {}
        if brand_col and model_col:
            for (brand, model), grp in df.groupby([brand_col, model_col]):
                ranges[(str(brand).strip(), str(model).strip())] = (int(grp[year_col].min()), 2026)
        elif name_col:
            df["_brand"] = df[name_col].str.split().str[0].str.strip()
            df["_model"] = df[name_col].str.split().str[1:].str.join(" ").str.strip()
            for (brand, model), grp in df.groupby(["_brand","_model"]):
                ranges[(str(brand).strip(), str(model).strip())] = (int(grp[year_col].min()), 2026)
        return ranges
    except Exception:
        return {}

model, brand_model_map, meta = load_artifacts()
year_ranges = load_year_ranges()

fuels         = meta["fuel_types"]
transmissions = meta["transmission_types"]
seller_types  = meta["seller_types"]
owners        = meta["owner_types"]
year_min      = meta["year_min"]
year_max      = meta["year_max"]
km_max        = meta["km_max"]
brands        = sorted(brand_model_map.keys())

def get_year_range(brand, model):
    key = (brand.strip(), model.strip())
    if key in year_ranges:
        return year_ranges[key][0], 2026
    brand_keys = [k for k in year_ranges if k[0] == brand.strip()]
    if brand_keys:
        return min(year_ranges[k][0] for k in brand_keys), 2026
    return year_min, 2026

def build_input(brand, mdl, year, km, fuel, transmission, seller_type, owner):
    return pd.DataFrame([{
        "brand": brand, "model": mdl, "age": 2026 - year,
        "km_log": np.log1p(km), "fuel": fuel,
        "seller_type": seller_type, "transmission": transmission, "owner": owner,
    }])

def predict_price(df_row):
    return max(model.predict(df_row)[0], 0)

def fmt_inr(val):
    lakh = val / 1e5
    return f"₹{lakh/100:.2f} Cr" if lakh >= 100 else f"₹{lakh:.2f} L"

def depreciation_series(brand, mdl, base_year, km, fuel, transmission, seller_type, owner):
    years, prices = [], []
    for yr in range(base_year, 2027):
        km_est = km * (yr - base_year + 1) / max((2026 - base_year), 1)
        row = build_input(brand, mdl, yr, km_est, fuel, transmission, seller_type, owner)
        years.append(yr)
        prices.append(predict_price(row))
    return years, prices

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#5a6070", family="Exo 2, sans-serif", size=11),
    margin=dict(l=0, r=0, t=14, b=0), height=230,
)

st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">◈ &nbsp;AI Valuation Engine&nbsp; ◈</div>
  <div class="hero-title">AUTOPRICEPRO</div>
  <div class="hero-sub">Precision Used Car Valuation &nbsp;·&nbsp; XGBoost ML &nbsp;·&nbsp; R² 95.46%</div>
  <div class="hero-rule"></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["◈  SINGLE VALUATION", "⬡  COMPARE TWO CARS"])

with tab1:
    col_form, col_result = st.columns([1, 1.25], gap="large")

    with col_form:
        st.markdown('<div class="g-card"><div class="g-card-title">Vehicle Specification</div>', unsafe_allow_html=True)

        sel_brand   = st.selectbox("Brand", brands, key="s_brand")
        models_list = brand_model_map.get(sel_brand, [])
        sel_model   = st.selectbox("Model", models_list, key="s_model")

        mdl_yr_min, mdl_yr_max = get_year_range(sel_brand, sel_model)
        mdl_default = min(max(mdl_yr_max - 3, mdl_yr_min), mdl_yr_max)

        c1, c2 = st.columns(2)
        with c1:
            sel_year = st.slider("Purchase Year", min_value=mdl_yr_min, max_value=mdl_yr_max, value=mdl_default, key="s_year")
        with c2:
            sel_km = st.number_input("KM Driven", min_value=0, max_value=km_max, value=13000, step=1, key="s_km")

        c3, c4 = st.columns(2)
        with c3:
            sel_fuel  = st.selectbox("Fuel Type", fuels, key="s_fuel")
        with c4:
            sel_trans = st.selectbox("Transmission", transmissions, key="s_trans")

        c5, c6 = st.columns(2)
        with c5:
            sel_seller = st.selectbox("Seller Type", seller_types, key="s_seller")
        with c6:
            sel_owner = st.selectbox("Owner", owners, key="s_owner")

        st.markdown("</div>", unsafe_allow_html=True)
        predict_btn = st.button("PREDICT MARKET VALUE", key="s_btn")

    with col_result:
        if predict_btn:
            row   = build_input(sel_brand, sel_model, sel_year, sel_km, sel_fuel, sel_trans, sel_seller, sel_owner)
            price = predict_price(row)
            low, high = price * 0.92, price * 1.08
            age   = 2026 - sel_year

            st.markdown(f"""
            <div class="result-panel">
              <div class="rp-tag">Estimated Market Value</div>
              <div class="rp-price">{fmt_inr(price)}</div>
              <div class="rp-range">Confidence Range &nbsp;·&nbsp; <b>{fmt_inr(low)}</b> — <b>{fmt_inr(high)}</b></div>
            </div>
            <div class="stat-row">
              <div class="stat-chip"><span class="sc-label">Age</span><span class="sc-val">{age} yrs</span></div>
              <div class="stat-chip"><span class="sc-label">KM Driven</span><span class="sc-val">{sel_km:,}</span></div>
              <div class="stat-chip"><span class="sc-label">Fuel</span><span class="sc-val">{sel_fuel}</span></div>
              <div class="stat-chip"><span class="sc-label">Trans.</span><span class="sc-val">{sel_trans[:4]}</span></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="sec-label">Ownership Cost Breakdown</div>', unsafe_allow_html=True)

            insurance   = round(price * 0.035 / 1e5, 2)
            maintenance = 18000 if sel_fuel == "Diesel" else 12000
            fuel_cost   = round((sel_km / 15) * (106 if sel_fuel == "Petrol" else 92 if sel_fuel == "Diesel" else 75) / 1e5, 2)
            rto_tax     = round(price * 0.02 / 1e5, 2)
            total_yearly = round(insurance + maintenance/1e5 + fuel_cost + rto_tax, 2)

            st.markdown(f"""
            <div class="info-grid">
              <div class="info-item">
                <div class="ii-icon">🛡️</div>
                <div class="ii-label">Insurance / yr</div>
                <div class="ii-val">₹{insurance:.2f} L</div>
                <div class="ii-note">~3.5% of market value</div>
              </div>
              <div class="info-item">
                <div class="ii-icon">🔧</div>
                <div class="ii-label">Maintenance / yr</div>
                <div class="ii-val">₹{maintenance/1e5:.2f} L</div>
                <div class="ii-note">{"Diesel service est." if sel_fuel == "Diesel" else "Petrol service est."}</div>
              </div>
              <div class="info-item">
                <div class="ii-icon">⛽</div>
                <div class="ii-label">Fuel Cost / yr</div>
                <div class="ii-val">₹{fuel_cost:.2f} L</div>
                <div class="ii-note">{sel_km:,} km @ avg mileage</div>
              </div>
              <div class="info-item">
                <div class="ii-icon">📋</div>
                <div class="ii-label">Road Tax / yr</div>
                <div class="ii-val">₹{rto_tax:.2f} L</div>
                <div class="ii-note">~2% of market value</div>
              </div>
            </div>
            <div class="total-cost-bar">
              <span class="tcb-label">TOTAL ESTIMATED ANNUAL COST</span>
              <span class="tcb-val">₹{total_yearly:.2f} L / year</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="sec-label">Price vs Similar Cars in Market</div>', unsafe_allow_html=True)

            similar_configs = [
                ("Older · +3 yrs", sel_year - 3, sel_km + 30000),
                ("Older · +1 yr",  sel_year - 1, sel_km + 10000),
                ("This Car",       sel_year,      sel_km),
                ("Newer · -1 yr",  sel_year + 1,  max(sel_km - 10000, 0)),
                ("Newer · -3 yrs", sel_year + 3,  max(sel_km - 30000, 0)),
            ]

            mdl_yr_min_s, mdl_yr_max_s = get_year_range(sel_brand, sel_model)
            sim_labels, sim_prices, sim_kms, sim_years, sim_colors = [], [], [], [], []
            for label, yr, km_s in similar_configs:
                yr_c = max(min(yr, mdl_yr_max_s), mdl_yr_min_s)
                km_c = max(km_s, 0)
                r    = build_input(sel_brand, sel_model, yr_c, km_c, sel_fuel, sel_trans, sel_seller, sel_owner)
                p    = predict_price(r)
                sim_labels.append(label)
                sim_prices.append(round(p / 1e5, 2))
                sim_kms.append(f"{km_c:,} km")
                sim_years.append(yr_c)
                sim_colors.append("#c8a84b" if label == "This Car" else "#3a4560")

            fig_sim = go.Figure()
            fig_sim.add_trace(go.Bar(
                x=sim_labels, y=sim_prices,
                marker_color=sim_colors,
                marker_line_color=["#e5c96b" if l == "This Car" else "#556080" for l in sim_labels],
                marker_line_width=1.5,
                text=[f"₹{p:.1f}L" for p in sim_prices],
                textposition="outside",
                textfont=dict(color="#a0a8b8", size=11, family="Rajdhani"),
                customdata=list(zip(sim_years, sim_kms)),
                hovertemplate="<b>%{x}</b><br>Year: %{customdata[0]}<br>KM: %{customdata[1]}<br>Price: ₹%{y:.2f} L<extra></extra>",
            ))
            sim_layout = dict(PLOT_LAYOUT)
            sim_layout["height"] = 260
            sim_layout["yaxis"] = dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.06)", zeroline=False)
            sim_layout["xaxis"] = dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10, color="#6a7080"))
            sim_layout["bargap"] = 0.35
            fig_sim.update_layout(**sim_layout)
            st.plotly_chart(fig_sim, use_container_width=True)
            st.markdown(
                '<div style="font-size:0.6rem;color:#404858;letter-spacing:0.12em;text-align:center;margin-top:-10px;">'
                'Same model · same fuel · varying year & mileage</div>',
                unsafe_allow_html=True
            )

        else:
            st.markdown("""
            <div class="placeholder">
              <span class="ico">◈</span>
              <p>Configure vehicle specifications<br>and press<br>
              <b>PREDICT MARKET VALUE</b></p>
            </div>
            """, unsafe_allow_html=True)


with tab2:
    cc1, cc2 = st.columns(2, gap="large")

    def car_form(col, idx):
        color_label = "CAR A — BLUE" if idx == 1 else "CAR B — AMBER"
        with col:
            st.markdown(f'<div class="g-card"><div class="g-card-title">{color_label}</div>', unsafe_allow_html=True)
            brand    = st.selectbox("Brand", brands, key=f"c{idx}_brand")
            mdl_list = brand_model_map.get(brand, [])
            mdl      = st.selectbox("Model", mdl_list, key=f"c{idx}_model")
            c_yr_min, c_yr_max = get_year_range(brand, mdl)
            c_default = min(max(c_yr_max - 3, c_yr_min), c_yr_max)
            yr       = st.slider("Purchase Year", min_value=c_yr_min, max_value=c_yr_max, value=c_default, key=f"c{idx}_year")
            km       = st.number_input("KM Driven", min_value=0, max_value=km_max, value=13000, step=1, key=f"c{idx}_km")
            fuel     = st.selectbox("Fuel Type", fuels, key=f"c{idx}_fuel")
            trans    = st.selectbox("Transmission", transmissions, key=f"c{idx}_trans")
            seller   = st.selectbox("Seller Type", seller_types, key=f"c{idx}_seller")
            owner    = st.selectbox("Owner", owners, key=f"c{idx}_owner")
            st.markdown("</div>", unsafe_allow_html=True)
        return brand, mdl, yr, km, fuel, trans, seller, owner

    data_a = car_form(cc1, 1)
    data_b = car_form(cc2, 2)

    compare_btn = st.button("RUN COMPARISON ANALYSIS", key="cmp_btn")

    if compare_btn:
        brand_a, mdl_a, yr_a, km_a, fuel_a, trans_a, seller_a, owner_a = data_a
        brand_b, mdl_b, yr_b, km_b, fuel_b, trans_b, seller_b, owner_b = data_b

        row_a   = build_input(brand_a, mdl_a, yr_a, km_a, fuel_a, trans_a, seller_a, owner_a)
        row_b   = build_input(brand_b, mdl_b, yr_b, km_b, fuel_b, trans_b, seller_b, owner_b)
        price_a = predict_price(row_a)
        price_b = predict_price(row_b)
        winner  = f"CAR A  ({brand_a} {mdl_a})" if price_a >= price_b else f"CAR B  ({brand_b} {mdl_b})"
        diff    = abs(price_a - price_b)

        r1, r2, r3 = st.columns([1, 0.18, 1])
        with r1:
            st.markdown(f"""
            <div class="vs-price-card vpc-a">
              <div class="vpc-tag">Car A · {brand_a} {mdl_a}</div>
              <div class="vpc-price">{fmt_inr(price_a)}</div>
              <div class="vpc-sub">{yr_a} &nbsp;·&nbsp; {km_a:,} km &nbsp;·&nbsp; {fuel_a}</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="vs-divider" style="height:100%;padding-top:1rem;">VS</div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class="vs-price-card vpc-b">
              <div class="vpc-tag">Car B · {brand_b} {mdl_b}</div>
              <div class="vpc-price">{fmt_inr(price_b)}</div>
              <div class="vpc-sub">{yr_b} &nbsp;·&nbsp; {km_b:,} km &nbsp;·&nbsp; {fuel_b}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="winner-strip">
            ◈ &nbsp; Higher Value: &nbsp; {winner} &nbsp; · &nbsp; Difference: {fmt_inr(diff)} &nbsp; ◈
        </div>
        """, unsafe_allow_html=True)

        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown('<div class="sec-label">Price Comparison</div>', unsafe_allow_html=True)
            fig_bar = go.Figure(go.Bar(
                x=[f"{brand_a} {mdl_a}", f"{brand_b} {mdl_b}"],
                y=[price_a / 1e5, price_b / 1e5],
                marker_color=["#4080e0", "#e08040"],
                marker_line_color=["#6ea8f8", "#f8a06e"],
                marker_line_width=1,
                text=[fmt_inr(price_a), fmt_inr(price_b)],
                textposition="outside",
                textfont=dict(color="#c8a84b", size=12, family="Rajdhani"),
            ))
            fig_bar.update_layout(
                **dict(PLOT_LAYOUT, height=280, yaxis=dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.07)", zeroline=False), xaxis=dict(gridcolor="rgba(0,0,0,0)")),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with ch2:
            st.markdown('<div class="sec-label">Depreciation Comparison</div>', unsafe_allow_html=True)
            yrs_a, dep_a = depreciation_series(brand_a, mdl_a, max(yr_a, 2010), km_a, fuel_a, trans_a, seller_a, owner_a)
            yrs_b, dep_b = depreciation_series(brand_b, mdl_b, max(yr_b, 2010), km_b, fuel_b, trans_b, seller_b, owner_b)

            fig_dep2 = go.Figure()
            fig_dep2.add_trace(go.Scatter(
                x=yrs_a, y=[p/1e5 for p in dep_a], name=f"{brand_a} {mdl_a}",
                line=dict(color="#4080e0", width=2.5), mode="lines+markers", marker=dict(size=4),
            ))
            fig_dep2.add_trace(go.Scatter(
                x=yrs_b, y=[p/1e5 for p in dep_b], name=f"{brand_b} {mdl_b}",
                line=dict(color="#e08040", width=2.5), mode="lines+markers", marker=dict(size=4),
            ))
            dep_layout = dict(PLOT_LAYOUT)
            dep_layout["height"] = 280
            dep_layout["xaxis"] = dict(title="Year", gridcolor="rgba(200,168,75,0.07)", zeroline=False)
            dep_layout["yaxis"] = dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.07)", zeroline=False)
            dep_layout["legend"] = dict(bgcolor="rgba(8,10,14,0.8)", bordercolor="rgba(200,168,75,0.2)", borderwidth=1, font=dict(color="#a0a8b8", size=10))
            fig_dep2.update_layout(**dep_layout)
            st.plotly_chart(fig_dep2, use_container_width=True)

        st.markdown('<div class="sec-label">Specifications</div>', unsafe_allow_html=True)
        specs_df = pd.DataFrame({
            "Specification":     ["Brand","Model","Year","KM Driven","Fuel","Transmission","Seller","Owner","Est. Price"],
            f"Car A  {brand_a}": [brand_a, mdl_a, yr_a, f"{km_a:,} km", fuel_a, trans_a, seller_a, owner_a, fmt_inr(price_a)],
            f"Car B  {brand_b}": [brand_b, mdl_b, yr_b, f"{km_b:,} km", fuel_b, trans_b, seller_b, owner_b, fmt_inr(price_b)],
        })
        st.dataframe(specs_df.set_index("Specification"), use_container_width=True)

st.markdown("""
<div class="luxury-footer">
    AutoPricePro &nbsp;·&nbsp; XGBoost ML Engine &nbsp;·&nbsp; R² 95.46%
    &nbsp;<span>|</span>&nbsp;
    Predictions are estimates — verify before transacting
</div>
""", unsafe_allow_html=True)