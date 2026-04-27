AI Study Planner
=================

AI Study Planner is a zero-fuss study planning app built with Python, Streamlit, SQLite, and scikit-learn. It turns tasks, deadlines, and available study time into a practical daily plan with simple machine-learning-based scoring.

Task planning, priority scoring, timetable generation, study logging, and recommendation support are all included in one small project.

Features
--------

- Add tasks with subject, title, deadline, difficulty, importance, and estimated hours.
- Rank tasks by urgency and learned priority adjustment from historical data.
- Estimate completion risk for pending tasks.
- Generate a daily timetable from available study hours.
- Log study sessions and review progress over time.
- Export tasks and study logs as CSV.

How it works
------------

1. The app computes a heuristic priority score from deadline pressure, difficulty, importance, and estimated workload.
2. When enough history exists, scikit-learn models refine the score and estimate completion probability.
3. The scheduler spreads study time across upcoming days based on the final priority order.
4. Study logs and task updates feed the next recommendation cycle.

Tech Stack
----------

- Python 3.10+
- Streamlit for the UI
- SQLite for persistence
- scikit-learn for scoring and prediction
- pandas for table handling and CSV export

Project Structure
-----------------

- `app.py` - Streamlit application and UI flow
- `db.py` - database schema and data access helpers
- `ai_engine.py` - scoring, model training, and recommendation logic
- `scheduler.py` - timetable generation utilities
- `requirements.txt` - Python dependencies
- `render.yaml` - optional deployment config

Quick Start
-----------

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies and run the app.

```bash
pip install -r requirements.txt
streamlit run app.py
```

3. Open `http://localhost:8501` in your browser.

Deployment
----------

The repository includes an optional `render.yaml` and a Render-friendly start command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

Contributing
------------

Contributions are welcome. Keep changes focused and open an issue for larger ideas.

License
-------

MIT - see the `LICENSE` file for details.
