import streamlit as st
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hangman",
    page_icon="💀",
    layout="centered",
)

# ── Word bank by category ─────────────────────────────────────────────────────
WORD_BANK = {
    "🐍 Python": [
        "generator", "decorator", "comprehension", "iterator", "recursion",
        "inheritance", "polymorphism", "encapsulation", "abstraction", "lambda",
        "dictionary", "exception", "virtualenv", "dataclass", "asyncio",
    ],
    "🧠 Data Science": [
        "overfitting", "normalization", "gradient", "backpropagation", "clustering",
        "regression", "precision", "confusion", "validation", "dimensionality",
        "imputation", "ensemble", "bootstrapping", "hyperparameter", "tokenization",
    ],
    "💻 CS Concepts": [
        "recursion", "hashing", "traversal", "complexity", "concurrency",
        "deadlock", "semaphore", "polymorphism", "abstraction", "encapsulation",
        "idempotent", "throughput", "latency", "scalability", "microservice",
    ],
    "🌐 General": [
        "programming", "algorithm", "database", "framework", "repository",
        "deployment", "debugging", "refactoring", "documentation", "abstraction",
        "integration", "authentication", "authorization", "middleware", "serialization",
    ],
}

MAX_WRONG = 6

# Hangman ASCII stages
HANGMAN_STAGES = [
    # 0 wrong
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    # 1 wrong
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    # 2 wrong
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    # 3 wrong
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    # 4 wrong
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    # 5 wrong
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    # 6 wrong - dead
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========""",
]

# ── Custom CSS — retro phosphor terminal aesthetic ────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Share Tech Mono', monospace;
        background-color: #050a05 !important;
    }

    .main, .block-container {
        background-color: #050a05 !important;
    }

    /* Scanline overlay */
    .main::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0,255,70,0.015) 2px,
            rgba(0,255,70,0.015) 4px
        );
        pointer-events: none;
        z-index: 9999;
    }

    .game-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.6rem;
        font-weight: 900;
        color: #00ff46;
        text-align: center;
        letter-spacing: 6px;
        text-shadow: 0 0 20px #00ff4688, 0 0 40px #00ff4644;
        margin-bottom: 2px;
        animation: flicker 5s infinite;
    }

    @keyframes flicker {
        0%,95%,100% { opacity: 1; }
        96% { opacity: 0.85; }
        97% { opacity: 1; }
        98% { opacity: 0.9; }
    }

    .game-subtitle {
        text-align: center;
        color: #2a6e38;
        font-size: 0.78rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 24px;
    }

    .ascii-art {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.95rem;
        color: #00ff46;
        text-shadow: 0 0 8px #00ff4666;
        background: #020802;
        border: 1px solid #0a3010;
        border-radius: 8px;
        padding: 16px 24px;
        line-height: 1.4;
        white-space: pre;
        text-align: left;
    }

    .word-display {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        letter-spacing: 10px;
        color: #00ff46;
        text-shadow: 0 0 10px #00ff4688;
        text-align: center;
        padding: 18px 0;
        border-bottom: 1px solid #0a3010;
        border-top: 1px solid #0a3010;
        margin: 16px 0;
    }

    .wrong-letters {
        color: #ff3b3b;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.05rem;
        text-shadow: 0 0 8px #ff3b3b88;
        letter-spacing: 6px;
        text-align: center;
    }

    .hint-box {
        border-radius: 6px;
        padding: 12px 18px;
        font-size: 0.85rem;
        text-align: center;
        letter-spacing: 1px;
        margin: 10px 0;
        font-family: 'Share Tech Mono', monospace;
    }
    .hint-win  { background: #021a08; border: 1px solid #00ff46; color: #00ff46; text-shadow: 0 0 6px #00ff4666; }
    .hint-lose { background: #1a0202; border: 1px solid #ff3b3b; color: #ff3b3b; text-shadow: 0 0 6px #ff3b3b66; }
    .hint-info { background: #020e1a; border: 1px solid #00aaff; color: #00aaff; }

    .stat-box {
        background: #020802;
        border: 1px solid #0a3010;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }
    .stat-label { color: #2a6e38; font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; }
    .stat-value { color: #00ff46; font-size: 1.4rem; font-weight: 700; text-shadow: 0 0 8px #00ff4666; }

    /* Alphabet keyboard */
    .kb-row { display: flex; justify-content: center; gap: 6px; margin: 4px 0; flex-wrap: wrap; }

    .kb-btn {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        width: 36px; height: 36px;
        border-radius: 4px;
        border: 1px solid #0a3010;
        background: #020802;
        color: #00ff46;
        cursor: pointer;
        transition: all 0.15s;
        text-shadow: 0 0 5px #00ff4666;
    }
    .kb-btn:hover:not(:disabled) { background: #0a3010; box-shadow: 0 0 10px #00ff4644; }
    .kb-btn.correct { background: #021a08; border-color: #00ff46; color: #00ff46; }
    .kb-btn.wrong   { background: #1a0202; border-color: #3b0000; color: #3b0000; text-decoration: line-through; cursor: not-allowed; }

    /* Override streamlit buttons */
    .stButton > button {
        background: #020802 !important;
        color: #00ff46 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border: 1px solid #0a3010 !important;
        border-radius: 4px !important;
        letter-spacing: 2px !important;
        font-size: 0.85rem !important;
        transition: all 0.2s !important;
        text-transform: uppercase !important;
    }
    .stButton > button:hover { background: #0a3010 !important; box-shadow: 0 0 12px #00ff4633 !important; }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #020802 !important;
        border: 1px solid #0a3010 !important;
        color: #00ff46 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    div[data-testid="stSelectbox"] label { color: #2a6e38 !important; font-size: 0.75rem; letter-spacing: 2px; }

    hr { border-color: #0a3010 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
def init_game(category=None):
    if category is None:
        category = random.choice(list(WORD_BANK.keys()))
    word = random.choice(WORD_BANK[category]).upper()
    st.session_state.update({
        "word":         word,
        "category":     category,
        "guessed":      set(),
        "wrong_count":  0,
        "game_over":    False,
        "won":          False,
        "total_games":  st.session_state.get("total_games", 0),
        "wins":         st.session_state.get("wins", 0),
        "streak":       st.session_state.get("streak", 0),
    })

if "word" not in st.session_state:
    init_game()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="game-title">HANGMAN</p>', unsafe_allow_html=True)
st.markdown('<p class="game-subtitle">[ guess the word · save the prisoner ]</p>', unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
stats = [
    ("GAMES",   st.session_state.get("total_games", 0)),
    ("WINS",    st.session_state.get("wins", 0)),
    ("STREAK",  st.session_state.get("streak", 0)),
    ("LIVES",   MAX_WRONG - st.session_state.wrong_count),
]
for col, (label, val) in zip([c1, c2, c3, c4], stats):
    color = "#ff3b3b" if label == "LIVES" and val <= 2 else "#00ff46"
    col.markdown(f"""<div class="stat-box">
        <div class="stat-label">{label}</div>
        <div class="stat-value" style="color:{color}">{val}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main layout: ASCII art + word ─────────────────────────────────────────────
left, right = st.columns([1, 1.4])

with left:
    stage = HANGMAN_STAGES[st.session_state.wrong_count]
    st.markdown(f'<div class="ascii-art">{stage}</div>', unsafe_allow_html=True)

with right:
    # Category hint
    st.markdown(f'<div class="hint-info hint-box">CATEGORY: {st.session_state.category}</div>', unsafe_allow_html=True)

    # Word display
    word = st.session_state.word
    displayed = " ".join(
        letter if letter in st.session_state.guessed else "_"
        for letter in word
    )
    st.markdown(f'<div class="word-display">{displayed}</div>', unsafe_allow_html=True)

    # Wrong letters
    wrong_letters = sorted(
        l for l in st.session_state.guessed if l not in word
    )
    if wrong_letters:
        st.markdown(
            f'<div class="wrong-letters">✗ &nbsp; {" ".join(wrong_letters)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="wrong-letters">&nbsp;</div>', unsafe_allow_html=True)

    # Progress bar
    lives_used = st.session_state.wrong_count
    st.progress(lives_used / MAX_WRONG,
                text=f"{MAX_WRONG - lives_used} / {MAX_WRONG} lives remaining")

# ── Win / Lose message ────────────────────────────────────────────────────────
if st.session_state.game_over:
    if st.session_state.won:
        st.markdown(
            f'<div class="hint-box hint-win">✔ CORRECT! THE WORD WAS &nbsp;<strong>{word}</strong>&nbsp; — PRISONER FREED!</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="hint-box hint-lose">✘ GAME OVER. THE WORD WAS &nbsp;<strong>{word}</strong>&nbsp; — PRISONER EXECUTED.</div>',
            unsafe_allow_html=True,
        )

# ── On-screen keyboard ────────────────────────────────────────────────────────
if not st.session_state.game_over:
    st.markdown("<br>", unsafe_allow_html=True)

    # Build keyboard rows
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    for row in rows:
        cols = st.columns(len(row))
        for col, letter in zip(cols, row):
            with col:
                already_guessed = letter in st.session_state.guessed
                label = letter
                if already_guessed:
                    label = f"~~{letter}~~" if letter not in word else f"**{letter}**"
                if st.button(
                    letter,
                    key=f"kb_{letter}",
                    disabled=already_guessed,
                    use_container_width=True,
                ):
                    st.session_state.guessed.add(letter)
                    if letter not in word:
                        st.session_state.wrong_count += 1

                    # Check win
                    if all(l in st.session_state.guessed for l in word):
                        st.session_state.game_over = True
                        st.session_state.won = True
                        st.session_state.total_games += 1
                        st.session_state.wins += 1
                        st.session_state.streak += 1

                    # Check lose
                    elif st.session_state.wrong_count >= MAX_WRONG:
                        st.session_state.game_over = True
                        st.session_state.total_games += 1
                        st.session_state.streak = 0

                    st.rerun()

# ── New game controls ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.game_over:
    cat_choice = st.selectbox(
        "NEXT CATEGORY",
        ["🎲 RANDOM"] + list(WORD_BANK.keys()),
        key="cat_select",
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶  PLAY AGAIN", use_container_width=True):
            wins = st.session_state.wins
            total = st.session_state.total_games
            streak = st.session_state.streak
            chosen = None if cat_choice == "🎲 RANDOM" else cat_choice
            init_game(chosen)
            st.session_state.wins = wins
            st.session_state.total_games = total
            st.session_state.streak = streak
            st.rerun()
    with col2:
        if st.button("↺  RESET STATS", use_container_width=True):
            for k in ["total_games", "wins", "streak"]:
                st.session_state[k] = 0
            init_game()
            st.rerun()
else:
    cat_choice = st.selectbox(
        "SWITCH CATEGORY (starts new game)",
        ["— keep current —"] + list(WORD_BANK.keys()),
        key="cat_mid",
    )
    if cat_choice != "— keep current —":
        wins = st.session_state.wins
        total = st.session_state.total_games
        streak = st.session_state.streak
        init_game(cat_choice)
        st.session_state.wins = wins
        st.session_state.total_games = total
        st.session_state.streak = streak
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#1a4a22;font-size:0.72rem;letter-spacing:2px;'>PYTHON-MINI-GAMES &nbsp;·&nbsp; VASANT &nbsp;·&nbsp; HANGMAN v1.0</p>",
    unsafe_allow_html=True,
)
