from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from ai_engine import generate_focus_message, rank_delay_risk_tasks, recommend_next_task, score_tasks
from db import (
    add_task,
    get_daily_study_consistency,
    get_due_reminders,
    get_recent_subject_hours,
    get_setting,
    get_study_streak,
    get_subject_daily_hours,
    get_subject_performance,
    init_db,
    list_study_logs,
    list_tasks,
    log_study_session,
    mark_task_completed,
    set_setting,
)
from scheduler import generate_timetable, generate_weekly_action_plan

st.set_page_config(page_title="AI Study Planner", page_icon="images/favicon.svg", layout="wide")
init_db()

if "weekly_plan_rows" not in st.session_state:
    st.session_state["weekly_plan_rows"] = []
if "weekly_plan_locked" not in st.session_state:
    st.session_state["weekly_plan_locked"] = False

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-main: #0a1220;
        --bg-panel: #101c30;
        --bg-muted: #0f1a2a;
        --text-main: #f6f7fb;
        --text-soft: #a9b8ce;
        --brand: #2ec4b6;
        --brand-strong: #19a898;
        --accent: #ff9f1c;
        --border: rgba(255, 255, 255, 0.1);
        --danger: #ff5a5f;
    }

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% -20%, rgba(46, 196, 182, 0.20) 0%, rgba(46, 196, 182, 0) 42%),
            radial-gradient(circle at 100% 0%, rgba(255, 159, 28, 0.16) 0%, rgba(255, 159, 28, 0) 36%),
            var(--bg-main);
        color: var(--text-main);
    }

    .app-shell {
        border: 1px solid var(--border);
        background: linear-gradient(145deg, rgba(17, 28, 46, 0.88), rgba(10, 18, 32, 0.92));
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(2px);
    }

    .hero-title {
        font-weight: 800;
        font-size: clamp(1.9rem, 3.8vw, 3rem);
        line-height: 1.08;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .hero-highlight {
        color: var(--brand);
    }

    .hero-subtitle {
        color: var(--text-soft);
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-size: 1.01rem;
    }

    .metric-card {
        border: 1px solid var(--border);
        border-radius: 14px;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0));
        padding: 0.9rem 1rem;
        min-height: 112px;
    }

    .metric-label {
        font-size: 0.82rem;
        color: var(--text-soft);
        margin-bottom: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.3rem;
    }

    .metric-note {
        font-size: 0.86rem;
        color: var(--text-soft);
    }

    .panel-title {
        font-size: 1.08rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .panel-text {
        color: var(--text-soft);
        font-size: 0.93rem;
        margin-bottom: 0.6rem;
    }

    .chip {
        display: inline-block;
        border: 1px solid rgba(46, 196, 182, 0.45);
        color: #ccfff8;
        background: rgba(46, 196, 182, 0.14);
        border-radius: 999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.8rem;
        margin-right: 0.45rem;
        margin-bottom: 0.3rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        background: transparent;
        border-bottom: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 10px 10px 0 0;
        padding: 0 1rem;
        color: var(--text-soft);
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(46, 196, 182, 0.14);
        color: #e9fffd;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(46, 196, 182, 0.48);
        background: linear-gradient(135deg, var(--brand), var(--brand-strong));
        color: #04131e;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: rgba(46, 196, 182, 0.85);
        color: #04131e;
    }

    .stDataFrame, .stTable {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    @media (max-width: 760px) {
        .metric-card {
            min-height: 96px;
        }

        .hero-subtitle {
            font-size: 0.94rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_metric_card(label: str, value: str, note: str = "") -> None:
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

default_hours = float(get_setting("daily_hours", "3"))
with st.sidebar:
    st.header("Settings")
    daily_hours = st.number_input("Available study time per day (hours)", min_value=0.5, max_value=16.0, value=default_hours, step=0.5)
    if st.button("Save Available Time"):
        set_setting("daily_hours", str(daily_hours))
        st.success("Saved")

pending_tasks = list_tasks("pending")
completed_tasks = list_tasks("completed")
all_tasks = list_tasks(None)
scored_tasks = score_tasks(pending_tasks, completed_tasks, all_tasks)
reminders = get_due_reminders(days_ahead=2)
streak_days = get_study_streak()
subject_stats = get_subject_performance()
recent_subject_hours = get_recent_subject_hours(days=7)

weak_subject = "None"
if subject_stats:
    weak_row = min(subject_stats, key=lambda row: row["completion_rate"])
    weak_subject = weak_row["subject"]

recommendation, recommendation_message, recommendation_reasons = recommend_next_task(scored_tasks, weak_subject, recent_subject_hours)

today = date.today()
week_end = today + timedelta(days=7)
overdue_tasks = [task for task in pending_tasks if date.fromisoformat(task["deadline"]) < today]
due_today_tasks = [task for task in pending_tasks if date.fromisoformat(task["deadline"]) == today]
due_week_tasks = [
    task
    for task in pending_tasks
    if today < date.fromisoformat(task["deadline"]) <= week_end
]

study_logs = list_study_logs()
consistency_rows = get_daily_study_consistency(days=28)
subject_daily_hours = get_subject_daily_hours(days=14)
risky_tasks = rank_delay_risk_tasks(scored_tasks, limit=8)
coach_message = generate_focus_message(recommendation, weak_subject, recent_subject_hours, risky_tasks)

completion_rate_total = round((len(completed_tasks) / len(all_tasks)) * 100, 1) if all_tasks else 0.0

st.markdown(
    """
    <div class="app-shell">
        <h1 class="hero-title">AI Study Planner</h1>
        <p class="hero-subtitle">ML-based study planning and progress tracking.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)
with metric_col_1:
    render_metric_card("Pending Tasks", str(len(pending_tasks)))
with metric_col_2:
    render_metric_card("Study Streak", str(streak_days))
with metric_col_3:
    render_metric_card("Completion Rate", f"{completion_rate_total}%")
with metric_col_4:
    render_metric_card("Weak Subject", weak_subject)

tab_plan, tab_ops, tab_insights = st.tabs(["Planning", "Execution", "Analytics"])

with tab_plan:
    st.markdown('<div class="panel-title">Add Study Task</div>', unsafe_allow_html=True)

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

        submitted = st.form_submit_button("Create Task")
        if submitted:
            if not subject.strip() or not title.strip():
                st.error("Subject and task name are required.")
            else:
                add_task(subject, title, deadline, difficulty, importance, estimated_hours)
                st.success("Task created")
                st.rerun()

    st.markdown('<div class="panel-title">Timetable</div>', unsafe_allow_html=True)
    plan_days = st.slider("Planning window (days)", min_value=1, max_value=30, value=7)
    schedule = generate_timetable(scored_tasks, daily_hours=daily_hours, days=plan_days)
    if schedule:
        st.dataframe(pd.DataFrame(schedule), use_container_width=True, hide_index=True)
    else:
        st.info("No schedule available yet. Add tasks and saved daily study time.")

with tab_ops:
    rec_col, rem_col = st.columns([1.4, 1])

    with rec_col:
        st.markdown('<div class="panel-title">Recommendation</div>', unsafe_allow_html=True)
        if recommendation:
            st.success(recommendation_message)
            if recommendation_reasons:
                reason_labels = {
                    "high priority": "high priority",
                    "low completion rate in this subject": "weak subject",
                    "low recent study time": "low recent time",
                    "high delay risk": "delay risk",
                }
                readable_tags = [reason_labels.get(reason, reason) for reason in recommendation_reasons]
                st.caption("Why this task: " + " | ".join(readable_tags))
            st.write(
                f"AI score: {recommendation['priority_score']} | "
                f"completion probability: {recommendation['completion_probability']} | "
                f"remaining: {recommendation['remaining_hours']}h"
            )
        else:
            st.info(recommendation_message)

    with rem_col:
        st.markdown('<div class="panel-title">Reminders</div>', unsafe_allow_html=True)
        status_col_1, status_col_2, status_col_3 = st.columns(3)
        with status_col_1:
            st.caption("Overdue")
            if overdue_tasks:
                for item in overdue_tasks[:3]:
                    st.write(f"- {item['subject']} | {item['title']}")
            else:
                st.write("None")
        with status_col_2:
            st.caption("Due Today")
            if due_today_tasks:
                for item in due_today_tasks[:3]:
                    st.write(f"- {item['subject']} | {item['title']}")
            else:
                st.write("None")
        with status_col_3:
            st.caption("Due This Week")
            if due_week_tasks:
                for item in due_week_tasks[:3]:
                    st.write(f"- {item['subject']} | {item['title']}")
            else:
                st.write("None")

        if reminders:
            st.caption("Upcoming reminders")
            for item in reminders[:3]:
                st.write(f"- {item['subject']} | {item['deadline']}")

    action_col_1, action_col_2 = st.columns(2)
    with action_col_1:
        st.markdown('<div class="panel-title">Mark Task Completed</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="panel-title">Log Study Session</div>', unsafe_allow_html=True)
        with st.form("log_form"):
            all_task_options = {"No task linked": None}
            for task in all_tasks:
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
                    linked = next((t for t in all_tasks if t["id"] == chosen_task_id), None)
                    if linked:
                        resolved_subject = linked["subject"]

                if not resolved_subject:
                    st.error("Subject is required.")
                else:
                    log_study_session(chosen_task_id, resolved_subject, session_date, session_hours)
                    st.success("Study session logged")
                    st.rerun()

with tab_insights:
    st.markdown('<div class="panel-title">Progress Analytics Dashboard</div>', unsafe_allow_html=True)

    consistency_df = pd.DataFrame(consistency_rows)
    if not consistency_df.empty:
        total_hours_7d = round(consistency_df.tail(7)["total_hours"].sum(), 1)
        active_days_7d = int(consistency_df.tail(7)["active_day"].sum())
        avg_daily_7d = round(total_hours_7d / 7.0, 2)
    else:
        total_hours_7d = 0.0
        active_days_7d = 0
        avg_daily_7d = 0.0

    kpi_1, kpi_2, kpi_3 = st.columns(3)
    with kpi_1:
        render_metric_card("Hours (Last 7 Days)", f"{total_hours_7d}h")
    with kpi_2:
        render_metric_card("Active Days (Last 7)", str(active_days_7d))
    with kpi_3:
        render_metric_card("Avg Daily Hours", f"{avg_daily_7d}h")

    if not consistency_df.empty:
        st.caption("Weekly consistency trend (last 28 days)")
        st.line_chart(consistency_df.set_index("study_date")[["total_hours"]])
    else:
        st.info("No consistency data yet. Log study sessions to unlock trend insights.")

    st.markdown('<div class="panel-title">AI Coach</div>', unsafe_allow_html=True)
    st.success(coach_message)

    st.markdown('<div class="panel-title">Predicted Delay Risk</div>', unsafe_allow_html=True)
    if risky_tasks:
        risk_df = pd.DataFrame(risky_tasks)[
            [
                "subject",
                "title",
                "deadline",
                "days_left",
                "remaining_hours",
                "completion_probability",
                "delay_risk_score",
            ]
        ]
        risk_df["completion_probability"] = (risk_df["completion_probability"] * 100).round(1)
        risk_df = risk_df.rename(columns={"completion_probability": "completion_prob_%"})
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
    else:
        st.info("No pending tasks available for risk analysis.")

    st.markdown('<div class="panel-title">Weekly Action Plan</div>', unsafe_allow_html=True)
    plan_col_1, plan_col_2 = st.columns(2)
    with plan_col_1:
        weekly_days = st.slider("Weekly planning window (days)", min_value=3, max_value=14, value=7, key="weekly_days")
    with plan_col_2:
        weekly_daily_hours = st.number_input(
            "Daily hours for weekly plan",
            min_value=0.5,
            max_value=16.0,
            value=float(daily_hours),
            step=0.5,
            key="weekly_daily_hours",
        )

    plan_actions_1, plan_actions_2, plan_actions_3 = st.columns(3)
    with plan_actions_1:
        generate_clicked = st.button("Generate Weekly Plan", disabled=st.session_state["weekly_plan_locked"])
    with plan_actions_2:
        lock_clicked = st.button(
            "Lock Plan",
            disabled=st.session_state["weekly_plan_locked"] or not st.session_state["weekly_plan_rows"],
        )
    with plan_actions_3:
        unlock_clicked = st.button("Unlock Plan", disabled=not st.session_state["weekly_plan_locked"])

    if generate_clicked:
        generated_plan = generate_weekly_action_plan(
            scored_tasks=scored_tasks,
            daily_hours=float(weekly_daily_hours),
            weak_subject=weak_subject,
            days=int(weekly_days),
        )
        st.session_state["weekly_plan_rows"] = generated_plan
        st.session_state["weekly_plan_locked"] = False

    if lock_clicked:
        st.session_state["weekly_plan_locked"] = True

    if unlock_clicked:
        st.session_state["weekly_plan_locked"] = False

    weekly_plan_rows = st.session_state.get("weekly_plan_rows", [])
    if st.session_state.get("weekly_plan_locked"):
        st.caption("Plan is locked. Unlock to regenerate.")

    if weekly_plan_rows:
        weekly_plan_df = pd.DataFrame(weekly_plan_rows)
        st.dataframe(weekly_plan_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Weekly Plan CSV",
            data=weekly_plan_df.to_csv(index=False),
            file_name="weekly_action_plan.csv",
            mime="text/csv",
        )
    else:
        st.caption("Click Generate Weekly Plan to create an actionable risk-aware plan.")

    st.markdown('<div class="panel-title">Subject Activity Heatmap (Last 14 Days)</div>', unsafe_allow_html=True)
    if subject_daily_hours:
        heatmap_df = pd.DataFrame(subject_daily_hours)
        pivot = (
            heatmap_df.pivot_table(
                index="subject",
                columns="study_date",
                values="total_hours",
                aggfunc="sum",
                fill_value=0.0,
            )
            .sort_index()
            .round(2)
        )
        st.dataframe(pivot, use_container_width=True)
    else:
        st.info("No subject-hour history yet for heatmap view.")

    st.markdown('<div class="panel-title">Priority Tasks</div>', unsafe_allow_html=True)
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
                "completion_probability",
            ]
        ]
        priority_df["completion_probability"] = (priority_df["completion_probability"] * 100).round(1)
        priority_df = priority_df.rename(columns={"completion_probability": "completion_prob_%"})
        st.dataframe(priority_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Export Priority Tasks CSV",
            data=priority_df.to_csv(index=False),
            file_name="priority_tasks.csv",
            mime="text/csv",
        )
    else:
        st.info("No pending tasks yet.")

    st.markdown('<div class="panel-title">Analytics Charts</div>', unsafe_allow_html=True)

    if recent_subject_hours:
        hours_df = pd.DataFrame(recent_subject_hours).rename(columns={"total_hours": "hours_last_7d"})
        st.caption("Subject-wise study hours (last 7 days)")
        st.bar_chart(hours_df.set_index("subject"))
    else:
        st.info("No subject-hours data yet.")

    completion_trend_rows = []
    for task in completed_tasks:
        completed_at = task.get("completed_at")
        if not completed_at:
            continue
        completed_date = datetime.fromisoformat(completed_at).date()
        week_start = completed_date - timedelta(days=completed_date.weekday())
        completion_trend_rows.append({"week": week_start.isoformat(), "completed": 1})

    if completion_trend_rows:
        completion_trend_df = pd.DataFrame(completion_trend_rows)
        completion_trend_df = completion_trend_df.groupby("week", as_index=False)["completed"].sum().sort_values("week")
        st.caption("Weekly completion trend")
        st.line_chart(completion_trend_df.set_index("week"))
    else:
        st.info("No completion trend data yet.")

    if scored_tasks:
        priority_bins = pd.cut(
            pd.Series([task["priority_score"] for task in scored_tasks]),
            bins=[-1, 10, 20, 30, 100],
            labels=["0-10", "11-20", "21-30", "31+"],
        )
        dist_df = priority_bins.value_counts().sort_index().rename_axis("priority_band").reset_index(name="tasks")
        st.caption("Priority distribution")
        st.bar_chart(dist_df.set_index("priority_band"))
    else:
        st.info("No priority distribution data yet.")

    st.markdown('<div class="panel-title">Weak Subject Analysis</div>', unsafe_allow_html=True)
    if subject_stats:
        perf_df = pd.DataFrame(subject_stats)
        perf_df["completion_rate"] = (perf_df["completion_rate"] * 100).round(1)
        perf_df = perf_df.rename(columns={"completion_rate": "completion_rate_percent"})
        st.dataframe(perf_df, use_container_width=True, hide_index=True)
    else:
        st.info("Weak subject analysis will appear after adding tasks.")

    st.markdown('<div class="panel-title">Study Sessions</div>', unsafe_allow_html=True)
    if study_logs:
        logs_df = pd.DataFrame(study_logs)
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Export Study Sessions CSV",
            data=logs_df.to_csv(index=False),
            file_name="study_sessions.csv",
            mime="text/csv",
        )
    else:
        st.info("No study session logs yet.")
