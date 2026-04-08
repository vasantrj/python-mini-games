import streamlit as st
import random
import time

# ─────────────────────────────────────────────────────────────────────────────
# QUESTION BANK
# ─────────────────────────────────────────────────────────────────────────────
ALL_QUESTIONS = [
    # Science
    {"q": "What is the chemical symbol for gold?",
     "opts": ["Au","Ag","Gd","Go"], "ans": "Au", "cat": "Science"},
    {"q": "How many bones are in the adult human body?",
     "opts": ["206","186","256","196"], "ans": "206", "cat": "Science"},
    {"q": "What planet is known as the Red Planet?",
     "opts": ["Venus","Jupiter","Mars","Saturn"], "ans": "Mars", "cat": "Science"},
    {"q": "What is the speed of light (approx) in km/s?",
     "opts": ["300,000","150,000","450,000","30,000"], "ans": "300,000", "cat": "Science"},
    {"q": "Which gas do plants absorb during photosynthesis?",
     "opts": ["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"], "ans": "Carbon Dioxide", "cat": "Science"},
    {"q": "What is the powerhouse of the cell?",
     "opts": ["Nucleus","Ribosome","Mitochondria","Golgi Body"], "ans": "Mitochondria", "cat": "Science"},
    # History
    {"q": "In which year did World War II end?",
     "opts": ["1943","1944","1945","1946"], "ans": "1945", "cat": "History"},
    {"q": "Who was the first person to walk on the Moon?",
     "opts": ["Buzz Aldrin","Yuri Gagarin","Neil Armstrong","Alan Shepard"], "ans": "Neil Armstrong", "cat": "History"},
    {"q": "The Berlin Wall fell in which year?",
     "opts": ["1987","1989","1991","1993"], "ans": "1989", "cat": "History"},
    {"q": "Which empire was ruled by Genghis Khan?",
     "opts": ["Ottoman","Roman","Mongol","Persian"], "ans": "Mongol", "cat": "History"},
    {"q": "Who invented the telephone?",
     "opts": ["Edison","Tesla","Bell","Marconi"], "ans": "Bell", "cat": "History"},
    # Geography
    {"q": "What is the longest river in the world?",
     "opts": ["Amazon","Yangtze","Mississippi","Nile"], "ans": "Nile", "cat": "Geography"},
    {"q": "Which country has the most natural lakes?",
     "opts": ["Russia","USA","Brazil","Canada"], "ans": "Canada", "cat": "Geography"},
    {"q": "What is the capital of Australia?",
     "opts": ["Sydney","Melbourne","Canberra","Perth"], "ans": "Canberra", "cat": "Geography"},
    {"q": "Mount Everest is part of which mountain range?",
     "opts": ["Andes","Alps","Rockies","Himalayas"], "ans": "Himalayas", "cat": "Geography"},
    # Tech
    {"q": "What does 'HTTP' stand for?",
     "opts": ["HyperText Transfer Protocol","High Transfer Text Protocol",
              "HyperText Transmission Process","Hosted Transfer Text Protocol"],
     "ans": "HyperText Transfer Protocol", "cat": "Tech"},
    {"q": "Who co-founded Apple with Steve Jobs?",
     "opts": ["Bill Gates","Steve Wozniak","Paul Allen","Larry Page"], "ans": "Steve Wozniak", "cat": "Tech"},
    {"q": "Which language is known as the backbone of the web?",
     "opts": ["Python","Java","JavaScript","C++"], "ans": "JavaScript", "cat": "Tech"},
    {"q": "What does 'CPU' stand for?",
     "opts": ["Core Processing Unit","Central Processing Unit",
              "Computer Processing Unit","Central Program Unit"],
     "ans": "Central Processing Unit", "cat": "Tech"},
    # Pop Culture
    {"q": "How many Academy Awards did 'Titanic' (1997) win?",
     "opts": ["9","11","14","7"], "ans": "11", "cat": "Pop Culture"},
    {"q": "Which band performed 'Bohemian Rhapsody'?",
     "opts": ["Led Zeppelin","The Beatles","Queen","Pink Floyd"], "ans": "Queen", "cat": "Pop Culture"},
    {"q": "What fictional country is Black Panther's home?",
     "opts": ["Sokovia","Wakanda","Kahndaq","Latveria"], "ans": "Wakanda", "cat": "Pop Culture"},
]

