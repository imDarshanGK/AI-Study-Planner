# AI Study Planner

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-storage-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

AI Study Planner is a practical study-planning app that turns tasks, deadlines, available hours, and progress history into a clear daily and weekly action plan.

It combines a clean Streamlit UI, SQLite persistence, and machine-learning-based task scoring to help students decide what to study next and how to stay consistent.

## At a Glance

- Task planning with subject, deadline, difficulty, importance, and estimated hours.
- AI-assisted priority scoring and completion-risk prediction.
- Auto-generated daily timetable and weekly action plan.
- Study session logging, streak tracking, and subject performance analysis.
- Analytics dashboard with consistency trends, risk insights, and focus recommendations.

## What It Does

### Planning

- Add study tasks with deadlines and effort estimates.
- Rank tasks by urgency, workload, and learned priority adjustment.
- Generate a timetable based on your available study hours.

### Execution

- Mark tasks as completed.
- Log study sessions by subject or linked task.
- Track progress events and streaks over time.

### Analytics

- View weekly consistency and study-hour KPIs.
- Spot weak subjects and low-focus areas.
- Review predicted delay-risk tasks.
- Generate one-click weekly plans with lock/unlock mode.

## AI Logic

The app uses a layered approach:

1. A heuristic score estimates urgency from deadline pressure, difficulty, importance, and workload.
2. When enough history exists, scikit-learn models refine the score and estimate completion probability.
3. The recommendation engine combines task priority with weak-subject and recent-focus signals.
4. The weekly planner converts those insights into a balanced, actionable schedule.

## Tech Stack

- Python
- Streamlit
- SQLite
- scikit-learn
- pandas

## Project Structure

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit UI and feature flow |
| `db.py` | SQLite schema and data access helpers |
| `ai_engine.py` | Priority scoring, risk prediction, and recommendation logic |
| `scheduler.py` | Daily timetable and weekly plan generation |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |

## Quick Start

1. Create a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the app.

```bash
streamlit run app.py
```

4. Open `http://localhost:8501` in your browser.

## Deployment

This repo includes a Render-friendly start command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

If you deploy on Render, connect the repo as a web service and use the command above.

## Current Feature Set

- Task input system
- AI priority scoring
- Completion probability estimation
- Daily timetable generator
- Study streak tracking
- Weak-subject analysis
- Progress analytics dashboard
- Subject activity heatmap
- Delay-risk ranking
- AI coach recommendation text
- Weekly action plan generator
- Lock/unlock mode for weekly plans

## Notes

- This project is intentionally practical and internship-ready.
- It does not claim advanced reinforcement learning.
- SQLite stores tasks, study sessions, and progress events locally.

## Contributing

Contributions are welcome. Keep changes focused and open an issue for larger ideas.

## License

MIT License. See the [LICENSE](LICENSE) file for the full terms.
