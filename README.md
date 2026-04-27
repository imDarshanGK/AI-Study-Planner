AI Study Planner
=================

AI Study Planner is a compact, professional study-planning prototype intended for technical portfolios and interviews. It demonstrates an end-to-end Python workflow: a Streamlit frontend, SQLite persistence, and a lightweight scikit-learn pipeline for data-driven recommendations.

Features
--------

- Capture tasks with subject, title, deadline, difficulty, importance, and estimated hours.
- Priority scoring that combines a heuristic urgency metric with a learned adjustment from historical data.
- Completion-risk estimation to surface at-risk tasks.
- Auto timetable generation that allocates daily study time across upcoming days.
- Study session logging, streaks, and subject performance analytics.
- CSV export for tasks and session logs.

Technical Summary
-----------------

- Python 3.10+
- Streamlit UI (`app.py`)
- SQLite persistence (`db.py`)
- ML: scikit-learn (LinearRegression, RandomForestClassifier) (`ai_engine.py`)
- Timetable generator (`scheduler.py`)
- Data tooling: pandas

Repository Layout
-----------------

- `app.py` — Streamlit application and UI flows (planning, execution, analytics)
- `db.py` — SQLite schema and data access helpers
- `ai_engine.py` — priority scoring, model training, and recommendation logic
- `scheduler.py` — timetable generation utilities
- `requirements.txt` — Python dependencies
- `render.yaml` — optional Render deploy configuration

Quickstart (local)
------------------

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies and run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

3. Open http://localhost:8501 in your browser.

Deployment Notes
----------------

The repository includes an optional `render.yaml`. For most hosts ensure the start command uses:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

Development Ideas
-----------------

- Add per-user authentication and persistent model artifacts for production use.
- Replace SQLite with a managed database for multi-user deployments.
- Separate API (FastAPI) from the Streamlit frontend for a production-grade architecture.

Contributing
------------

Contributions welcome. Open an issue for bugs or feature requests and submit focused pull requests.

License
-------

MIT — see the `LICENSE` file for details.
AI Study Planner
=================

AI Study Planner is a concise, practical study-planning application intended as a portfolio-ready project. It demonstrates a complete Python-based workflow: a Streamlit user interface, SQLite persistence, and lightweight machine learning with scikit-learn to produce data-driven recommendations.

This repository contains a working MVP focused on clear, verifiable functionality — task capture, priority scoring, timetable generation, study logging, and evidence-based recommendations.

Key Features
------------

- Task capture: subject, title, deadline, difficulty, importance, and estimated hours.
- AI-driven priority scoring: heuristic urgency combined with a learned adjustment from historical data.
- Completion probability: a classifier estimates task completion risk to surface at-risk items.
- Auto timetable: allocates available daily study hours across upcoming days.
- Progress tracking: study session logs, streaks, and subject performance analytics.
- CSV export: download tasks and session logs for offline analysis.

Why this project
----------------

This project is deliberately scoped to be practical and demonstrable in interviews: it shows end-to-end design, basic production considerations (dependency pinning and a deploy config), and a small applied ML pipeline that uses real usage data rather than fabricated claims.

Technical Overview
------------------

- Language: Python 3.10+
- UI: Streamlit
- ML: scikit-learn (LinearRegression for score adjustment; RandomForestClassifier for completion probability)
- Storage: SQLite
- Data tooling: pandas for CSV export and simple analytics

Repository Layout
-----------------

- `app.py` — Streamlit application and UI flows (planning, execution, analytics).
- `db.py` — SQLite schema, migrations, and data access helpers.
- `ai_engine.py` — priority scoring, model training, and recommendation logic.
- `scheduler.py` — timetable generation utilities.
- `requirements.txt` — Python dependencies.
- `render.yaml` — optional Render deployment configuration.

Quickstart (local)
------------------

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies and run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

3. Open http://localhost:8501 in your browser.

Deployment notes
----------------

The repository includes a `render.yaml` and a Streamlit start command that uses the `$PORT` environment variable. For basic deploy steps:

1. Push the repository to a Git provider (e.g. GitHub).
2. Create a new Web Service on a host such as Render, Railway, or another cloud provider.
3. Ensure the start command uses: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`.

If you prefer Docker, containerize the app and expose the port expected by your hosting provider.

Development & Extension Ideas
-----------------------------

- Add user authentication and per-user data isolation.
- Replace SQLite with a managed database for multi-user deployments.
- Add a lightweight API (FastAPI) to separate backend logic from the Streamlit frontend.
- Improve model training workflows (online updates, persistent model artifacts).

Contributing
------------

Contributions are welcome. Please open issues for bug reports or feature requests and submit focused pull requests for changes.

License
-------

MIT — see the `LICENSE` file for details.
# AI Study Planner

AI Study Planner — a compact, practical study planning app that demonstrates a full-stack workflow:

- Python backend logic
- Streamlit user interface
- SQLite persistence
- Real machine learning with scikit-learn

Live demo: https://studora-app.onrender.com

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

*Screenshots: available on the live demo linked above.*
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
