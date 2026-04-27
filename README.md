# AI Study Planner

AI Study Planner — a compact, practical study planning app that demonstrates a full-stack workflow:

- Python backend logic
- Streamlit user interface
- SQLite persistence
- Real machine learning with scikit-learn

This repository contains a working MVP you can run locally or deploy to a simple cloud host. It focuses on real features (no fake claims): task input, priority scoring, timetable generation, study logging, and behavior-aware recommendations.
## Overview

Key capabilities:

- Task capture: subject, title, deadline, difficulty, importance, estimated hours
- AI-driven priority scoring: deadline pressure, difficulty, importance, workload
- ML adjustments: a LinearRegression model refines scores from historical outcomes
- Completion probability: RandomForestClassifier predicts completion risk
- Auto timetable: allocate available daily hours across upcoming days
- Progress tracking: study session logs, study streak, weak-subject analysis
- Recommendations: concise, data-backed suggestion with reasons (e.g. "low recent time", "weak subject")
## Core Features

- Task input and persistence (`tasks` table in SQLite)
- Study session logging (`study_logs` table)
- AI priority scoring and completion prediction (`ai_engine.py`)
- Automatic timetable generator (`scheduler.py`)
- Analytics and CSV export for tasks and sessions
- Simple Streamlit UI with a professional dashboard
## How it works (brief)

1. Heuristic score is computed per task using deadline pressure, difficulty, importance, and estimated hours.
2. When enough completed-task history exists the app trains a LinearRegression model to adjust priority scores.
3. A RandomForestClassifier estimates completion probability using difficulty, importance, days left, estimated hours, and logged progress ratio.
4. The final rank = heuristic + learned adjustment + a risk boost for low completion probability. Recommendations show concise reason tags.
## Tech stack

- Python 3.10+
- Streamlit (UI)
- scikit-learn (ML)
- SQLite (persistence)
- pandas (tables & CSV export)
## Project structure

- `app.py` — Streamlit UI and user flows
- `db.py` — SQLite schema and data access helpers
- `ai_engine.py` — priority scoring, ML training, recommendation logic
- `scheduler.py` — timetable generation
- `requirements.txt` — Python dependencies
- `render.yaml` — (optional) Render deploy config
## Quick start (local)

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies and run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.
## Deployment

Recommended quick option: Render (auto-deploy from GitHub). The repo already includes `render.yaml` and a Streamlit server command that uses `$PORT`.

Other options: Railway, Heroku (requires Procfile), Docker on any host.

## Screenshots

Add screenshots to the repo under `images/` and reference them in this README. Example:

```md
![Dashboard screenshot](images/dashboard.png)
```

## What to include in your portfolio write-up

- Short problem statement (what the app solves)
- Key technical choices (Streamlit, scikit-learn, SQLite)
- A sentence about how the ML models are used (scoring + completion probability)
- One-sentence deployment note (Render or Railway link)

## Contributing

Contributions welcome — open an issue or PR. Keep changes small and focused.

## License

MIT — see the `LICENSE` file.
# AI Study Planner

AI Study Planner is a real, working project that combines:
- Python backend logic
- Streamlit user interface
- SQLite persistence
- Real machine learning with scikit-learn

It helps students plan subjects, deadlines, and available time while generating a daily study strategy.

## What It Does

### User Inputs
- Subjects
- Task deadlines
- Difficulty and importance
- Available study time per day

### AI Generates
- Daily timetable
- Priority-scored tasks
- Due-soon reminders
- Completion probability estimates for pending tasks

### Tracks
- Study streak
- Weak subjects (low completion rate)

### Recommends
- Next best task automatically
- Behavior-aware recommendation text (priority + weak-subject + low recent focus)

## Core Features Included
- Task input system
- AI priority scoring
- Auto timetable generator
- Progress tracking
- Smart recommendation engine

## AI Logic

Current base priority starts simple:

Priority = deadline pressure + difficulty + importance + workload factor

Then the app upgrades with real ML models:
- Linear Regression: learns score adjustment from completed task outcomes
- Random Forest Classifier: predicts completion probability using
	- difficulty
	- importance
	- days left
	- estimated hours
	- current logged progress ratio

The final ranking combines heuristic urgency + learned score adjustment + risk boost from low completion probability.

This is the actual AI part of the project: task ranking, completion prediction, and recommendation reasoning are data-driven, not static UI text.

## Tech Stack
- Python
- Streamlit
- scikit-learn
- SQLite

## Project Structure
- `app.py` - Streamlit UI and feature flow
- `db.py` - SQLite schema and data access
- `ai_engine.py` - priority scoring + recommendation logic
- `scheduler.py` - timetable generation
- `requirements.txt` - dependencies

## Setup

1. Create a virtual environment
2. Install dependencies
3. Run the app

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- This is intentionally a practical basic-to-intermediate build suitable for real-world applications.
- It does not claim advanced reinforcement learning; that can be added later as an upgrade.
- SQLite now stores tasks, study sessions, and progress events.

## Next Upgrade Ideas
- User login/authentication
- Dashboard charts
- FastAPI backend split
- Deployment on Render or Railway

## Deployment

This repo now includes a Render deployment config in [render.yaml](render.yaml).

Render start command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

Deployment steps:
1. Push this repo to GitHub.
2. Create a new Web Service on Render.
3. Connect the GitHub repo.
4. Use the provided build and start commands.
5. Deploy and open the live URL.

Supported deployment options (quick):

- Render (recommended): automatic GitHub deploys, free tier available, supports Streamlit with `$PORT` environment variable.
- Railway: quick deploys from GitHub and simple environment config.
- Vercel: mainly for frontend, but can run Streamlit via a Docker service.
- Heroku: still possible using a simple Procfile, but requires manual setup and may have dyno sleep on free tier.

Adding screenshots to README:

1. Create an `images/` folder at the repo root and add your screenshot files (e.g. `images/dashboard.png`).
2. Reference them in `README.md` using standard Markdown:

```md
![Dashboard screenshot](images/dashboard.png)
```

I added a placeholder reference in the docs; commit the actual image files and push to include them in the project.
