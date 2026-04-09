from datetime import date

import pandas as pd
import streamlit as st

from ai_engine import recommend_next_task, score_tasks
from db import (
    add_task,
    get_due_reminders,
    get_setting,
    get_study_streak,
    get_subject_performance,
    init_db,
    list_tasks,
    log_study_session,
    mark_task_completed,
    set_setting,
)
from scheduler import generate_timetable

st.set_page_config(page_title="AI Study Planner", page_icon="📘", layout="wide")
init_db()

st.title("AI Study Planner")
st.caption("Plan study sessions with deadline-aware priority scoring and automatic next-task recommendations.")

default_hours = float(get_setting("daily_hours", "3"))
with st.sidebar:
    st.header("Settings")
    daily_hours = st.number_input("Available study time per day (hours)", min_value=0.5, max_value=16.0, value=default_hours, step=0.5)
    if st.button("Save Available Time"):
        set_setting("daily_hours", str(daily_hours))
        st.success("Saved")

st.subheader("1) Add Study Task")
with st.form("add_task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        subject = st.text_input("Subject", placeholder="Data Structures")
    with col2:
        title = st.text_input("Task", placeholder="Revise linked lists")
    with col3:
        deadline = st.date_input("Deadline", min_value=date.today())

    col4, col5, col6 = st.columns(3)
    with col4:
        difficulty = st.slider("Difficulty", min_value=1, max_value=10, value=5)
    with col5:
        importance = st.slider("Importance", min_value=1, max_value=10, value=5)
    with col6:
        estimated_hours = st.number_input("Estimated hours", min_value=0.5, max_value=200.0, value=2.0, step=0.5)

    submitted = st.form_submit_button("Add Task")
    if submitted:
        if not subject.strip() or not title.strip():
            st.error("Subject and task name are required.")
        else:
            add_task(subject, title, deadline, difficulty, importance, estimated_hours)
            st.success("Task added")
            st.rerun()

pending_tasks = list_tasks("pending")
completed_tasks = list_tasks("completed")
scored_tasks = score_tasks(pending_tasks, completed_tasks)
recommendation = recommend_next_task(scored_tasks)
reminders = get_due_reminders(days_ahead=2)
streak_days = get_study_streak()
subject_stats = get_subject_performance()

weak_subject = "None"
if subject_stats:
    weak_row = min(subject_stats, key=lambda row: row["completion_rate"])
    weak_subject = weak_row["subject"]

st.subheader("2) Dashboard")
metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Pending Tasks", len(pending_tasks))
metric_2.metric("Study Streak (days)", streak_days)
metric_3.metric("Due Soon Reminders", len(reminders))
metric_4.metric("Weak Subject", weak_subject)

if reminders:
    st.warning("Tasks due soon")
    for item in reminders:
        st.write(f"- {item['subject']} | {item['title']} | deadline: {item['deadline']}")

st.subheader("3) AI Priority Tasks")
if scored_tasks:
    priority_df = pd.DataFrame(scored_tasks)[
        [
            "id",
            "subject",
            "title",
            "deadline",
            "difficulty",
            "importance",
            "estimated_hours",
            "logged_hours",
            "remaining_hours",
            "priority_score",
        ]
    ]
    st.dataframe(priority_df, use_container_width=True)
else:
    st.info("No pending tasks yet.")

st.subheader("4) Auto Timetable")
days_to_plan = st.slider("Plan days", min_value=1, max_value=30, value=7)
schedule = generate_timetable(scored_tasks, daily_hours=daily_hours, days=days_to_plan)
if schedule:
    st.dataframe(pd.DataFrame(schedule), use_container_width=True)
else:
    st.info("No schedule generated yet. Add tasks and available time.")

st.subheader("5) Smart Recommendation")
if recommendation:
    st.success(
        f"Next task: {recommendation['subject']} - {recommendation['title']}"
        f" | score {recommendation['priority_score']} | remaining {recommendation['remaining_hours']}h"
    )
else:
    st.info("No recommendation available.")

st.subheader("6) Progress Tracking")
action_col_1, action_col_2 = st.columns(2)

with action_col_1:
    st.markdown("Mark Task Completed")
    if pending_tasks:
        options = {f"#{task['id']} {task['subject']} - {task['title']}": task["id"] for task in pending_tasks}
        selected_label = st.selectbox("Pending task", list(options.keys()), key="mark_done_select")
        if st.button("Complete Task"):
            mark_task_completed(options[selected_label])
            st.success("Task marked as completed")
            st.rerun()
    else:
        st.write("No pending tasks")

with action_col_2:
    st.markdown("Log Study Session")
    with st.form("log_form"):
        all_task_options = {"No task linked": None}
        for task in list_tasks(None):
            label = f"#{task['id']} {task['subject']} - {task['title']}"
            all_task_options[label] = task["id"]

        picked = st.selectbox("Task", list(all_task_options.keys()))
        session_subject = st.text_input("Subject for session")
        session_date = st.date_input("Study date", value=date.today())
        session_hours = st.number_input("Hours studied", min_value=0.25, max_value=16.0, value=1.0, step=0.25)
        if st.form_submit_button("Log Session"):
            chosen_task_id = all_task_options[picked]
            resolved_subject = session_subject.strip()
            if not resolved_subject and chosen_task_id is not None:
                linked = next((t for t in list_tasks(None) if t["id"] == chosen_task_id), None)
                if linked:
                    resolved_subject = linked["subject"]

            if not resolved_subject:
                st.error("Subject is required.")
            else:
                log_study_session(chosen_task_id, resolved_subject, session_date, session_hours)
                st.success("Study session logged")
                st.rerun()

st.subheader("7) Weak Subject Analysis")
if subject_stats:
    perf_df = pd.DataFrame(subject_stats)
    perf_df["completion_rate"] = (perf_df["completion_rate"] * 100).round(1)
    perf_df = perf_df.rename(columns={"completion_rate": "completion_rate_percent"})
    st.dataframe(perf_df, use_container_width=True)
else:
    st.info("Weak subject analysis will appear after adding tasks.")
