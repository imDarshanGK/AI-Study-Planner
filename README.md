# AI Study Planner

AI Study Planner is a real, working internship-ready project that combines:
- Python backend logic
- Streamlit user interface
- SQLite persistence
- Basic machine learning with scikit-learn

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
- This is intentionally a practical basic-to-intermediate build suitable for internship applications.
- It does not claim advanced reinforcement learning; that can be added later as an upgrade.
- SQLite now stores tasks, study sessions, and progress events.

## Next Upgrade Ideas
- User login/authentication
- Dashboard charts
- FastAPI backend split
- Deployment on Render or Railway