LABELS = ["A", "B", "C", "D"]
TOTAL_Q = 10
TIME_PER_Q = 15  # seconds


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def start_game():
    questions = random.sample(ALL_QUESTIONS, TOTAL_Q)
    for q in questions:
        shuffled = q["opts"][:]
        random.shuffle(shuffled)
        q["shuffled"] = shuffled
    wins   = st.session_state.get("wins", 0)
    played = st.session_state.get("played", 0)
    best   = st.session_state.get("best", 0)
    st.session_state.update({
        "questions":  questions,
        "current":    0,
        "score":      0,
        "phase":      "playing",   # playing | feedback | results
        "chosen":     None,
        "start_time": time.time(),
        "timed_out":  False,
        "wins":       wins,
        "played":     played,
        "best":       best,
    })

if "phase" not in st.session_state:
    start_game()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Quiz Show", page_icon="📺", layout="centered")


# ─────────────────────────────────────────────────────────────────────────────
# CSS  —  Retro CRT / Late-night game show
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&display=swap');

:root {
    --bg:        #07090f;
    --screen:    #0b0f1c;
    --border:    #1c2340;
    --amber:     #f5b800;
    --amber-dim: #a07a00;
    --green:     #00e676;
    --red:       #ff3d3d;
    --text:      #dde3f5;
    --muted:     #4a5270;
    --scanline:  rgba(0,0,0,0.18);
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--bg) !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--text) !important;
}

[data-testid="stHeader"],
[data-testid="stDecoration"],
#MainMenu, footer { display: none !important; }

/* ── CRT screen wrapper ── */
.crt {
    background: var(--screen);
    border: 3px solid var(--border);
    border-radius: 18px;
    box-shadow:
        0 0 0 1px #0d1120,
        0 0 30px rgba(245,184,0,0.08),
        0 0 80px rgba(245,184,0,0.04),
        inset 0 0 40px rgba(0,0,0,0.6);
    padding: 36px 32px 32px;
    position: relative;
    overflow: hidden;
}

/* scanlines */
.crt::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        to bottom,
        var(--scanline) 0px,
        var(--scanline) 1px,
        transparent 1px,
        transparent 3px
    );
    pointer-events: none;
    z-index: 10;
    border-radius: 16px;
}

/* vignette */
.crt::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center,
        transparent 55%,
        rgba(0,0,0,0.55) 100%);
    pointer-events: none;
    z-index: 11;
    border-radius: 16px;
}

/* ── Show title ── */
.show-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    color: var(--amber);
    letter-spacing: 6px;
    text-align: center;
    line-height: 1;
    text-shadow:
        0 0 12px rgba(245,184,0,0.6),
        0 0 30px rgba(245,184,0,0.2);
    margin-bottom: 2px;
}

.show-tagline {
    text-align: center;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 28px;
}

/* ── Top bar ── */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
}

.q-counter {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: var(--muted);
    letter-spacing: 2px;
}

.q-counter span { color: var(--amber); }

.cat-badge {
    font-size: 0.68rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--amber-dim);
    border: 1px solid var(--amber-dim);
    padding: 3px 10px;
    border-radius: 2px;
}

.score-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: var(--text);
    letter-spacing: 2px;
}

.score-display span { color: var(--green); }

/* ── Timer bar ── */
.timer-track {
    background: var(--border);
    height: 4px;
    border-radius: 2px;
    margin-bottom: 24px;
    overflow: hidden;
}

.timer-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s linear, background 1s;
}

/* ── Question ── */
.question-text {
    font-size: 1.18rem;
    color: var(--text);
    line-height: 1.65;
    margin-bottom: 28px;
    min-height: 60px;
    letter-spacing: 0.3px;
}

/* ── Answer option rows ── */
.opt-row {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px 16px;
    margin-bottom: 9px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
    font-size: 0.97rem;
    letter-spacing: 0.2px;
    color: var(--text);
}

.opt-row:hover {
    border-color: var(--amber-dim);
    background: rgba(245,184,0,0.06);
}

.opt-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.15rem;
    color: var(--amber);
    min-width: 22px;
    letter-spacing: 1px;
}

/* feedback states */
.opt-correct {
    border-color: var(--green) !important;
    background: rgba(0,230,118,0.08) !important;
    color: var(--green) !important;
}

.opt-correct .opt-label { color: var(--green) !important; }

.opt-wrong {
    border-color: var(--red) !important;
    background: rgba(255,61,61,0.08) !important;
    color: var(--red) !important;
}

.opt-wrong .opt-label { color: var(--red) !important; }

.opt-dim {
    opacity: 0.3;
}

/* ── Feedback banner ── */
.feedback-msg {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 3px;
    text-align: center;
    padding: 10px 0 16px;
}

.fb-correct { color: var(--green); text-shadow: 0 0 18px rgba(0,230,118,0.4); }
.fb-wrong   { color: var(--red);   text-shadow: 0 0 18px rgba(255,61,61,0.35); }
.fb-timeout { color: var(--amber); text-shadow: 0 0 18px rgba(245,184,0,0.35); }

