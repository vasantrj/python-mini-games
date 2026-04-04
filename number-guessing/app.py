import streamlit as st
import random
import time

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎯",
    layout="centered",
)

# ── Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .main { background-color: #0f0f0f; }

    .game-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        color: #c8f135;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .game-subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-top: 4px;
        margin-bottom: 28px;
    }

    .stat-box {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
    }

    .stat-label {
        color: #666;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stat-value {
        color: #c8f135;
        font-size: 1.6rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .hint-box {
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 1.05rem;
        font-weight: 600;
        text-align: center;
        margin: 16px 0;
    }

    .hint-high  { background: #2a1a1a; border: 1px solid #ff4b4b; color: #ff4b4b; }
    .hint-low   { background: #1a1f2a; border: 1px solid #4b9fff; color: #4b9fff; }
    .hint-win   { background: #1a2a1a; border: 1px solid #c8f135; color: #c8f135; }
    .hint-lose  { background: #2a1a1a; border: 1px solid #ff6b35; color: #ff6b35; }

    .history-pill {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.82rem;
        color: #aaa;
        margin: 3px;
    }

    .stButton > button {
        background: #c8f135 !important;
        color: #0f0f0f !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-size: 1rem !important;
        transition: opacity 0.2s !important;
    }

    .stButton > button:hover { opacity: 0.85 !important; }

    div[data-testid="stNumberInput"] input {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #fff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.1rem !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Difficulty settings ─────────────────────────────────────────────
DIFFICULTIES = {
    "Easy":   {"range": (1, 50),  "max_guesses": 10, "emoji": "🟢"},
    "Medium": {"range": (1, 100), "max_guesses": 7,  "emoji": "🟡"},
    "Hard":   {"range": (1, 200), "max_guesses": 5,  "emoji": "🔴"},
}

# ── Session state init ──────────────────────────────────────────────
def init_state(difficulty="Medium"):
    cfg = DIFFICULTIES[difficulty]
    lo, hi = cfg["range"]
    st.session_state.update({
        "secret":       random.randint(lo, hi),
        "guesses_left": cfg["max_guesses"],
        "max_guesses":  cfg["max_guesses"],
        "history":      [],
        "game_over":    False,
        "won":          False,
        "difficulty":   difficulty,
        "range":        cfg["range"],
        "total_games":  st.session_state.get("total_games", 0),
        "wins":         st.session_state.get("wins", 0),
        "best_score":   st.session_state.get("best_score", None),
    })

if "secret" not in st.session_state:
    init_state()

# ── Header ──────────────────────────────────────────────────────────
st.markdown('<p class="game-title">🎯 Number Guesser</p>', unsafe_allow_html=True)
st.markdown('<p class="game-subtitle">Can you crack the number before you run out of guesses?</p>', unsafe_allow_html=True)

# ── Stats row ───────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
lo, hi = st.session_state.range

with c1:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-label">Range</div>
        <div class="stat-value">{lo}–{hi}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    gl = st.session_state.guesses_left
    color = "#c8f135" if gl > 3 else "#ff4b4b"
    st.markdown(f"""<div class="stat-box">
        <div class="stat-label">Guesses Left</div>
        <div class="stat-value" style="color:{color}">{gl}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    win_rate = (
        f"{int(st.session_state.wins / st.session_state.total_games * 100)}%"
        if st.session_state.total_games > 0 else "—"
    )
    st.markdown(f"""<div class="stat-box">
        <div class="stat-label">Win Rate</div>
        <div class="stat-value">{win_rate}</div>
    </div>""", unsafe_allow_html=True)

with c4:
    best = st.session_state.best_score if st.session_state.best_score else "—"
    st.markdown(f"""<div class="stat-box">
        <div class="stat-label">Best (fewest)</div>
        <div class="stat-value">{best}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Difficulty selector (only before game starts) ───────────────────
if not st.session_state.history and not st.session_state.game_over:
    diff_choice = st.selectbox(
        "Select Difficulty",
        list(DIFFICULTIES.keys()),
        index=list(DIFFICULTIES.keys()).index(st.session_state.difficulty),
        format_func=lambda d: f"{DIFFICULTIES[d]['emoji']}  {d}  —  "
                              f"{DIFFICULTIES[d]['range'][0]}–{DIFFICULTIES[d]['range'][1]}, "
                              f"{DIFFICULTIES[d]['max_guesses']} guesses",
    )
    if diff_choice != st.session_state.difficulty:
        init_state(diff_choice)
        st.rerun()

# ── Hint display ────────────────────────────────────────────────────
if st.session_state.history:
    last = st.session_state.history[-1]
    if st.session_state.won:
        guesses_used = st.session_state.max_guesses - st.session_state.guesses_left
        st.markdown(
            f'<div class="hint-box hint-win">🎉 Correct! The number was <strong>{st.session_state.secret}</strong> — found in {guesses_used} guess{"es" if guesses_used > 1 else ""}!</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.game_over and not st.session_state.won:
        st.markdown(
            f'<div class="hint-box hint-lose">💀 Out of guesses! The number was <strong>{st.session_state.secret}</strong>. Better luck next time!</div>',
            unsafe_allow_html=True,
        )
    elif last > st.session_state.secret:
        gap = last - st.session_state.secret
        hint = "Way too high! 🔥🔥" if gap > 20 else "A bit high ↓"
        st.markdown(f'<div class="hint-box hint-high">📈 {last} — {hint}</div>', unsafe_allow_html=True)
    else:
        gap = st.session_state.secret - last
        hint = "Way too low! 🧊🧊" if gap > 20 else "A bit low ↑"
        st.markdown(f'<div class="hint-box hint-low">📉 {last} — {hint}</div>', unsafe_allow_html=True)

# ── Input & guess button ────────────────────────────────────────────
if not st.session_state.game_over:
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        guess = st.number_input(
            f"Enter a number between {lo} and {hi}",
            min_value=lo,
            max_value=hi,
            step=1,
            key="guess_input",
            label_visibility="collapsed",
        )
    with col_btn:
        submit = st.button("Guess →", use_container_width=True)

    if submit:
        if guess in st.session_state.history:
            st.warning(f"You already guessed {guess}! Try a different number.")
        else:
            st.session_state.history.append(guess)
            st.session_state.guesses_left -= 1

            if guess == st.session_state.secret:
                st.session_state.game_over = True
                st.session_state.won = True
                st.session_state.total_games += 1
                st.session_state.wins += 1
                guesses_used = st.session_state.max_guesses - st.session_state.guesses_left
                if st.session_state.best_score is None or guesses_used < st.session_state.best_score:
                    st.session_state.best_score = guesses_used
            elif st.session_state.guesses_left == 0:
                st.session_state.game_over = True
                st.session_state.total_games += 1

            st.rerun()

# ── Guess history ───────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<br>**Your guesses:**", unsafe_allow_html=True)
    pills = "".join(
        f'<span class="history-pill">{"✅" if g == st.session_state.secret else "❌"} {g}</span>'
        for g in st.session_state.history
    )
    st.markdown(f"<div>{pills}</div>", unsafe_allow_html=True)

# ── Progress bar ────────────────────────────────────────────────────
if st.session_state.history and not st.session_state.game_over:
    used = len(st.session_state.history)
    total = st.session_state.max_guesses
    st.progress(used / total, text=f"{used}/{total} guesses used")

# ── Play again ──────────────────────────────────────────────────────
if st.session_state.game_over:
    st.markdown("<br>", unsafe_allow_html=True)
    col_r, col_d = st.columns(2)
    with col_r:
        if st.button("🔄  Play Again (same difficulty)", use_container_width=True):
            diff = st.session_state.difficulty
            wins = st.session_state.wins
            total = st.session_state.total_games
            best = st.session_state.best_score
            init_state(diff)
            st.session_state.wins = wins
            st.session_state.total_games = total
            st.session_state.best_score = best
            st.rerun()
    with col_d:
        if st.button("🎚️  Change Difficulty", use_container_width=True):
            wins = st.session_state.wins
            total = st.session_state.total_games
            best = st.session_state.best_score
            init_state("Medium")
            st.session_state.wins = wins
            st.session_state.total_games = total
            st.session_state.best_score = best
            st.rerun()

# ── Footer ──────────────────────────────────────────────────────────
st.markdown("<br><hr style='border-color:#1e1e1e'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#444;font-size:0.8rem;'>Part of <strong style='color:#666'>python-mini-games</strong> by Vasant</p>",
    unsafe_allow_html=True,
)
