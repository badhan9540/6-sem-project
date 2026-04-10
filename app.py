import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os, json, hashlib, warnings
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WorkloadAI – Pattern Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #030712;
    font-family: 'Outfit', sans-serif;
    color: #cbd5e1;
    overflow-x: hidden;
}

/* ── ANIMATED PARTICLE BACKGROUND ── */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 10%, rgba(108,99,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 90%, rgba(0,212,255,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(16,185,129,0.04) 0%, transparent 65%);
    pointer-events: none; z-index: 0;
    animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%   { opacity: 0.7; }
    100% { opacity: 1; }
}

/* ── CYBER GRID ── */
.stApp::after {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(108,99,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108,99,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none; z-index: 0;
    animation: gridMove 20s linear infinite;
}
@keyframes gridMove { 0%{background-position:0 0} 100%{background-position:60px 60px} }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050b18 0%, #070d1e 100%) !important;
    border-right: 1px solid rgba(108,99,255,0.2) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.6), inset -1px 0 0 rgba(108,99,255,0.1);
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] strong { color: #e0f2fe !important; }

/* ── 3D HERO CARD ── */
.hero-container {
    background: linear-gradient(135deg,
        rgba(108,99,255,0.15) 0%,
        rgba(0,212,255,0.08) 50%,
        rgba(16,185,129,0.06) 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 24px;
    padding: 44px 52px;
    margin-bottom: 32px;
    position: relative; overflow: hidden;
    transform: perspective(1200px) rotateX(1.5deg);
    box-shadow:
        0 25px 70px rgba(0,0,0,0.6),
        0 0 0 1px rgba(108,99,255,0.1),
        inset 0 1px 0 rgba(255,255,255,0.06),
        0 0 80px rgba(108,99,255,0.05);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}
.hero-container::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.8), rgba(0,212,255,0.6), transparent);
}
.hero-container::after {
    content: '';
    position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.06), transparent);
    animation: heroShimmer 5s ease-in-out infinite;
}
@keyframes heroShimmer { 0%{left:-100%} 100%{left:200%} }
.hero-container:hover {
    transform: perspective(1200px) rotateX(0deg) translateY(-3px);
    box-shadow: 0 35px 90px rgba(0,0,0,0.7), 0 0 60px rgba(108,99,255,0.12);
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.8rem; font-weight: 700;
    background: linear-gradient(135deg, #a78bfa 0%, #6c63ff 30%, #00d4ff 70%, #7dd3fc 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 10px 0;
    letter-spacing: 2px; text-transform: uppercase;
    filter: drop-shadow(0 0 20px rgba(108,99,255,0.3));
}
.hero-sub { color: #94a3b8; font-size: 0.95rem; margin: 0; letter-spacing: 0.5px; }

/* ── 3D METRIC CARDS ── */
.metric-card {
    background: linear-gradient(145deg, rgba(10,16,30,0.95), rgba(6,10,20,0.98));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 28px 20px; text-align: center;
    position: relative; overflow: hidden;
    transform: perspective(600px) rotateX(3deg) rotateY(0deg);
    box-shadow:
        0 15px 50px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.04);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: default;
    animation: cardFloat 0.5s ease both;
}
@keyframes cardFloat {
    from { opacity: 0; transform: perspective(600px) rotateX(3deg) translateY(20px); }
    to   { opacity: 1; transform: perspective(600px) rotateX(3deg) translateY(0); }
}
.metric-card:nth-child(1) { animation-delay: 0.05s; }
.metric-card:nth-child(2) { animation-delay: 0.10s; }
.metric-card:nth-child(3) { animation-delay: 0.15s; }
.metric-card:nth-child(4) { animation-delay: 0.20s; }
.metric-card:hover {
    transform: perspective(600px) rotateX(0deg) translateY(-8px) scale(1.03);
    box-shadow: 0 30px 70px rgba(0,0,0,0.6), 0 0 40px rgba(108,99,255,0.1);
    border-color: rgba(108,99,255,0.25);
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 18px 18px 0 0;
}
.metric-card::after {
    content: '';
    position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
    transition: left 0.6s ease;
}
.metric-card:hover::after { left: 150%; }
.metric-card.purple::before { background: linear-gradient(90deg,#6c63ff,#a78bfa); box-shadow: 0 0 15px #6c63ff88; }
.metric-card.cyan::before   { background: linear-gradient(90deg,#00d4ff,#67e8f9); box-shadow: 0 0 15px #00d4ff88; }
.metric-card.amber::before  { background: linear-gradient(90deg,#f59e0b,#fcd34d); box-shadow: 0 0 15px #f59e0b88; }
.metric-card.green::before  { background: linear-gradient(90deg,#10b981,#6ee7b7); box-shadow: 0 0 15px #10b98188; }
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.8rem; font-weight: 700; letter-spacing: 1px;
    text-shadow: 0 0 30px currentColor;
    animation: valueGlow 3s ease-in-out infinite alternate;
}
@keyframes valueGlow { 0%{filter:brightness(1)} 100%{filter:brightness(1.2)} }
.metric-label { color: #64748b; font-size: 0.72rem; margin-top: 8px; text-transform: uppercase; letter-spacing: 2.5px; }

/* ── STATUS BADGE ── */
.status-badge {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 10px 22px; border-radius: 8px;
    font-weight: 700; font-size: 0.9rem;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1.5px; text-transform: uppercase;
    backdrop-filter: blur(12px);
    position: relative; overflow: hidden;
}
.status-badge::after {
    content: '';
    position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    animation: badgeShimmer 3s ease-in-out infinite;
}
@keyframes badgeShimmer { 0%{left:-100%} 100%{left:200%} }
.status-dot {
    width: 9px; height: 9px; border-radius: 50%;
    animation: dotPulse 2s ease-in-out infinite;
    display: inline-block; flex-shrink: 0;
}
@keyframes dotPulse {
    0%,100% { transform: scale(1); box-shadow: 0 0 0 0 currentColor; }
    50% { transform: scale(1.3); box-shadow: 0 0 0 4px transparent; }
}
.status-low    { background: rgba(16,185,129,0.1); color: #34d399; border: 1px solid rgba(16,185,129,0.35); box-shadow: 0 0 25px rgba(16,185,129,0.12), inset 0 1px 0 rgba(16,185,129,0.1); }
.status-medium { background: rgba(245,158,11,0.1); color: #fbbf24; border: 1px solid rgba(245,158,11,0.35); box-shadow: 0 0 25px rgba(245,158,11,0.12), inset 0 1px 0 rgba(245,158,11,0.1); }
.status-high   { background: rgba(239,68,68,0.1);  color: #f87171; border: 1px solid rgba(239,68,68,0.35);  box-shadow: 0 0 25px rgba(239,68,68,0.12),  inset 0 1px 0 rgba(239,68,68,0.1); }
.status-low .status-dot    { background: #34d399; box-shadow: 0 0 8px #34d399; }
.status-medium .status-dot { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }
.status-high .status-dot   { background: #f87171; box-shadow: 0 0 8px #f87171; }

/* ── SECTION TITLES ── */
.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.25rem; font-weight: 700;
    margin: 34px 0 18px;
    display: flex; align-items: center; gap: 12px;
    color: #e2e8f0; letter-spacing: 2px; text-transform: uppercase;
    position: relative;
}
.section-title::before {
    content: '';
    width: 3px; height: 22px;
    background: linear-gradient(180deg, #6c63ff, #00d4ff);
    border-radius: 2px;
    box-shadow: 0 0 12px rgba(108,99,255,0.7), 0 0 24px rgba(0,212,255,0.3);
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(108,99,255,0.4), rgba(0,212,255,0.2), transparent);
}

/* ── GUIDANCE CARDS ── */
.guidance-card {
    background: linear-gradient(135deg, rgba(8,15,35,0.9), rgba(5,10,25,0.95));
    border: 1px solid rgba(108,99,255,0.15);
    border-radius: 14px;
    padding: 18px 22px; margin: 10px 0;
    border-left: 3px solid #6c63ff;
    position: relative; overflow: hidden;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    animation: slideIn 0.4s ease both;
}
@keyframes slideIn { from{opacity:0;transform:translateX(-16px)} to{opacity:1;transform:translateX(0)} }
.guidance-card:nth-child(1){animation-delay:0.05s}
.guidance-card:nth-child(2){animation-delay:0.10s}
.guidance-card:nth-child(3){animation-delay:0.15s}
.guidance-card:nth-child(4){animation-delay:0.20s}
.guidance-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(108,99,255,0.04), transparent);
    pointer-events: none;
}
.guidance-card:hover {
    transform: translateX(6px);
    border-left-color: #00d4ff;
    border-color: rgba(108,99,255,0.3);
    box-shadow: 0 8px 35px rgba(0,0,0,0.5), -4px 0 25px rgba(108,99,255,0.12);
}

/* ── INFO BOX ── */
.info-box {
    background: rgba(8,15,35,0.7);
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 10px; padding: 14px 18px;
    color: #64748b; font-size: 0.87rem; line-height: 1.8; margin: 8px 0;
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(108,99,255,0.2);
}

/* ── PROGRESS BARS ── */
.prog-bg  { background: rgba(255,255,255,0.04); border-radius: 999px; height: 6px; overflow: hidden; }
.prog-bar { height: 100%; border-radius: 999px; transition: width 1s cubic-bezier(0.4,0,0.2,1); position: relative; overflow: hidden; }
.prog-bar::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.4) 50%, transparent 100%);
    animation: progShimmer 2s ease-in-out infinite;
}
@keyframes progShimmer { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #6c63ff 40%, #00d4ff 100%) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 14px 32px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important; font-size: 1.05rem !important;
    letter-spacing: 2.5px !important; text-transform: uppercase !important;
    box-shadow: 0 4px 25px rgba(108,99,255,0.4), 0 0 0 1px rgba(108,99,255,0.3) !important;
    transition: all 0.3s ease !important;
    position: relative; overflow: hidden;
}
.stButton > button:hover {
    box-shadow: 0 8px 40px rgba(108,99,255,0.6), 0 0 30px rgba(0,212,255,0.3) !important;
    transform: translateY(-3px) scale(1.01) !important;
}
.stButton > button:active { transform: translateY(-1px) !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input {
    background: rgba(8,15,35,0.85) !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important; color: #e0f2fe !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(108,99,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.12), 0 0 20px rgba(108,99,255,0.1) !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: rgba(8,15,35,0.85) !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important; color: #e0f2fe !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(5,10,22,0.9) !important;
    border-radius: 12px; padding: 5px; gap: 3px;
    border: 1px solid rgba(108,99,255,0.15);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important; color: #334155 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important; letter-spacing: 0.5px !important;
    transition: all 0.25s ease !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #6c63ff !important; background: rgba(108,99,255,0.06) !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(108,99,255,0.25), rgba(0,212,255,0.12)) !important;
    color: #a78bfa !important;
    border: 1px solid rgba(108,99,255,0.35) !important;
    box-shadow: 0 0 20px rgba(108,99,255,0.12), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}

/* ── ALERTS ── */
.stSuccess { background: rgba(16,185,129,0.08) !important; border: 1px solid rgba(16,185,129,0.2) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(108,99,255,0.08) !important; border: 1px solid rgba(108,99,255,0.2) !important; border-radius: 10px !important; }
.stError   { background: rgba(239,68,68,0.08)  !important; border: 1px solid rgba(239,68,68,0.2)  !important; border-radius: 10px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #030712; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #6c63ff, #00d4ff); border-radius: 3px; }

/* ── WEEKLY DAY CARDS ── */
.day-card {
    background: rgba(8,15,30,0.9);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 16px 8px; text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.day-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.4); }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
THRESHOLD  = 1.0  # score is 0-1 scale
USERS_FILE = "users_db.json"
FEATURES   = [
    "Sleep Duration","Quality of Sleep","Physical Activity Level",
    "Heart Rate","Daily Steps","work_hours_per_day",
    "screen_time_before_sleep","breaks_during_work","Daily_Screen_Time(hrs)"
]
FEAT_META = {
    "Sleep Duration":           ("😴 Sleep Duration",      "#6c63ff"),
    "Quality of Sleep":         ("🌙 Sleep Quality",       "#8b5cf6"),
    "Physical Activity Level":  ("🏃 Physical Activity",   "#10b981"),
    "Heart Rate":               ("❤️ Heart Rate",           "#ef4444"),
    "Daily Steps":              ("👣 Daily Steps",          "#f59e0b"),
    "work_hours_per_day":       ("💼 Work Hours/Day",       "#e11d48"),
    "screen_time_before_sleep": ("📱 Screen Before Sleep", "#f97316"),
    "breaks_during_work":       ("☕ Breaks During Work",   "#06b6d4"),
    "Daily_Screen_Time(hrs)":   ("🖥️ Daily Screen Time",   "#64748b"),
}
FEAT_EASY = {f: FEAT_META[f][0] for f in FEATURES}
COLOR_MAP = {"Balanced":"#10b981","Moderate":"#f59e0b","Overloaded":"#ef4444"}

# ─── USER DB ──────────────────────────────────────────────────────────────────
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    return {}

def save_users(u):
    with open(USERS_FILE,"w") as f:
        json.dump(u, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, name):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    users[username] = {"name":name,"password":hash_pw(password),"history":[]}
    save_users(users)
    return True, "Account created! Please login."

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found!"
    if users[username]["password"] != hash_pw(password):
        return False, "Wrong password!"
    return True, users[username]["name"]

def save_history(username, history):
    users = load_users()
    if username in users:
        users[username]["history"] = history
        save_users(users)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
for k,v in [("logged_in",False),("username",""),("user_name",""),("history",[])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def classify(score):
    if score < 0.15:   return "Balanced",  "status-low"
    elif score < 0.55: return "Moderate",  "status-medium"
    else:              return "Overloaded", "status-high"

def compute_score(row):
    """
    Score purely from 5 question answers.
    Returns 0.0 to 1.0 (0=perfect day, 1=worst day)
    Thresholds: <0.30 Balanced | 0.30-0.60 Moderate | >0.60 Overloaded
    """
    score = 0.0

    # Sleep — most important factor
    s = row.get("Sleep Duration", 0.5)
    if   s >= 8.5/12: score += 0.00
    elif s >= 7.0/12: score += 0.10
    elif s >= 5.0/12: score += 0.25
    else:             score += 0.50

    # Work hours
    w = row.get("work_hours_per_day", 0.5)
    if   w <= 5/16:  score += 0.00
    elif w <= 8/16:  score += 0.10
    elif w <= 11/16: score += 0.25
    else:            score += 0.45

    # Physical activity
    a = row.get("Physical Activity Level", 0.5)
    if   a >= 0.8:  score += 0.00
    elif a >= 0.45: score += 0.05
    elif a >= 0.15: score += 0.10
    else:           score += 0.15

    # Breaks during work
    b = row.get("breaks_during_work", 0.5)
    if   b >= 0.6:  score += 0.00
    elif b >= 0.35: score += 0.03
    elif b >= 0.15: score += 0.07
    else:           score += 0.12

    # Screen before sleep
    sc = row.get("screen_time_before_sleep", 0.5)
    if   sc <= 0:    score += 0.00
    elif sc <= 0.05: score += 0.02
    elif sc <= 0.13: score += 0.04
    else:            score += 0.07

    return round(min(score, 1.0), 3)

def try_load_model():
    try:
        import pathlib, tensorflow as tf
        base = pathlib.Path(r"C:\Users\pkarn\OneDrive\Desktop\project workload pattern")
        np_wts_path = base/"model_weights_np2.npy"
        if np_wts_path.exists():
            all_weights = np.load(str(np_wts_path), allow_pickle=True)
            # Classification model: 9 -> 64 -> 32 -> 16 -> 3
            m = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation="relu", input_shape=(9,)),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(3,  activation="softmax"),
            ])
            wi = 0
            for layer in m.layers:
                if len(layer.get_weights()) > 0 and wi < len(all_weights) and len(all_weights[wi]) > 0:
                    layer.set_weights(all_weights[wi])
                    wi += 1
            return m, None
    except Exception as e:
        print(f"Model load error: {e}")
    return None, None

def get_guidance(level):
    tips = {
        "Balanced":   [
            "✅ Great job! Your day looks healthy and well-balanced.",
            "💧 Keep drinking water and take small breaks every hour.",
            "🌿 Your sleep and work routine is on track — keep it up!",
            "📊 Log daily to track your progress over time.",
        ],
        "Moderate":   [
            "⚡ Your day seems a bit busy. Try to slow down a little.",
            "🧘 Take a 10-minute break — stretch, breathe, or go for a short walk.",
            "📋 Focus on your top 3 tasks today and leave the rest for tomorrow.",
            "🌙 Try to get 7-8 hours of sleep tonight to recover well.",
        ],
        "Overloaded": [
            "🚨 Your day looks really hectic. It's time to take a step back.",
            "🛑 Try to hand off or delay some tasks — you don't have to do everything today.",
            "🚶 Step outside for 5-10 minutes — fresh air helps clear your mind.",
            "📵 Put your phone down before bed — screen time is making it worse.",
            "💬 Talk to someone you trust about how you are feeling.",
            "📅 Plan an easier day tomorrow — your body needs recovery time.",
        ],
    }
    return tips.get(level, tips["Balanced"])

def plotly_bg():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#e2e8f0"),
    )

def weekly_insight(wdf):
    if len(wdf) == 0: return "No data for this week yet."
    avg  = wdf["score"].mean()
    over = int((wdf["label"] == "Overloaded").sum())
    mod  = int((wdf["label"] == "Moderate").sum())
    bal  = int((wdf["label"] == "Balanced").sum())
    n    = len(wdf)
    if over >= n * 0.5:
        mood = "😓 You were quite stressed this week."
        tip  = "Try to reduce your workload and get more sleep next week."
    elif bal >= n * 0.6:
        mood = "😊 You had a great week!"
        tip  = "Keep it up — your routine is working really well."
    else:
        mood = "😐 Mixed week — some balanced, some busy days."
        tip  = "Try to stay consistent — keep sleep and breaks regular."
    return (f"{mood}<br><br>📊 <b>{n} days analyzed</b> — "
            f"✅ {bal} balanced &nbsp;|&nbsp; ⚡ {mod} moderate &nbsp;|&nbsp; 🚨 {over} overloaded<br>"
            f"Average score: <b>{avg:.3f}</b><br><br>"
            f"💡 <b>Tip:</b> {tip}")

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN / REGISTER
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    _, mid, _ = st.columns([1,2,1])
    with mid:
        st.markdown("""
        <div style="text-align:center;padding:48px 0 32px;">
            <div style="font-size:4rem;filter:drop-shadow(0 0 25px rgba(108,99,255,0.9));margin-bottom:16px;
                animation:iconFloat 4s ease-in-out infinite;display:inline-block;">🧠</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:2.6rem;font-weight:700;letter-spacing:5px;
                background:linear-gradient(135deg,#a78bfa,#6c63ff,#00d4ff);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-transform:uppercase;
                filter:drop-shadow(0 0 20px rgba(108,99,255,0.4));">WorkloadAI</div>
            <div style="color:#475569;font-size:0.72rem;margin-top:8px;letter-spacing:5px;font-family:'Rajdhani',sans-serif;text-transform:uppercase;">Pattern Analysis System</div>
            <div style="width:80px;height:1px;background:linear-gradient(90deg,transparent,#6c63ff,#00d4ff,transparent);margin:14px auto 0;"></div>
            <div style="display:flex;justify-content:center;gap:8px;margin-top:12px;">
                <span style="width:5px;height:5px;border-radius:50%;background:#6c63ff;box-shadow:0 0 8px #6c63ff;display:inline-block;animation:dotPulse 2s infinite;"></span>
                <span style="width:5px;height:5px;border-radius:50%;background:#00d4ff;box-shadow:0 0 8px #00d4ff;display:inline-block;animation:dotPulse 2s infinite 0.4s;"></span>
                <span style="width:5px;height:5px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;display:inline-block;animation:dotPulse 2s infinite 0.8s;"></span>
            </div>
        </div>""", unsafe_allow_html=True)

        tl, tr = st.tabs(["🔑 Login", "✨ Register"])
        with tl:
            st.markdown("<br>", unsafe_allow_html=True)
            lu = st.text_input("👤 Username", placeholder="Enter your username", key="lu")
            lp = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="lp")
            if st.button("🚀 Login", key="btn_login"):
                if not lu or not lp:
                    st.error("Please fill in all fields!")
                else:
                    ok, res = login_user(lu, lp)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username  = lu
                        st.session_state.user_name = res
                        st.session_state.history   = load_users().get(lu,{}).get("history",[])
                        st.success(f"Welcome back, {res}! 🎉")
                        st.experimental_rerun()
                    else:
                        st.error(res)

        with tr:
            st.markdown("<br>", unsafe_allow_html=True)
            rn = st.text_input("✨ Full Name",        placeholder="Your display name",              key="rn")
            ru = st.text_input("👤 Username",         placeholder="Choose a username",               key="ru")
            rp = st.text_input("🔒 Password",         type="password", placeholder="Min 6 chars",   key="rp")
            rc = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat password",key="rc")
            if st.button("✨ Create Account", key="btn_reg"):
                if not all([rn,ru,rp,rc]):    st.error("Please fill in all fields!")
                elif rp != rc:                st.error("Passwords do not match!")
                elif len(rp) < 6:             st.error("Password must be at least 6 characters!")
                else:
                    ok, msg = register_user(ru, rp, rn)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:16px 0 20px;'>
        <div style='font-size:2.5rem;filter:drop-shadow(0 0 12px rgba(56,189,248,0.6));'>🧠</div>
        <div style='font-family:"Rajdhani",sans-serif;font-size:1.2rem;font-weight:700;letter-spacing:3px;
                    background:linear-gradient(135deg,#38bdf8,#0ea5e9);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-transform:uppercase;'>WorkloadAI</div>
        <div style='color:#334155;font-size:0.7rem;margin-top:4px;letter-spacing:2px;font-family:"Rajdhani",sans-serif;'>PATTERN ANALYSIS</div>
    </div>
    <hr style='border-color:rgba(108,99,255,0.2);margin:0 0 12px;'/>
    <div style='padding:0 0 12px;'>
        <div style='color:#94a3b8;font-size:0.75rem;font-weight:600;letter-spacing:.08em;margin-bottom:6px;'>LOGGED IN AS</div>
        <div style='font-size:1rem;font-weight:700;color:#6c63ff;'>👤 {st.session_state.user_name}</div>
    </div>
    <hr style='border-color:rgba(108,99,255,0.2);margin:0 0 12px;'/>
    <div style='padding:0 0 12px;'>
        <div style='color:#94a3b8;font-size:0.78rem;font-weight:600;letter-spacing:.08em;margin-bottom:10px;'>HOW IT WORKS</div>
        <div style='color:#cbd5e1;font-size:0.82rem;line-height:1.8;'>
            1️⃣ &nbsp;Answer 5 quick questions<br>
            2️⃣ &nbsp;Click <b>Analyze</b><br>
            3️⃣ &nbsp;Get your workload score<br>
            4️⃣ &nbsp;Read personalized tips
        </div>
    </div>
    <hr style='border-color:rgba(108,99,255,0.2);margin:0 0 12px;'/>
    <div style='padding:0 0 12px;'>
        <div style='color:#94a3b8;font-size:0.78rem;font-weight:600;letter-spacing:.08em;margin-bottom:10px;'>SCORE GUIDE</div>
        <div style='font-size:0.82rem;line-height:1.9;'>
            <span style='color:#10b981;'>● Balanced</span> — Healthy day<br>
            <span style='color:#f59e0b;'>● Moderate</span> — A bit busy<br>
            <span style='color:#ef4444;'>● Overloaded</span> — Needs rest
        </div>
    </div>
    <hr style='border-color:rgba(108,99,255,0.2);margin:0 0 12px;'/>""", unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        save_history(st.session_state.username, st.session_state.history)
        for k in ["logged_in","username","user_name","history"]:
            del st.session_state[k]
        st.experimental_rerun()

    st.markdown("<div style='color:#475569;font-size:0.72rem;text-align:center;padding:12px 0;'>⚠️ Not a medical tool.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-container">
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:16px;">
        <div style="font-size:3rem;filter:drop-shadow(0 0 20px rgba(108,99,255,0.8));animation:iconFloat 4s ease-in-out infinite;">🧠</div>
        <div>
            <div class="hero-title">WorkloadAI — Pattern Analysis</div>
            <p class="hero-sub">AI-powered behavioral analysis &nbsp;·&nbsp; Neural classification &nbsp;·&nbsp; Real-time insights</p>
        </div>
    </div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:12px;">
        <div style="color:#a78bfa;font-size:0.78rem;letter-spacing:2px;font-family:Rajdhani,sans-serif;display:flex;align-items:center;gap:6px;">
            <span style="width:6px;height:6px;border-radius:50%;background:#6c63ff;box-shadow:0 0 8px #6c63ff;display:inline-block;animation:dotPulse 2s infinite;"></span>NEURAL NETWORK
        </div>
        <div style="color:#a78bfa;font-size:0.78rem;letter-spacing:2px;font-family:Rajdhani,sans-serif;display:flex;align-items:center;gap:6px;">
            <span style="width:6px;height:6px;border-radius:50%;background:#00d4ff;box-shadow:0 0 8px #00d4ff;display:inline-block;animation:dotPulse 2s infinite 0.3s;"></span>99.7% ACCURACY
        </div>
        <div style="color:#a78bfa;font-size:0.78rem;letter-spacing:2px;font-family:Rajdhani,sans-serif;display:flex;align-items:center;gap:6px;">
            <span style="width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;display:inline-block;animation:dotPulse 2s infinite 0.6s;"></span>PRIVACY FIRST
        </div>
    </div>
</div>
<style>
@keyframes iconFloat { 0%,100%{transform:translateY(0) rotate(0deg)} 50%{transform:translateY(-6px) rotate(3deg)} }
</style>""", unsafe_allow_html=True)


# ── PARTICLES ANIMATION (CSS-based) ─────────────────────────────────────────
st.markdown("""
<style>
.particle {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    animation: particleFloat linear infinite;
}
@keyframes particleFloat {
    0%   { transform: translateY(0px) translateX(0px); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 1; }
    100% { transform: translateY(-100vh) translateX(30px); opacity: 0; }
}
@keyframes particlePulse {
    0%,100% { transform: scale(1); opacity: 0.6; }
    50%     { transform: scale(1.8); opacity: 1; }
}
</style>
<div id="particles-wrap" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;overflow:hidden;">
  <div class="particle" style="left:5%;top:80%;width:3px;height:3px;background:rgba(108,99,255,0.8);box-shadow:0 0 6px #6c63ff;animation-duration:12s;animation-delay:0s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:10%;top:90%;width:2px;height:2px;background:rgba(0,212,255,0.8);box-shadow:0 0 6px #00d4ff;animation-duration:15s;animation-delay:1s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:18%;top:85%;width:4px;height:4px;background:rgba(167,139,250,0.7);box-shadow:0 0 8px #a78bfa;animation-duration:11s;animation-delay:2s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:25%;top:95%;width:2px;height:2px;background:rgba(16,185,129,0.8);box-shadow:0 0 6px #10b981;animation-duration:18s;animation-delay:0.5s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:33%;top:88%;width:3px;height:3px;background:rgba(108,99,255,0.7);box-shadow:0 0 6px #6c63ff;animation-duration:13s;animation-delay:3s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:40%;top:92%;width:2px;height:2px;background:rgba(0,212,255,0.9);box-shadow:0 0 8px #00d4ff;animation-duration:16s;animation-delay:1.5s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:47%;top:86%;width:3px;height:3px;background:rgba(167,139,250,0.8);box-shadow:0 0 6px #a78bfa;animation-duration:14s;animation-delay:4s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:55%;top:93%;width:2px;height:2px;background:rgba(108,99,255,0.8);box-shadow:0 0 6px #6c63ff;animation-duration:10s;animation-delay:2.5s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:62%;top:89%;width:4px;height:4px;background:rgba(0,212,255,0.7);box-shadow:0 0 8px #00d4ff;animation-duration:17s;animation-delay:0.8s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:70%;top:94%;width:2px;height:2px;background:rgba(16,185,129,0.8);box-shadow:0 0 6px #10b981;animation-duration:12s;animation-delay:3.5s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:78%;top:87%;width:3px;height:3px;background:rgba(108,99,255,0.9);box-shadow:0 0 8px #6c63ff;animation-duration:15s;animation-delay:1.2s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:85%;top:91%;width:2px;height:2px;background:rgba(0,212,255,0.8);box-shadow:0 0 6px #00d4ff;animation-duration:13s;animation-delay:4.5s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:92%;top:84%;width:3px;height:3px;background:rgba(167,139,250,0.7);box-shadow:0 0 6px #a78bfa;animation-duration:11s;animation-delay:2.2s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:8%;top:50%;width:2px;height:2px;background:rgba(108,99,255,0.5);box-shadow:0 0 6px #6c63ff;animation-duration:20s;animation-delay:6s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:22%;top:60%;width:3px;height:3px;background:rgba(0,212,255,0.5);box-shadow:0 0 6px #00d4ff;animation-duration:22s;animation-delay:7s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:45%;top:55%;width:2px;height:2px;background:rgba(167,139,250,0.5);box-shadow:0 0 6px #a78bfa;animation-duration:19s;animation-delay:5s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:68%;top:65%;width:3px;height:3px;background:rgba(16,185,129,0.5);box-shadow:0 0 6px #10b981;animation-duration:21s;animation-delay:8s;animation-name:particleFloat;"></div>
  <div class="particle" style="left:88%;top:45%;width:2px;height:2px;background:rgba(108,99,255,0.5);box-shadow:0 0 6px #6c63ff;animation-duration:18s;animation-delay:9s;animation-name:particleFloat;"></div>
  <!-- Glowing orbs that pulse -->
  <div style="position:fixed;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(108,99,255,0.06),transparent);top:20%;left:10%;animation:particlePulse 6s ease-in-out infinite;pointer-events:none;z-index:1;"></div>
  <div style="position:fixed;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(0,212,255,0.04),transparent);top:50%;right:5%;animation:particlePulse 8s ease-in-out infinite 2s;pointer-events:none;z-index:1;"></div>
  <div style="position:fixed;width:150px;height:150px;border-radius:50%;background:radial-gradient(circle,rgba(16,185,129,0.05),transparent);bottom:20%;left:40%;animation:particlePulse 7s ease-in-out infinite 1s;pointer-events:none;z-index:1;"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INPUT FORM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📝 Tell Us About Your Day</div>', unsafe_allow_html=True)

q1 = st.selectbox("😴 How did you sleep last night?",
    ["Very well (8+ hours)","Okay (6-8 hours)","Not great (4-6 hours)","Poorly (< 4 hours)"])
q2 = st.selectbox("💼 How was your workload today?",
    ["Light — easy day","Normal — manageable","Heavy — quite busy","Overwhelming — too much"])
q3 = st.selectbox("🏃 Did you exercise or stay active?",
    ["Yes, very active","A little (walk/stretch)","Barely moved","No activity at all"])
q4 = st.selectbox("📱 How much screen time before bed?",
    ["None","Less than 30 mins","30 min – 1 hour","More than 1 hour"])
q5 = st.selectbox("☕ How many breaks did you take during work?",
    ["5 or more","3-4 breaks","1-2 breaks","No breaks at all"])

sleep_v = {"Very well (8+ hours)":8.5,"Okay (6-8 hours)":7.0,"Not great (4-6 hours)":5.0,"Poorly (< 4 hours)":3.5}[q1]
squal_v = {"Very well (8+ hours)":8.0,"Okay (6-8 hours)":6.5,"Not great (4-6 hours)":4.5,"Poorly (< 4 hours)":2.5}[q1]
act_v   = {"Yes, very active":80.0,"A little (walk/stretch)":45.0,"Barely moved":15.0,"No activity at all":5.0}[q3]
step_v  = {"Yes, very active":12000.0,"A little (walk/stretch)":6000.0,"Barely moved":2000.0,"No activity at all":500.0}[q3]
work_v  = {"Light — easy day":5.0,"Normal — manageable":8.0,"Heavy — quite busy":11.0,"Overwhelming — too much":14.0}[q2]
scrs_v  = {"None":0.0,"Less than 30 mins":0.3,"30 min – 1 hour":0.75,"More than 1 hour":2.0}[q4]
brk_v   = {"5 or more":6.0,"3-4 breaks":3.5,"1-2 breaks":1.5,"No breaks at all":0.0}[q5]

# Normalization to match training dataset (all features 0-1)
feat_today = {
    "Sleep Duration":           min(sleep_v / 12.0, 1.0),
    "Quality of Sleep":         min(squal_v / 10.0, 1.0),
    "Physical Activity Level":  min(act_v / 100.0, 1.0),
    "Heart Rate":               min((72.0 - 40.0) / 60.0, 1.0),    # 40-100 bpm range
    "Daily Steps":              min(step_v / 20000.0, 1.0),
    "work_hours_per_day":       min(work_v / 16.0, 1.0),
    "screen_time_before_sleep": min(scrs_v / 4.0, 1.0),
    "breaks_during_work":       min(brk_v / 10.0, 1.0),
    "Daily_Screen_Time(hrs)":   min(6.0 / 16.0, 1.0),
}

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("🔍 Analyze My Workload", use_container_width=True)

# ── Run analysis only when button clicked ──────────────────────────────────
if analyze_btn:
    model, _ = try_load_model()
    if model is not None:
        import pandas as _pd
        _X = _pd.DataFrame([feat_today])[FEATURES].values
        probs = model.predict(_X, verbose=0)[0]
        pred_class = int(np.argmax(probs))
        label = ["Balanced", "Moderate", "Overloaded"][pred_class]
        score = float(pred_class) / 2.0  # 0.0, 0.5, 1.0 for display
        _, badge = classify(score)
    else:
        score = compute_score(feat_today)
        label, badge = classify(score)
    today_date = datetime.now().strftime("%Y-%m-%d")
    new_entry = {
        "date":         datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score":        score,
        "label":        label,
        "sleep_dur":    feat_today["Sleep Duration"],
        "sleep_qual":   feat_today["Quality of Sleep"],
        "activity":     feat_today["Physical Activity Level"],
        "heart_rate":   feat_today["Heart Rate"],
        "steps":        feat_today["Daily Steps"],
        "work_hours":   feat_today["work_hours_per_day"],
        "screen_sleep": feat_today["screen_time_before_sleep"],
        "breaks":       feat_today["breaks_during_work"],
        "screen_time":  feat_today["Daily_Screen_Time(hrs)"],
    }
    # Replace today's entry if already exists — one entry per day only
    existing_dates = [e["date"][:10] for e in st.session_state.history]
    if today_date in existing_dates:
        idx = existing_dates.index(today_date)
        st.session_state.history[idx] = new_entry
        st.success("✅ Today's data updated!")
    else:
        st.session_state.history.append(new_entry)
        st.success("✅ Today's data saved!")
    save_history(st.session_state.username, st.session_state.history)

# ── Stop if no history at all ───────────────────────────────────────────────
if not st.session_state.history:
    st.info("👆 Answer the questions above and click **Analyze My Workload** to see your results.")
    st.stop()

# ── Build history dataframe (deduplicate by date, keep latest per day) ────────
hdf = pd.DataFrame(st.session_state.history)
hdf["date_parsed"] = pd.to_datetime(hdf["date"], errors="coerce")
hdf["score"]       = hdf["score"].astype(float)
hdf["day_key"]     = hdf["date_parsed"].dt.strftime("%Y-%m-%d")
hdf = hdf.drop_duplicates(subset="day_key", keep="last").reset_index(drop=True)
hdf = hdf.sort_values("date_parsed").reset_index(drop=True)

latest       = hdf.iloc[-1]
latest_score = float(latest["score"])
avg_score    = float(hdf["score"].mean())
high_days    = int((hdf["label"] == "Overloaded").sum())
total_days   = len(hdf)
cur_lvl, cur_badge = classify(latest_score)

# Feature values from latest entry
feat_latest = {
    "Sleep Duration":           float(latest.get("sleep_dur",    0.5)),
    "Quality of Sleep":         float(latest.get("sleep_qual",   0.5)),
    "Physical Activity Level":  float(latest.get("activity",     0.5)),
    "Heart Rate":               float(latest.get("heart_rate",   0.5)),
    "Daily Steps":              float(latest.get("steps",        0.5)),
    "work_hours_per_day":       float(latest.get("work_hours",   0.5)),
    "screen_time_before_sleep": float(latest.get("screen_sleep", 0.5)),
    "breaks_during_work":       float(latest.get("breaks",       0.5)),
    "Daily_Screen_Time(hrs)":   float(latest.get("screen_time",  0.5)),
}

# ══════════════════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Current Overview</div>', unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)
for col,cls,clr,val,lbl in [
    (c1,"purple","#6c63ff",f"{latest_score:.3f}","Latest Score"),
    (c2,"cyan",  "#06b6d4",f"{avg_score:.3f}",   "Average Score"),
    (c3,"amber", "#f59e0b",str(high_days),        "Overloaded Days"),
    (c4,"green", "#10b981",str(total_days),        "Days Analyzed"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card {cls}">
            <div class="metric-value" style="color:{clr};">{val}</div>
            <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div style='display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin:16px 0;'>
    <span style='color:#94a3b8;font-size:0.95rem;'>Today's Workload Status:</span>
    <span class='status-badge {cur_badge}'><span class='status-dot'></span>{cur_lvl}</span>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "📈 Score Trend","🔍 Feature Details",
    "💡 Guidance","📅 Weekly Report","📋 Summary Report","🗂️ History"
])

# ── TAB 1 : SCORE TREND ───────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">📉 Your Deviation Score — Day by Day</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        📌 <b>How to read:</b> Each bar = one day.
        <b style='color:#10b981;'>Green</b> = Balanced &nbsp;|&nbsp;
        <b style='color:#f59e0b;'>Yellow</b> = Moderate &nbsp;|&nbsp;
        <b style='color:#ef4444;'>Red</b> = Overloaded &nbsp;|&nbsp;
        Score range: 0 to 1 &nbsp;|&nbsp; Lower = better ✅
    </div>""", unsafe_allow_html=True)

    hdf["day_label"] = hdf["date_parsed"].dt.strftime("%d %b")
    raw_scores       = hdf["score"].tolist()
    norm_scores      = [min(round(s, 3), 1.0) for s in raw_scores]
    labels_          = hdf["label"].tolist()
    colors_          = [COLOR_MAP.get(l, "#6c63ff") for l in labels_]
    xlabels_         = hdf["day_label"].tolist()
    bal_limit        = 0.15
    mod_limit        = 0.55

    fig1 = go.Figure()

    # Colored background zones
    fig1.add_hrect(y0=0,         y1=bal_limit,
                   fillcolor="rgba(16,185,129,0.12)", line_width=0,
                   annotation_text="✅ Balanced Zone",
                   annotation_position="top left",
                   annotation_font=dict(color="#10b981", size=11))
    fig1.add_hrect(y0=bal_limit, y1=mod_limit,
                   fillcolor="rgba(245,158,11,0.10)", line_width=0,
                   annotation_text="⚡ Moderate Zone",
                   annotation_position="top left",
                   annotation_font=dict(color="#f59e0b", size=11))
    fig1.add_hrect(y0=mod_limit, y1=1.0,
                   fillcolor="rgba(239,68,68,0.08)", line_width=0,
                   annotation_text="🚨 Overloaded Zone",
                   annotation_position="top left",
                   annotation_font=dict(color="#ef4444", size=11))

    # Bars
    fig1.add_trace(go.Bar(
        x=xlabels_, y=norm_scores,
        marker_color=colors_,
        marker_line_color="rgba(255,255,255,0.15)",
        marker_line_width=1,
        text=[f"{l}" for l in labels_],
        textposition="outside",
        textfont=dict(size=12, color="white"),
        hovertemplate="<b>%{x}</b><br>Score: %{y:.3f}<extra></extra>",
        showlegend=False,
        width=0.5,
    ))

    # Legend dummies
    for lvl, clr in [("✅ Balanced","#10b981"),("⚡ Moderate","#f59e0b"),("🚨 Overloaded","#ef4444")]:
        fig1.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
            name=lvl, marker=dict(color=clr, size=12, symbol="square")))

    ly1 = plotly_bg()
    ly1["xaxis"] = dict(title="Date", gridcolor="rgba(255,255,255,0.06)",
                        tickangle=0, tickfont=dict(size=13))
    ly1["yaxis"] = dict(
        title="Deviation Score (0 = best, 1 = worst)",
        gridcolor="rgba(255,255,255,0.06)",
        range=[0, 1.15],
        tickmode="array",
        tickvals=[0, bal_limit, mod_limit, 1.0],
        ticktext=[
            "0  ✅ Balanced",
            f"{bal_limit}  ⚡ Moderate starts",
            f"{mod_limit}  🚨 Overloaded starts",
            "1.0  Max",
        ],
        tickfont=dict(size=10),
        title_font=dict(size=12),
        side="left",
    )
    # Add horizontal lines with range labels
    fig1.add_shape(type="line", x0=-0.5, x1=len(xlabels_)-0.5,
                   y0=bal_limit, y1=bal_limit,
                   line=dict(color="#10b981", width=1.5, dash="dot"))
    fig1.add_shape(type="line", x0=-0.5, x1=len(xlabels_)-0.5,
                   y0=mod_limit, y1=mod_limit,
                   line=dict(color="#f59e0b", width=1.5, dash="dot"))

    # Range annotations on right side
    fig1.add_annotation(x=len(xlabels_)-0.3, y=bal_limit/2,
                        text="✅ Normal<br>0 – 0.15",
                        showarrow=False, xanchor="left",
                        font=dict(color="#10b981", size=10),
                        bgcolor="rgba(16,185,129,0.15)", borderpad=3)
    fig1.add_annotation(x=len(xlabels_)-0.3, y=(bal_limit+mod_limit)/2,
                        text="⚡ Moderate<br>0.15 – 0.55",
                        showarrow=False, xanchor="left",
                        font=dict(color="#f59e0b", size=10),
                        bgcolor="rgba(245,158,11,0.15)", borderpad=3)
    fig1.add_annotation(x=len(xlabels_)-0.3, y=(mod_limit+0.8)/2,
                        text="🚨 Overloaded<br>> 0.55",
                        showarrow=False, xanchor="left",
                        font=dict(color="#ef4444", size=10),
                        bgcolor="rgba(239,68,68,0.15)", borderpad=3)

    fig1.update_layout(**ly1, height=440, bargap=0.4,
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(t=50, b=40, l=10, r=130))
    st.plotly_chart(fig1, use_container_width=True)

    if total_days >= 2:
        st.markdown('<div class="section-title">🍩 Deviation Level Distribution</div>', unsafe_allow_html=True)
        lc = hdf["label"].value_counts()
        fig_d = go.Figure(go.Pie(
            labels=lc.index, values=lc.values, hole=0.55,
            marker=dict(colors=[COLOR_MAP.get(l,"#6c63ff") for l in lc.index],
                        line=dict(color="#0a0e1a",width=2)),
            textfont=dict(size=13,color="white"),
            hovertemplate="<b>%{label}</b><br>%{value} days — %{percent}<extra></extra>"
        ))
        fig_d.update_layout(**plotly_bg(),height=300,
            legend=dict(orientation="h",y=-0.1,x=0.25),
            margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_d, use_container_width=True)

# ── TAB 2 : FEATURE DETAILS ───────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">🔬 Today\'s Habits in Detail</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        📌 Each bar = one habit. Dotted line = normal level (0.5).<br>
        If sleep/breaks are low or work/screen-time is high — that affects your score.
    </div>""", unsafe_allow_html=True)

    for row_feats in [
        ["Sleep Duration","Quality of Sleep","Physical Activity Level"],
        ["Heart Rate","Daily Steps","work_hours_per_day"],
        ["screen_time_before_sleep","breaks_during_work","Daily_Screen_Time(hrs)"],
    ]:
        cols = st.columns(3)
        for col,feat in zip(cols,row_feats):
            lbl,clr = FEAT_META[feat]
            val     = feat_latest[feat]
            with col:
                fig_b = go.Figure()
                fig_b.add_trace(go.Bar(
                    x=[lbl], y=[val],
                    marker_color=clr,
                    marker_line_color="rgba(255,255,255,0.2)", marker_line_width=1,
                    text=[f"{val:.2f}"], textposition="outside",
                    textfont=dict(color=clr,size=13)
                ))
                fig_b.add_hline(y=0.5,line_dash="dot",line_color="rgba(255,255,255,0.35)",
                                annotation_text="Normal",annotation_font=dict(size=10,color="#94a3b8"))
                ly = plotly_bg()
                ly["xaxis"] = dict(gridcolor="rgba(255,255,255,0.06)")
                ly["yaxis"] = dict(range=[0,1.3],gridcolor="rgba(255,255,255,0.06)")
                fig_b.update_layout(**ly,
                    title=dict(text=lbl,font=dict(size=13,color=clr),x=0.02),
                    height=220, showlegend=False,
                    margin=dict(t=36,b=16,l=10,r=10))
                st.plotly_chart(fig_b, use_container_width=True)

    st.markdown("<div class='section-title'>🎯 Today's Full Snapshot (Radar)</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        📌 Bigger shape = higher value.
        <b>Work hours</b> &amp; <b>screen time</b> should stay low.
        <b>Sleep</b> &amp; <b>breaks</b> should be higher.
    </div>""", unsafe_allow_html=True)

    cats  = [FEAT_EASY[f] for f in FEATURES]
    vals  = [feat_latest[f] for f in FEATURES]
    cats2 = cats + [cats[0]]
    vals2 = vals + [vals[0]]

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=[0.5]*len(cats2),theta=cats2,fill="toself",
        fillcolor="rgba(6,182,212,0.06)",line=dict(color="#06b6d4",width=1.5,dash="dot"),name="Normal"))
    fig_r.add_trace(go.Scatterpolar(r=vals2,theta=cats2,fill="toself",
        fillcolor="rgba(108,99,255,0.15)",line=dict(color="#6c63ff",width=2.5),name="Today"))
    fig_r.update_layout(**plotly_bg(),
        polar=dict(
            radialaxis=dict(visible=True,range=[0,1],gridcolor="rgba(255,255,255,0.08)",
                            tickfont=dict(color="#64748b",size=9)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)",tickfont=dict(color="#cbd5e1",size=11)),
            bgcolor="rgba(0,0,0,0)"),
        height=400, legend=dict(orientation="h",y=-0.1,x=0.3),
        margin=dict(t=20,b=40,l=20,r=20))
    st.plotly_chart(fig_r, use_container_width=True)