/* ── Results screen ── */
.results-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    color: var(--amber);
    text-align: center;
    line-height: 1;
    text-shadow:
        0 0 20px rgba(245,184,0,0.5),
        0 0 50px rgba(245,184,0,0.15);
    letter-spacing: 4px;
}

.results-label {
    text-align: center;
    font-size: 0.72rem;
    letter-spacing: 5px;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 4px;
    margin-bottom: 28px;
}

.results-verdict {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 4px;
    text-align: center;
    margin-bottom: 8px;
}

.stat-row {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin: 20px 0 28px;
}

.stat-col { text-align: center; }
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: var(--text);
    line-height: 1;
}
.stat-key {
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
}

/* ── Streamlit button override ── */
.stButton > button {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 3px !important;
    background: transparent !important;
    color: var(--amber) !important;
    border: 2px solid var(--amber-dim) !important;
    border-radius: 3px !important;
    padding: 10px 32px !important;
    transition: all 0.15s !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: rgba(245,184,0,0.1) !important;
    border-color: var(--amber) !important;
    box-shadow: 0 0 16px rgba(245,184,0,0.2) !important;
}

/* Progress dots */
.dot-row {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin-bottom: 24px;
}

.pdot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
}
.pdot.done-right { background: var(--green); }
.pdot.done-wrong { background: var(--red); }
.pdot.active     { background: var(--amber); box-shadow: 0 0 6px var(--amber); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: render option rows as HTML
# ─────────────────────────────────────────────────────────────────────────────
def render_options_html(opts, chosen, correct_ans, phase):
    rows = []
    for i, opt in enumerate(opts):
        label = LABELS[i]
        if phase == "feedback":
            if opt == correct_ans:
                cls = "opt-row opt-correct"
            elif opt == chosen:
                cls = "opt-row opt-wrong"
            else:
                cls = "opt-row opt-dim"
        else:
            cls = "opt-row"
        rows.append(
            f'<div class="{cls}">'
            f'<span class="opt-label">{label}</span>'
            f'<span>{opt}</span>'
            f'</div>'
        )
    return "\n".join(rows)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN RENDER
# ─────────────────────────────────────────────────────────────────────────────
phase = st.session_state.phase

# ── RESULTS SCREEN ────────────────────────────────────────────────────────────
if phase == "results":
    score  = st.session_state.score
    played = st.session_state.played
    best   = st.session_state.best
    pct    = int(score / TOTAL_Q * 100)

    if   pct == 100: verdict, vcls = "PERFECT SCORE !", "fb-correct"
    elif pct >= 80:  verdict, vcls = "OUTSTANDING",     "fb-correct"
    elif pct >= 60:  verdict, vcls = "SOLID ROUND",     "fb-correct"
    elif pct >= 40:  verdict, vcls = "NEEDS WORK",      "fb-timeout"
    else:            verdict, vcls = "BETTER LUCK NEXT TIME", "fb-wrong"

    st.markdown('<div class="crt">', unsafe_allow_html=True)
    st.markdown('<p class="show-title">QUIZ SHOW</p>', unsafe_allow_html=True)

    st.markdown(f'<div class="results-score">{score}<span style="font-size:2.5rem;color:var(--muted)">/{TOTAL_Q}</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="results-label">final score</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="results-verdict {vcls}">{verdict}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-col">
        <div class="stat-num">{pct}%</div>
        <div class="stat-key">Accuracy</div>
      </div>
      <div class="stat-col">
        <div class="stat-num">{played}</div>
        <div class="stat-key">Games</div>
      </div>
      <div class="stat-col">
        <div class="stat-num">{best}</div>
        <div class="stat-key">Best</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶  PLAY AGAIN"):
        start_game()
        st.rerun()

    st.markdown("""
    <p style='text-align:center;color:#1c2340;font-family:Share Tech Mono,monospace;
       font-size:0.8rem;margin-top:24px;'>python-mini-games · vasant</p>
    """, unsafe_allow_html=True)
    st.stop()


# ── PLAYING / FEEDBACK ────────────────────────────────────────────────────────
questions   = st.session_state.questions
idx         = st.session_state.current
q           = questions[idx]
opts        = q["shuffled"]
correct_ans = q["ans"]
chosen      = st.session_state.chosen
timed_out   = st.session_state.timed_out

# Timer logic
elapsed     = time.time() - st.session_state.start_time
remaining   = max(0, TIME_PER_Q - elapsed)
timer_pct   = remaining / TIME_PER_Q
timer_color = "#00e676" if timer_pct > 0.5 else ("#f5b800" if timer_pct > 0.25 else "#ff3d3d")

# Auto timeout
if phase == "playing" and remaining == 0 and not timed_out:
    st.session_state.timed_out = True
    st.session_state.phase     = "feedback"
    st.rerun()

# ── CRT open ──
st.markdown('<div class="crt">', unsafe_allow_html=True)

# Title
st.markdown('<p class="show-title">QUIZ SHOW</p>', unsafe_allow_html=True)
st.markdown('<p class="show-tagline">10 questions · 4 categories · 15 seconds each</p>', unsafe_allow_html=True)

# Progress dots
dots = []
history = st.session_state.get("history", [])
for i in range(TOTAL_Q):
    if i < len(history):
        cls = "pdot done-right" if history[i] else "pdot done-wrong"
    elif i == idx:
        cls = "pdot active"
    else:
        cls = "pdot"
    dots.append(f'<div class="{cls}"></div>')
st.markdown(f'<div class="dot-row">{"".join(dots)}</div>', unsafe_allow_html=True)

# Top bar
st.markdown(f"""
<div class="top-bar">
  <div class="q-counter">Q <span>{idx+1:02d}</span> / {TOTAL_Q:02d}</div>
  <div class="cat-badge">{q["cat"]}</div>
  <div class="score-display">SCORE &nbsp;<span>{st.session_state.score}</span></div>
</div>
""", unsafe_allow_html=True)

# Timer bar (only while playing)
if phase == "playing":
    st.markdown(f"""
    <div class="timer-track">
      <div class="timer-fill" style="width:{timer_pct*100:.1f}%;background:{timer_color};"></div>
    </div>
    """, unsafe_allow_html=True)

# Question
st.markdown(f'<div class="question-text">{q["q"]}</div>', unsafe_allow_html=True)

# ── Options ───────────────────────────────────────────────────────────────────
if phase == "playing":
    # Render as clickable Streamlit buttons (one per row)
    for i, opt in enumerate(opts):
        if st.button(f"{LABELS[i]}  ·  {opt}", key=f"opt_{i}"):
            st.session_state.chosen = opt
            st.session_state.phase  = "feedback"
            correct = (opt == correct_ans)
            if correct:
                st.session_state.score += 1
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(correct)
            st.rerun()

    # Override button style for answer opts — inline
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"]
    .stButton > button {
        text-align: left !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.96rem !important;
        letter-spacing: 0.5px !important;
        color: var(--text) !important;
        border-color: #1c2340 !important;
        padding: 12px 18px !important;
        justify-content: flex-start !important;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"]
    .stButton > button:hover {
        border-color: var(--amber-dim) !important;
        background: rgba(245,184,0,0.05) !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

else:
    # Feedback phase: show colored HTML rows
    st.markdown(render_options_html(opts, chosen, correct_ans, "feedback"), unsafe_allow_html=True)

    # Feedback message
    if timed_out:
        msg, cls = f"⏱  TIME'S UP — IT WAS {correct_ans.upper()}", "fb-timeout"
    elif chosen == correct_ans:
        msg, cls = "✓  CORRECT !", "fb-correct"
    else:
        msg, cls = f"✗  WRONG — IT WAS {correct_ans.upper()}", "fb-wrong"

    st.markdown(f'<div class="feedback-msg {cls}">{msg}</div>', unsafe_allow_html=True)

# ── CRT close ──
st.markdown("</div>", unsafe_allow_html=True)

# ── Next / Finish button ──────────────────────────────────────────────────────
if phase == "feedback":
    st.markdown("<br>", unsafe_allow_html=True)
    is_last = (idx + 1 >= TOTAL_Q)
    label   = "▶  SEE RESULTS" if is_last else "▶  NEXT QUESTION"
    if st.button(label):
        if is_last:
            score  = st.session_state.score
            played = st.session_state.played + 1
            best   = max(st.session_state.best, score)
            st.session_state.played  = played
            st.session_state.best    = best
            st.session_state.phase   = "results"
        else:
            st.session_state.current   += 1
            st.session_state.chosen     = None
            st.session_state.timed_out  = False
            st.session_state.phase      = "playing"
            st.session_state.start_time = time.time()
        st.rerun()
elif phase == "playing":
    # Auto-refresh every second for timer
    time.sleep(1)
    st.rerun()

# Footer
st.markdown("""
<p style='text-align:center;color:#12172a;font-family:Share Tech Mono,monospace;
   font-size:0.78rem;margin-top:20px;'>python-mini-games · vasant</p>
""", unsafe_allow_html=True)
