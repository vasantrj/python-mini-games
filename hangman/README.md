# 💀 Hangman

A retro **phosphor terminal-styled** Hangman game built with **Python + Streamlit**.  
Guess the hidden word letter by letter before the prisoner is executed — 6 wrong guesses and it's over.

---

## ▶️ Play Now

> **[🚀 Launch Game →](https://app.streamlit.app)**  
    (Deploying Soon...)

---

## 🎮 How to Play

1. A secret word is chosen from the selected category
2. Click letters on the on-screen keyboard to guess
3. Each wrong guess adds a body part to the hangman
4. Reveal the full word before 6 mistakes — or the prisoner is gone

---

## 📚 Word Categories

| Category | Description |
|----------|-------------|
| 🐍 Python | Python programming concepts & terms |
| 🧠 Data Science | ML, statistics & data terminology |
| 💻 CS Concepts | Core computer science vocabulary |
| 🌐 General | Common tech/programming words |

> Categories double as a learning tool — great for interview vocab revision!

---

## ✨ Features

- Classic ASCII hangman — 7 progressive stages
- Full on-screen QWERTY keyboard (click to guess)
- 4 word categories including Python & Data Science
- Win streak tracker across rounds
- Session stats — Games, Wins, Streak, Lives Left
- Lives counter turns red when ≤ 2 remain
- Switch category mid-session or after game
- Phosphor green terminal aesthetic with scanline effect & glow

---

## 🖥️ Run Locally

```bash
# Clone the repo
git clone https://github.com/vasantrj/python-mini-games.git
cd python-mini-games/games/hangman

# Install dependencies
pip install -r requirements.txt

# Launch the game
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🗂️ Project Structure

```
hangman/
├── app.py            # Full game logic + UI
├── requirements.txt  # streamlit>=1.32.0
└── README.md         # This file
```

---

## 🧠 What I Learned

- Using `st.session_state` to model turn-based game state cleanly
- Dynamically disabling buttons after use with Streamlit reruns
- Injecting custom CSS (fonts, glow effects, scanlines) into Streamlit for a fully branded look
- Organizing domain-specific word banks as Python dicts for easy extension
- Building streak/stat persistence across multiple game rounds in a single session

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Game logic & word banks |
| Streamlit | UI framework + free cloud hosting |
| CSS (injected) | Phosphor terminal theme, Orbitron + Share Tech Mono fonts |

---

## 💡 Extend It Yourself

- Add a **hints system** (reveal a letter for a score penalty)
- Load words from an external **words.txt** file
- Add a **multiplayer mode** where Player 1 types a word and Player 2 guesses
- Integrate with an **API** to fetch random words by difficulty

---

## 👤 Author

**Vasant Joshi** — Final Year CSE Student  
[GitHub](https://github.com/vasantrj) · [LinkedIn](https://linkedin.com/in/vasantjoshi) 

---

*Part of the [python-mini-games](https://github.com/vasantrj/python-mini-games) collection.*