# ── TAB 3 : GUIDANCE ──────────────────────────────────────────────────────────
with tab3:
    ca,cb = st.columns([2,1])
    with ca:
        st.markdown(f'<div class="section-title">💡 Personalized Guidance — {cur_lvl}</div>', unsafe_allow_html=True)
        for i,tip in enumerate(get_guidance(cur_lvl)):
            st.markdown(f'<div class="guidance-card">{tip}</div>', unsafe_allow_html=True)
    with cb:
        st.markdown("<div class='section-title'>📊 Today's Metrics</div>", unsafe_allow_html=True)
        for icon,name,val,clr in [
            ("😴","Sleep Duration",   feat_latest["Sleep Duration"],           "#6c63ff"),
            ("🌙","Sleep Quality",    feat_latest["Quality of Sleep"],          "#8b5cf6"),
            ("🏃","Physical Activity",feat_latest["Physical Activity Level"],   "#10b981"),
            ("❤️","Heart Rate",       feat_latest["Heart Rate"],                "#ef4444"),
            ("👣","Daily Steps",      feat_latest["Daily Steps"],               "#f59e0b"),
            ("💼","Work Hours/Day",   feat_latest["work_hours_per_day"],        "#e11d48"),
            ("📱","Screen Before Bed",feat_latest["screen_time_before_sleep"],  "#f97316"),
            ("☕","Breaks",           feat_latest["breaks_during_work"],         "#06b6d4"),
            ("🖥️","Daily Screen Time",feat_latest["Daily_Screen_Time(hrs)"],    "#64748b"),
        ]:
            pct = min(int(val*100),100)
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                    <span style="color:#e2e8f0;font-size:0.88rem;">{icon} {name}</span>
                    <span style="color:{clr};font-weight:700;font-size:0.88rem;">{val:.2f}</span>
                </div>
                <div class="prog-bg"><div class="prog-bar" style="width:{pct}%;background:linear-gradient(90deg,{clr}88,{clr});"></div></div>
            </div>""", unsafe_allow_html=True)

# ── TAB 4 : WEEKLY REPORT ─────────────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-title'>📅 This Week's Report</div>", unsafe_allow_html=True)

    # Filter current week only
    _today     = pd.Timestamp.today().normalize() + timedelta(hours=23, minutes=59, seconds=59)
    _wk_start  = pd.Timestamp.today().normalize() - timedelta(days=6)
    wdf        = hdf[(hdf["date_parsed"] >= _wk_start) & (hdf["date_parsed"] <= _today)].copy()

    if len(wdf) < 1:
        st.info("📌 No data this week yet. Log a day to see your weekly report!")
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(108,99,255,0.12),rgba(6,182,212,0.10));
                    border:1px solid rgba(108,99,255,0.3);border-radius:18px;padding:24px 28px;margin-bottom:24px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:12px;">
                📋 This Week's Summary</div>
            <div style="color:#cbd5e1;font-size:0.92rem;line-height:1.9;">{weekly_insight(wdf)}</div>
        </div>""", unsafe_allow_html=True)

        # Day cards
        st.markdown('<div class="section-title">📆 Day-by-Day Status</div>', unsafe_allow_html=True)
        dcols = st.columns(min(len(wdf),7))
        for i,(_, row) in enumerate(wdf.iterrows()):
            if i >= len(dcols): break
            lvl = row["label"]; clr = COLOR_MAP.get(lvl,"#6c63ff")
            emj = {"Balanced":"✅","Moderate":"⚡","Overloaded":"🚨"}.get(lvl,"❓")
            try:   dn = row["date_parsed"].strftime("%a\n%d %b")
            except: dn = str(row["date"])[:10]
            with dcols[i]:
                st.markdown(f"""
                <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(255,255,255,0.08);
                            border-radius:14px;padding:14px 8px;text-align:center;">
                    <div style="font-size:1.5rem;">{emj}</div>
                    <div style="font-size:0.68rem;color:#94a3b8;margin:4px 0;">{dn}</div>
                    <div style="font-size:0.72rem;font-weight:700;color:{clr};">{lvl}</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">{row['score']:.3f}</div>
                </div>""", unsafe_allow_html=True)

        try:    xlabels = wdf["date_parsed"].dt.strftime("%a, %d %b").tolist()
        except: xlabels = wdf["date"].astype(str).tolist()

        # Bar chart
        st.markdown('<div class="section-title">📊 Weekly Score Bar Chart</div>', unsafe_allow_html=True)
        st.markdown("""<div class="info-box">
            <b style='color:#10b981;'>Green = Balanced</b> &nbsp;
            <b style='color:#f59e0b;'>Yellow = Moderate</b> &nbsp;
            <b style='color:#ef4444;'>Red = Overloaded</b>
        </div>""", unsafe_allow_html=True)

        fig_wb = go.Figure()
        # Background zones
        fig_wb.add_hrect(y0=0,    y1=0.15, fillcolor="rgba(16,185,129,0.08)", line_width=0,
                         annotation_text="✅ Balanced", annotation_position="top left",
                         annotation_font=dict(color="#10b981", size=10))
        fig_wb.add_hrect(y0=0.15, y1=0.55, fillcolor="rgba(245,158,11,0.08)", line_width=0,
                         annotation_text="⚡ Moderate", annotation_position="top left",
                         annotation_font=dict(color="#f59e0b", size=10))
        fig_wb.add_hrect(y0=0.55, y1=1.2,  fillcolor="rgba(239,68,68,0.06)",  line_width=0,
                         annotation_text="🚨 Overloaded", annotation_position="top left",
                         annotation_font=dict(color="#ef4444", size=10))
        _wb_scores = wdf["score"].tolist()
        _wb_labels = wdf["label"].tolist()
        _wb_display = [max(s, 0.01) for s in _wb_scores]  # min height so 0.0 bars show
        fig_wb.add_trace(go.Bar(
            x=xlabels, y=_wb_display,
            marker_color=[COLOR_MAP.get(l,"#6c63ff") for l in _wb_labels],
            marker_line_color="rgba(255,255,255,0.15)", marker_line_width=1,
            text=[f"{s:.3f}" for s in _wb_scores],
            textposition="outside", textfont=dict(color="white", size=11)
        ))
        fig_wb.add_hline(y=0.55, line_dash="dot", line_color="rgba(239,68,68,0.6)",
                         annotation_text="0.55", annotation_position="right",
                         annotation_font=dict(color="#ef4444",size=10))
        fig_wb.add_hline(y=0.15, line_dash="dot", line_color="rgba(16,185,129,0.6)",
                         annotation_text="0.15", annotation_position="right",
                         annotation_font=dict(color="#10b981",size=10))
        wb_ly = plotly_bg()
        wb_ly["xaxis"] = dict(title="Date", gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=12))
        wb_ly["yaxis"] = dict(title="Score (0=best, 1=worst)",
                              gridcolor="rgba(255,255,255,0.04)", range=[0, 1.2])
        fig_wb.update_layout(**wb_ly, height=380, margin=dict(t=30,b=20,l=10,r=60), bargap=0.4)
        st.plotly_chart(fig_wb, use_container_width=True)



        # Distribution pie
        st.markdown("<div class='section-title'>🍩 This Week's Distribution</div>", unsafe_allow_html=True)
        wlc = wdf["label"].value_counts()
        fig_wp = go.Figure(go.Pie(
            labels=wlc.index, values=wlc.values, hole=0.55,
            marker=dict(colors=[COLOR_MAP.get(l,"#6c63ff") for l in wlc.index],
                        line=dict(color="#0a0e1a",width=2)),
            textfont=dict(size=13,color="white"),
            hovertemplate="<b>%{label}</b><br>%{value} days — %{percent}<extra></extra>"
        ))
        fig_wp.update_layout(**plotly_bg(),height=300,
            legend=dict(orientation="h",y=-0.1,x=0.2),
            margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_wp, use_container_width=True)

        # Heatmap
        if len(wdf) >= 2:
            st.markdown('<div class="section-title">🔥 Weekly Habits Heatmap</div>', unsafe_allow_html=True)
            st.markdown("""<div class="info-box">
                <b style='color:#10b981;'>Green = good</b> &nbsp; <b style='color:#ef4444;'>Red = needs attention</b>
            </div>""", unsafe_allow_html=True)
            hcols = ["sleep_dur","sleep_qual","activity","work_hours","screen_sleep","breaks"]
            hlbls = ["😴 Sleep","🌙 Sleep Quality","🏃 Activity","💼 Work Hours","📱 Screen@Bed","☕ Breaks"]
            hmap_x = wdf["date_parsed"].dt.strftime("%a %d %b").tolist()
            # high=good: sleep, sleep_qual, activity, breaks
            # high=bad : work_hours, screen_sleep (invert these)
            invert_cols = {"work_hours", "screen_sleep"}
            matrix = []
            raw_vals = []
            for col in hcols:
                if col in wdf.columns:
                    vals = wdf[col].fillna(0.5).tolist()
                else:
                    vals = [0.5]*len(wdf)
                raw_vals.append(vals)
                if col in invert_cols:
                    matrix.append([1-v for v in vals])
                else:
                    matrix.append(vals)
            # Build hover text with labels
            hover_text = []
            for i, habit in enumerate(hlbls):
                row_hover = []
                for j, day in enumerate(hmap_x):
                    v = matrix[i][j]
                    if v >= 0.8:   lbl = "Excellent ✅"
                    elif v >= 0.6: lbl = "Good 🟢"
                    elif v >= 0.4: lbl = "Moderate 🟡"
                    elif v >= 0.2: lbl = "Bad 🟠"
                    else:          lbl = "Very Bad 🔴"
                    row_hover.append(f"<b>{habit}</b><br>📅 {day}<br>Value: {v:.2f}<br>Status: {lbl}")
                hover_text.append(row_hover)

            fig_hm = go.Figure(go.Heatmap(
                z=matrix,
                x=hmap_x,
                y=hlbls,
                colorscale=[[0,"#ef4444"],[0.25,"#f97316"],[0.5,"#f59e0b"],[0.75,"#84cc16"],[1,"#10b981"]],
                zmin=0, zmax=1,
                text=[[f"{raw_vals[i][j]:.2f}" for j in range(len(hmap_x))] for i in range(len(hlbls))],
                texttemplate="%{text}",
                textfont=dict(size=11, color="white"),
                hoverinfo="text",
                hovertext=hover_text,
                hoverongaps=False,
                colorbar=dict(
                    title=dict(text="Level", font=dict(color="#94a3b8", size=11)),
                    tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                    ticktext=["🔴 Very Bad", "🟠 Bad", "🟡 OK", "🟢 Good", "✅ Excellent"],
                    tickfont=dict(size=9, color="#94a3b8"),
                    tickmode="array",
                )
            ))
            hm_ly = plotly_bg()
            hm_ly["xaxis"] = dict(title="Day", tickfont=dict(size=11, color="#94a3b8"))
            hm_ly["yaxis"] = dict(title="", tickfont=dict(size=11, color="#94a3b8"), autorange="reversed")
            fig_hm.update_layout(**hm_ly, height=320, margin=dict(t=10,b=10,l=140,r=130))
            st.plotly_chart(fig_hm, use_container_width=True)

        # Best day always show if 2+ days
        # Worst day only show if there is at least 1 Overloaded day
        if len(wdf) >= 2:
            best_row = wdf.loc[wdf["score"].idxmin()]
            try:    bd = pd.to_datetime(best_row["date"]).strftime("%d %b, %A")
            except: bd = str(best_row["date"])[:10]

            overloaded_days = wdf[wdf["label"] == "Overloaded"]

            if len(overloaded_days) > 0:
                worst_row = overloaded_days.loc[overloaded_days["score"].idxmax()]
                try:    wd = pd.to_datetime(worst_row["date"]).strftime("%d %b, %A")
                except: wd = str(worst_row["date"])[:10]
                col_b, col_w = st.columns(2)
            else:
                col_b = st.columns(1)[0]
                col_w = None

            with col_b:
                st.markdown(f"""
                <div style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);
                            border-radius:14px;padding:20px;text-align:center;margin-top:16px;">
                    <div style="font-size:2rem;">🏆</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#10b981;font-size:1.1rem;letter-spacing:1px;">BEST DAY THIS WEEK</div>
                    <div style="color:#94a3b8;font-size:0.9rem;margin-top:6px;">{bd}</div>
                    <div style="color:#10b981;font-size:1.8rem;font-weight:800;margin-top:8px;font-family:'Rajdhani',sans-serif;">{best_row["score"]:.3f}</div>
                    <div style="color:#475569;font-size:0.8rem;">Lowest deviation ✅</div>
                </div>""", unsafe_allow_html=True)

            if col_w is not None:
                with col_w:
                    st.markdown(f"""
                    <div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);
                                border-radius:14px;padding:20px;text-align:center;margin-top:16px;">
                        <div style="font-size:2rem;">😓</div>
                        <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#ef4444;font-size:1.1rem;letter-spacing:1px;">HARDEST DAY THIS WEEK</div>
                        <div style="color:#94a3b8;font-size:0.9rem;margin-top:6px;">{wd}</div>
                        <div style="color:#ef4444;font-size:1.8rem;font-weight:800;margin-top:8px;font-family:'Rajdhani',sans-serif;">{worst_row["score"]:.3f}</div>
                        <div style="color:#475569;font-size:0.8rem;">Highest deviation 🚨</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("📌 Log at least 2 days this week to see Best day!")

# ── TAB 5 : SUMMARY REPORT ────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-title">📋 Summary Report</div>', unsafe_allow_html=True)
    bal_d = int((hdf["label"]=="Balanced").sum())
    mod_d = int((hdf["label"]=="Moderate").sum())
    ovr_d = int((hdf["label"]=="Overloaded").sum())

    st.markdown(f"""
    <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(255,255,255,0.08);
                border-radius:20px;padding:36px 40px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;margin-bottom:32px;">
            <div>
                <h2 style="margin:0;font-family:'Space Grotesk',sans-serif;
                           background:linear-gradient(135deg,#6c63ff,#06b6d4);
                           -webkit-background-clip:text;-webkit-text-fill-color:transparent;">Workload Pattern Report</h2>
                <p style="color:#64748b;margin:6px 0 0;font-size:0.9rem;">
                    {st.session_state.user_name} &nbsp;·&nbsp; Generated: {datetime.today().strftime("%B %d, %Y")}</p>
            </div>
            <span class='status-badge {cur_badge}'><span class='status-dot'></span>Today: {cur_lvl}</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:32px;">
            <div style="text-align:center;background:rgba(108,99,255,0.08);border-radius:12px;padding:20px;">
                <div style="font-size:2rem;font-weight:800;color:#6c63ff;">{latest_score:.3f}</div>
                <div style="color:#64748b;font-size:0.8rem;margin-top:4px;">TODAY'S SCORE</div>
            </div>
            <div style="text-align:center;background:rgba(6,182,212,0.08);border-radius:12px;padding:20px;">
                <div style="font-size:2rem;font-weight:800;color:#06b6d4;">{avg_score:.3f}</div>
                <div style="color:#64748b;font-size:0.8rem;margin-top:4px;">AVERAGE SCORE</div>
            </div>
            <div style="text-align:center;background:rgba(239,68,68,0.08);border-radius:12px;padding:20px;">
                <div style="font-size:2rem;font-weight:800;color:#ef4444;">{ovr_d}</div>
                <div style="color:#64748b;font-size:0.8rem;margin-top:4px;">OVERLOADED DAYS</div>
            </div>
        </div>
        <h3 style="color:#e2e8f0;font-family:'Space Grotesk',sans-serif;margin-bottom:16px;">Total {total_days} Days Analyzed</h3>
        <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:28px;">
            <div style="flex:1;min-width:120px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:#10b981;">{bal_d}</div>
                <div style="color:#64748b;font-size:0.8rem;">✅ Balanced Days</div>
            </div>
            <div style="flex:1;min-width:120px;background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:#f59e0b;">{mod_d}</div>
                <div style="color:#64748b;font-size:0.8rem;">⚡ Moderate Days</div>
            </div>
            <div style="flex:1;min-width:120px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:#ef4444;">{ovr_d}</div>
                <div style="color:#64748b;font-size:0.8rem;">🚨 Overloaded Days</div>
            </div>
        </div>
        <div style="padding:18px;background:rgba(108,99,255,0.08);border-left:3px solid #6c63ff;border-radius:0 10px 10px 0;">
            <p style="margin:0;color:#94a3b8;font-size:0.85rem;">
                ⚠️ <strong style="color:#a5b4fc;">Disclaimer:</strong>
                This report is for workload pattern analysis only and does not constitute
                medical advice, stress diagnosis, or mental health assessment.
            </p>
        </div>
    </div>""", unsafe_allow_html=True)

# ── TAB 6 : HISTORY ──────────────────────────────────────────────────────────
with tab6:
    st.markdown('<div class="section-title">🗂️ Full History — All Weeks</div>', unsafe_allow_html=True)

    if hdf.empty:
        st.info("No history yet.")
    else:
        # Get all weeks available
        hdf_hist = hdf.copy()
        hdf_hist["week_start"] = hdf_hist["date_parsed"].dt.to_period("W").apply(lambda x: x.start_time)
        hdf_hist["week_label"] = hdf_hist["week_start"].dt.strftime("Week of %d %b %Y")
        all_weeks = sorted(hdf_hist["week_label"].unique(), reverse=True)

        selected_week = st.selectbox("📅 Select a week to view:", all_weeks)

        week_data = hdf_hist[hdf_hist["week_label"] == selected_week].copy()
        week_data = week_data.sort_values("date_parsed").reset_index(drop=True)

        if len(week_data) == 0:
            st.info("No data for this week.")
        else:
            # Week summary
            bal_w  = int((week_data["label"]=="Balanced").sum())
            mod_w  = int((week_data["label"]=="Moderate").sum())
            ovr_w  = int((week_data["label"]=="Overloaded").sum())
            avg_w  = float(week_data["score"].mean())

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(108,99,255,0.12),rgba(0,212,255,0.08));
                        border:1px solid rgba(108,99,255,0.25);border-radius:16px;padding:20px 24px;margin-bottom:20px;">
                <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:700;color:#a78bfa;letter-spacing:2px;margin-bottom:10px;">
                    📋 {selected_week.upper()}</div>
                <div style="display:flex;gap:24px;flex-wrap:wrap;">
                    <span style="color:#10b981;font-size:0.9rem;">✅ {bal_w} Balanced</span>
                    <span style="color:#f59e0b;font-size:0.9rem;">⚡ {mod_w} Moderate</span>
                    <span style="color:#ef4444;font-size:0.9rem;">🚨 {ovr_w} Overloaded</span>
                    <span style="color:#94a3b8;font-size:0.9rem;">Avg: {avg_w:.3f}</span>
                </div>
            </div>""", unsafe_allow_html=True)

            # Day cards for selected week
            day_cols = st.columns(min(len(week_data), 7))
            for i, (_, row) in enumerate(week_data.iterrows()):
                if i >= len(day_cols): break
                lvl = row["label"]
                clr = COLOR_MAP.get(lvl, "#6c63ff")
                emj = {"Balanced":"✅","Moderate":"⚡","Overloaded":"🚨"}.get(lvl,"❓")
                try:   dn = row["date_parsed"].strftime("%a\n%d %b")
                except: dn = str(row["date"])[:10]
                with day_cols[i]:
                    st.markdown(f"""
                    <div style="background:rgba(8,15,30,0.9);border:1px solid rgba(255,255,255,0.07);
                                border-radius:14px;padding:14px 8px;text-align:center;margin-bottom:8px;">
                        <div style="font-size:1.4rem;">{emj}</div>
                        <div style="font-size:0.68rem;color:#64748b;margin:4px 0;">{dn}</div>
                        <div style="font-size:0.75rem;font-weight:700;color:{clr};font-family:'Rajdhani',sans-serif;">{lvl}</div>
                        <div style="font-size:0.68rem;color:#334155;margin-top:2px;">{row["score"]:.3f}</div>
                    </div>""", unsafe_allow_html=True)

            # Bar chart for selected week
            st.markdown('<div class="section-title">📊 Week Score Chart</div>', unsafe_allow_html=True)
            w_xlabels = week_data["date_parsed"].dt.strftime("%a, %d %b").tolist()
            fig_h = go.Figure()
            fig_h.add_hrect(y0=0,    y1=0.15, fillcolor="rgba(16,185,129,0.08)", line_width=0)
            fig_h.add_hrect(y0=0.15, y1=0.55, fillcolor="rgba(245,158,11,0.08)", line_width=0)
            fig_h.add_hrect(y0=0.55, y1=1.2,  fillcolor="rgba(239,68,68,0.06)",  line_width=0)
            _h_scores = week_data["score"].tolist()
            _h_labels = week_data["label"].tolist()
            _h_display = [max(s, 0.01) for s in _h_scores]
            fig_h.add_trace(go.Bar(
                x=w_xlabels, y=_h_display,
                marker_color=[COLOR_MAP.get(l,"#6c63ff") for l in _h_labels],
                text=[f"{s:.3f}" for s in _h_scores],
                textposition="outside", textfont=dict(color="white",size=11),
                marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1,
            ))
            fig_h.add_hline(y=0.55, line_dash="dot", line_color="rgba(239,68,68,0.6)",
                            annotation_text="Overloaded", annotation_font=dict(color="#ef4444",size=10))
            fig_h.add_hline(y=0.15, line_dash="dot", line_color="rgba(16,185,129,0.6)",
                            annotation_text="Balanced",   annotation_font=dict(color="#10b981",size=10))
            h_ly = plotly_bg()
            h_ly["xaxis"] = dict(title="Day", gridcolor="rgba(255,255,255,0.05)", tickangle=0)
            h_ly["yaxis"] = dict(title="Score (0=best, 1=worst)",
                                 gridcolor="rgba(255,255,255,0.05)", range=[0,1.2])
            fig_h.update_layout(**h_ly, height=360, bargap=0.35,
                margin=dict(t=20,b=20,l=10,r=80))
            st.plotly_chart(fig_h, use_container_width=True)

            # Heatmap for selected week
            if len(week_data) >= 2:
                st.markdown('<div class="section-title">🔥 Habits Heatmap</div>', unsafe_allow_html=True)
                hcols = ["sleep_dur","sleep_qual","activity","work_hours","screen_sleep","breaks"]
                hlbls = ["😴 Sleep","🌙 Sleep Quality","🏃 Activity","💼 Work Hours","📱 Screen@Bed","☕ Breaks"]
                if all(c in week_data.columns for c in hcols):
                    hmap_x2 = week_data["date_parsed"].dt.strftime("%a %d %b").tolist()
                    invert_cols2 = {"work_hours", "screen_sleep"}
                    matrix2 = []
                    raw2 = []
                    for col in hcols:
                        vals2 = week_data[col].fillna(0.5).tolist() if col in week_data.columns else [0.5]*len(week_data)
                        raw2.append(vals2)
                        matrix2.append([1-v for v in vals2] if col in invert_cols2 else vals2)
                    # Build hover text
                    hover_text2 = []
                    for i, habit in enumerate(hlbls):
                        row_hover = []
                        for j, day in enumerate(hmap_x2):
                            display_v = matrix2[i][j]  # already inverted for work/screen
                            raw_v = raw2[i][j]
                            if display_v >= 0.8:   lbl = "Excellent ✅"
                            elif display_v >= 0.6: lbl = "Good 🟢"
                            elif display_v >= 0.4: lbl = "OK 🟡"
                            elif display_v >= 0.2: lbl = "Bad 🟠"
                            else:                  lbl = "Very Bad 🔴"
                            row_hover.append(f"<b>{habit}</b><br>📅 {day}<br>Value: {raw_v:.2f}<br>Status: {lbl}")
                        hover_text2.append(row_hover)

                    fig_hh = go.Figure(go.Heatmap(
                        z=matrix2, x=hmap_x2, y=hlbls,
                        colorscale=[[0,"#ef4444"],[0.25,"#f97316"],[0.5,"#f59e0b"],[0.75,"#84cc16"],[1,"#10b981"]],
                        zmin=0, zmax=1,
                        text=[[f"{raw2[i][j]:.2f}" for j in range(len(hmap_x2))] for i in range(len(hlbls))],
                        texttemplate="%{text}", textfont=dict(size=11, color="white"),
                        hoverinfo="text", hovertext=hover_text2,
                        showscale=True,
                        colorbar=dict(
                            title=dict(text="Level", font=dict(color="#94a3b8", size=11)),
                            tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                            ticktext=["Very Bad 🔴", "Bad 🟠", "OK 🟡", "Good 🟢", "Excellent ✅"],
                            tickfont=dict(size=9, color="#94a3b8"),
                        )
                    ))
                    hh_ly = plotly_bg()
                    hh_ly["xaxis"] = dict(title="Day", tickfont=dict(size=11))
                    hh_ly["yaxis"] = dict(title="", tickfont=dict(size=11))
                    fig_hh.update_layout(**hh_ly, height=300, margin=dict(t=10,b=10,l=140,r=120))
                    st.plotly_chart(fig_hh, use_container_width=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:60px;padding:28px;text-align:center;
            border-top:1px solid rgba(108,99,255,0.1);
            background:linear-gradient(90deg,transparent,rgba(108,99,255,0.03),transparent);">
    <div style="color:#475569;font-size:0.75rem;letter-spacing:2px;font-family:Rajdhani,sans-serif;text-transform:uppercase;">
        <strong style="background:linear-gradient(135deg,#6c63ff,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">WorkloadAI</strong>
        &nbsp;·&nbsp; Pattern Analysis System &nbsp;·&nbsp; Neural Network · Streamlit · Plotly &nbsp;·&nbsp;
        <em style="color:#334155;">Not a medical tool</em>
    </div>
</div>""", unsafe_allow_html=True)