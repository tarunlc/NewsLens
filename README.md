# 🔍 NewsLens — Media Divergence Tracker

> Compare how 10 major news outlets report the **same story** — detect conflicting facts automatically using NLP.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-orange)
![NewsAPI](https://img.shields.io/badge/Data-NewsAPI-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🧠 What Is This?

NewsLens is an AI/ML project that fetches live headlines from 10 global news outlets, groups articles about the same event using **TF-IDF + Cosine Similarity**, then flags where their reported facts **diverge**.

**Example — same story, different facts:**
| Outlet | Claim |
|---|---|
| BBC News | 50% of facility destroyed |
| Fox News | 100% destroyed |
| Reuters | Partial damage reported |

NewsLens catches this automatically and highlights it as a ⚡ Fact Conflict.

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python + Flask |
| NLP / ML | scikit-learn — TF-IDF Vectorizer + Cosine Similarity |
| Conflict Detection | Regex claim extraction (%, numbers, $, time) |
| Data Source | NewsAPI — 10 live outlets |
| Frontend | Vanilla HTML/CSS/JS — dark editorial UI |
| Deployment | Google Colab + Cloudflare Tunnel |

---

## 📰 Sources Tracked

| Outlet | Bias |
|---|---|
| BBC News | Center |
| Reuters | Center |
| AP News | Center |
| Sky News | Center |
| CNN | Center-Left |
| Al Jazeera | Center-Left |
| NBC News | Center-Left |
| The Guardian | Center-Left |
| Washington Post | Center-Left |
| Fox News | Right |

---

## 🚀 Run Locally
```bash
git clone https://github.com/tarunlc/NewsLens.git
cd NewsLens
pip install -r requirements.txt
python app.py
# Open http://localhost:5050
```

---

## ⚙️ How It Works

1. **Fetch** — Live top headlines pulled from all 10 sources via NewsAPI
2. **Vectorize** — Article title + description converted to TF-IDF vectors
3. **Group** — Cosine similarity clusters articles covering the same event
4. **Extract** — Regex pulls numerical claims: percentages, casualties, money, time
5. **Compare** — Flags where different outlets report different numbers on same story
6. **Display** — Filterable dark-theme dashboard with divergence scores

---

## 📁 Project Structure
```
NewsLens/
├── app.py               # Flask server + API routes
├── news_service.py      # Fetch, TF-IDF grouping, conflict detection
├── templates/
│   └── index.html       # Dark editorial UI
├── requirements.txt
└── README.md
```

---

## 👤 Author

**Tarun** — B.Tech AI & ML, Dayananda Sagar University, Bengaluru
MSc Business Analytics, Aston University (2026)
Background: AI Safety · Red Teaming · Data Analytics

---

## 📄 License
MIT — free to use, modify, and build on.
