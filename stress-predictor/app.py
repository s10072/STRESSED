import streamlit as st
import numpy as np
from model import train_model

st.set_page_config(page_title="Stress Type Quiz", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'DM Serif Display', serif !important; }
    .hero { text-align: center; padding: 2rem 0 1rem 0; }
    .hero h1 { font-size: 2.8rem; margin-bottom: 0.2rem; letter-spacing: -1px; }
    .hero p { color: #6b7280; font-size: 1rem; margin-top: 0; }
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px; padding: 2rem; color: white;
        text-align: center; margin: 1rem 0;
    }
    .profile-type { font-family: 'DM Serif Display', serif; font-size: 2rem; margin: 0.5rem 0; }
    .qlabel { font-size: 1.05rem; font-weight: 600; margin-bottom: 0.2rem; color: #111; }
    .qhint { font-size: 0.85rem; color: #9ca3af; margin-bottom: 0.4rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_model():
    return train_model()

model, scaler = get_model()

QUESTIONS = [
    {"key": "morning", "label": "1. Describe your typical morning",
     "hint": "e.g. rushed, calm, skip breakfast, check phone immediately...",
     "placeholder": "I usually wake up late and immediately check my phone..."},
    {"key": "sleep", "label": "2. How has your sleep been lately?",
     "hint": "e.g. hours, quality, trouble falling asleep, waking up tired...",
     "placeholder": "I get around 6 hours but wake up feeling exhausted..."},
    {"key": "work", "label": "3. How do you feel about your workload?",
     "hint": "e.g. overwhelmed, bored, balanced, under pressure...",
     "placeholder": "I have deadlines every day and can never fully switch off..."},
    {"key": "body", "label": "4. What does your body feel like at end of day?",
     "hint": "e.g. tense, headaches, energised, physically drained...",
     "placeholder": "My shoulders are always tense and I get headaches often..."},
    {"key": "unwind", "label": "5. How do you unwind after a stressful day?",
     "hint": "e.g. scroll social media, exercise, talk to friends, can't unwind...",
     "placeholder": "I usually scroll my phone for hours before bed..."},
]

def analyse_answers(answers):
    text = " ".join(answers.values()).lower()

    # Keyword scoring
    high_stress = ["overwhelmed", "exhausted", "anxious", "panic", "can't sleep",
                   "rushed", "deadline", "burnout", "tense", "headache", "late",
                   "no time", "stressed", "pressure", "tired", "drained", "never switch off"]
    low_stress  = ["calm", "relaxed", "balanced", "good sleep", "exercise", "meditat",
                   "walk", "friends", "energised", "happy", "fine", "okay", "peaceful"]
    caffeine    = ["coffee", "caffeine", "energy drink", "red bull"]
    social      = ["friends", "family", "talk", "social", "people", "chat"]
    active      = ["gym", "run", "walk", "exercise", "sport", "yoga", "workout"]

    h = sum(1 for w in high_stress if w in text)
    l = sum(1 for w in low_stress  if w in text)
    c = sum(1 for w in caffeine    if w in text)
    s = sum(1 for w in social      if w in text)
    a = sum(1 for w in active      if w in text)

    score = min(10, max(1, 5 + h - l + c - s - a))

    # Determine sleep roughly
    sleep_hrs = 7
    for word, hrs in [("5 hour", 5), ("6 hour", 6), ("4 hour", 4), ("8 hour", 8), ("9 hour", 9)]:
        if word in text: sleep_hrs = hrs

    # ML prediction
    mood_score = max(1, 4 - h + l)
    social_score = min(4, 1 + s)
    activity_min = 30 if a == 0 else 60
    features = np.array([[sleep_hrs, activity_min, c*2, mood_score, 8, social_score]])
    features_scaled = scaler.transform(features)
    ml_pred = model.predict(features_scaled)[0]

    # Pick stress type
    if score >= 8 or h >= 5:
        profile = {
            "emoji": "🔥",
            "type": "The Chronic Overachiever",
            "tagline": "You push hard — but you're running on empty.",
            "description": "You thrive under pressure but rarely give yourself permission to rest. Your mind is always on the next task, and your body is quietly paying the price. You likely mistake busyness for productivity.",
            "strength": "Your drive and resilience are exceptional — you get things done when others give up.",
            "watch_out": "Burnout doesn't announce itself. The crash usually comes right after a big milestone.",
            "tips": ["Block 20 mins of do-nothing time each day — no phone, no tasks.", "Try the 2-minute rule: if it takes under 2 mins, do it now; otherwise schedule it.", "Track your energy, not just your time — notice when you're most focused and protect it."]
        }
    elif score >= 5 or h >= 2:
        profile = {
            "emoji": "🌊",
            "type": "The Silent Stacker",
            "tagline": "Stress builds quietly until it overflows.",
            "description": "You seem fine on the outside, but small pressures accumulate under the surface. You don't always voice when things are too much, and your body absorbs what your mind won't process.",
            "strength": "You're emotionally resilient and handle day-to-day challenges without drama.",
            "watch_out": "Suppressed stress doesn't disappear — it shows up as tension, poor sleep, or sudden overwhelm.",
            "tips": ["Journal for 5 mins before bed — getting thoughts out of your head helps your nervous system settle.", "Name your stress out loud to someone you trust at least once a week.", "Set one hard boundary this week — say no to one thing that drains you."]
        }
    else:
        profile = {
            "emoji": "🌿",
            "type": "The Balanced Navigator",
            "tagline": "You've found your rhythm — protect it.",
            "description": "You have a healthier relationship with stress than most. You likely have routines that ground you and know when to step back. The challenge is maintaining this when life throws curveballs.",
            "strength": "Your self-awareness is your superpower — you know what you need before you hit a wall.",
            "watch_out": "Complacency can creep in. Keep checking in with yourself as pressures change.",
            "tips": ["Share your coping strategies with someone who's struggling — teaching reinforces your own habits.", "Add one new recovery ritual (cold shower, 10-min walk, breathing exercise) to lock in your gains.", "Schedule a monthly stress check-in with yourself to catch drift early."]
        }

    profile["score"] = score
    profile["ml_level"] = ["Low", "Moderate", "High"][ml_pred]
    profile["ml_color"] = ["green", "orange", "red"][ml_pred]
    return profile

# --- State ---
if "step"    not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = {}
if "result"  not in st.session_state: st.session_state.result = None

# --- Hero ---
st.markdown("""
<div class="hero">
    <div style="font-size:2.5rem">🧠</div>
    <h1>What's Your Stress Type?</h1>
    <p>5 questions · ML-powered · Get your personal stress profile</p>
</div>
""", unsafe_allow_html=True)

total   = len(QUESTIONS)
current = st.session_state.step

if st.session_state.result is None:
    if current < total:
        st.progress(current / total, text=f"Question {current + 1} of {total}")
        st.markdown("<br>", unsafe_allow_html=True)

        q = QUESTIONS[current]
        st.markdown(f'<div class="qlabel">{q["label"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="qhint">{q["hint"]}</div>',  unsafe_allow_html=True)

        answer = st.text_area(
            label=q["label"], placeholder=q["placeholder"],
            height=110, label_visibility="collapsed", key=f"input_{current}"
        )

        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("Next →", use_container_width=True, type="primary"):
                if answer.strip():
                    st.session_state.answers[q["key"]] = answer.strip()
                    st.session_state.step += 1
                    st.rerun()
                else:
                    st.warning("Please write something — even a sentence is fine!")
        with col1:
            if current > 0:
                if st.button("← Back", use_container_width=True):
                    st.session_state.step -= 1
                    st.rerun()
    else:
        with st.spinner("Analysing your answers..."):
            st.session_state.result = analyse_answers(st.session_state.answers)
            st.rerun()

else:
    r = st.session_state.result
    score = r["score"]
    color = "#22c55e" if score <= 3 else "#f59e0b" if score <= 6 else "#ef4444"

    st.markdown(f"""
    <div class="profile-card">
        <div style="font-size:3rem">{r["emoji"]}</div>
        <div class="profile-type">{r["type"]}</div>
        <div style="opacity:0.85; font-size:1rem; margin-top:0.3rem">{r["tagline"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Stress level**")
    ml = r["ml_level"]
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem">
        <div style="flex:1; background:#f3f4f6; border-radius:99px; height:12px; overflow:hidden">
            <div style="width:{score*10}%; background:{color}; height:100%; border-radius:99px"></div>
        </div>
        <div style="font-size:1.2rem; font-weight:700; color:{color}">{score}/10 · {ml}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**About you**")
    st.markdown(r["description"])

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"💪 **Strength**\n\n{r['strength']}")
    with col2:
        st.warning(f"⚠️ **Watch out for**\n\n{r['watch_out']}")

    st.markdown("**Your 3 personalised tips**")
    for i, tip in enumerate(r["tips"], 1):
        st.info(f"**{i}.** {tip}")

    st.divider()
    if st.button("🔄 Retake the quiz", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.result = None
        st.rerun()
