AI Study Planner
=================

AI Study Planner is a practical study-planning app built with Python, Streamlit, SQLite, and scikit-learn. It is intended as a portfolio-ready project that demonstrates task planning, priority scoring, timetable generation, study tracking, and simple machine learning for recommendations.

Features
--------

- Add tasks with subject, title, deadline, difficulty, importance, and estimated hours.
- Score task priority using urgency, workload, and learned adjustments from past data.
- Estimate completion risk for pending tasks.
- Generate a daily study timetable from available hours.
- Log study sessions and review progress over time.
- Export tasks and study logs as CSV.

Technical Summary
-----------------

- Python 3.10+
- Streamlit UI in `app.py`
- SQLite persistence in `db.py`
- scikit-learn models in `ai_engine.py`
- Timetable generation in `scheduler.py`
- pandas for table handling and CSV export

Repository Layout
-----------------

- `app.py` - Streamlit application and UI flow
- `db.py` - database schema and data access helpers
- `ai_engine.py` - scoring, model training, and recommendation logic
- `scheduler.py` - timetable generation utilities
- `requirements.txt` - Python dependencies
- `render.yaml` - optional deployment config

Quickstart
----------

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

Deployment Notes
----------------

The app includes a Render-friendly start command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

Contributing
------------

Contributions are welcome. Please keep changes focused and open an issue for larger ideas.

License
-------

MIT - see the `LICENSE` file for details.
