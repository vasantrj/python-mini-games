# 📺 Quiz Show

A 10-question trivia game styled like a **retro CRT game show terminal** — Bebas Neue headings,
scanline overlay, amber glow, monospace body text. Feels nothing like a default Streamlit app.

---

## ▶️ Play Now

> **[🚀 Launch Game →](https://app.streamlit.app)**  
    (Deploying Soon..)

---

## 🎮 How to Play

1. Each round pulls **10 random questions** from the bank (22 total, shuffled)
2. You have **15 seconds** per question — the timer bar drains in real time
3. Pick the correct answer from **A / B / C / D**
4. Instant feedback after each answer — green for right, red for wrong
5. Final screen shows your score, accuracy %, and all-time best

---

## 📚 Categories

| Category | Sample Questions |
|----------|-----------------|
| 🔬 Science | Powerhouse of the cell, speed of light, chemical symbols |
| 🏛️ History | WW2 end year, Moon landing, Berlin Wall |
| 🌍 Geography | Longest river, capital of Australia, mountain ranges |
| 💻 Tech | HTTP meaning, Apple co-founder, backbone of the web |
| 🎬 Pop Culture | Oscars count, Bohemian Rhapsody, Wakanda |

---

## ✨ Features

- 📺 **CRT scanline overlay** via CSS `repeating-linear-gradient` — no images needed
- ⏱️ **Live 15-second countdown** bar with color shift (green → amber → red)
- 🟢🔴 **10-dot progress trail** — every answer leaves a green or red dot
- 🎨 **Bebas Neue** headers + **Share Tech Mono** body — zero generic fonts
- 🏆 Persistent best score and games played across rounds
- 🔀 Questions and answer order shuffled every game
- 🔇 Auto-advance on timeout with "TIME'S UP" message

---

## 🖥️ Run Locally

```bash
git clone https://github.com/vasantrj/python-mini-games.git
cd python-mini-games/games/quiz-game

pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🗂️ Project Structure

```
quiz-game/
├── app.py            # All game logic + UI + CSS
├── requirements.txt  # streamlit>=1.32.0
└── README.md
```

---

## 🧠 What I Learned

- Real-time UI updates in Streamlit using `time.sleep(1)` + `st.rerun()` for live timers
- Injecting complex, scoped CSS overrides into Streamlit without a custom component
- Managing multi-phase game state (playing → feedback → results) cleanly in `st.session_state`
- Styling a recognizable aesthetic (CRT / retro terminal) using only CSS — no assets

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Game logic, question bank, state |
| Streamlit | UI framework + free hosting |
| CSS (injected) | CRT scanlines, amber glow, Bebas Neue theme |
| Google Fonts | Bebas Neue (display) + Share Tech Mono (body) |

---

## 👤 Author

**Vasant Joshi** — Final Year CSE Student  
[GitHub](https://github.com/vasantrj) · [LinkedIn](https://linkedin.com/in/vasantjoshi) · 

---

*Part of the [python-mini-games](https://github.com/vasantrj/python-mini-games) collection.*
