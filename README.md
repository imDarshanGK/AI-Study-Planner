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
