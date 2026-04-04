# 🎯 Number Guessing Game

A sleek, dark-themed number guessing game built with **Python + Streamlit**.  
Guess the secret number within a limited number of attempts — difficulty scales the range and pressure.

---

## ▶️ Play Now

> **[🚀 Launch Game →](https://app.streamlit.app)**  
    (Deploying soon...)

---

## 🎮 How to Play

1. Choose a difficulty — Easy, Medium, or Hard
2. Enter your guess in the input field
3. The game tells you if the secret number is **higher** or **lower**
4. Crack the number before your guesses run out!

---

## 🎚️ Difficulty Levels

| Difficulty | Range   | Max Guesses | Optimal Strategy |
|------------|---------|-------------|------------------|
| 🟢 Easy   | 1 – 50  | 10          | Binary search wins in ≤6 |
| 🟡 Medium | 1 – 100 | 7           | Binary search wins in ≤7 |
| 🔴 Hard   | 1 – 200 | 5           | Needs near-perfect binary search |

---

## ✨ Features

- [] Dark warm UI with electric lime accents
- [] Live stats — Win Rate, Best Score, Guesses Left
- [] Progress bar tracking guesses used
- [] Play Again without losing your score streak
- [] Hot/cold proximity hints ("Way too high!", "A bit low")
- [] Duplicate guess detection

---

## 🖥️ Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/python-mini-games.git
cd python-mini-games/games/number-guessing

# Install dependencies
pip install -r requirements.txt

# Launch the game
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🗂️ Project Structure

```
number-guessing/
├── app.py            # Full game logic + UI
├── requirements.txt  # streamlit>=1.32.0
└── README.md         # This file
```

---

## 🧠 What I Learned

- Managing multi-step game state with `st.session_state`
- Persisting cross-game stats (wins, best score) across Streamlit reruns
- Building reactive UIs without JavaScript using Streamlit's rerun model
- Applying custom CSS inside Streamlit for a branded, non-default look

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core logic |
| Streamlit | UI framework + free hosting |
| CSS (injected) | Custom dark theme & styling |

---

## 👤 Author

**Vasant** — Final Year CSE Student  
[GitHub](https://github.com/vasantrj) · [LinkedIn](https://linkedin.com/in/vasantjoshi)

---

*Part of the [python-mini-games](https://github.com/vasantrj/python-mini-games) collection.*
