import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "study_planner.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                deadline TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                importance INTEGER NOT NULL,
                estimated_hours REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS study_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                subject TEXT NOT NULL,
                study_date TEXT NOT NULL,
                hours REAL NOT NULL,
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                task_id INTEGER,
                subject TEXT,
                value REAL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
            """
        )


def _log_progress_event(
    event_type: str,
    task_id: int | None = None,
    subject: str | None = None,
    value: float | None = None,
    notes: str | None = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO progress_events(event_type, task_id, subject, value, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (event_type, task_id, subject, value, notes, datetime.utcnow().isoformat()),
        )


def add_task(
    subject: str,
    title: str,
    deadline: date,
    difficulty: int,
    importance: int,
    estimated_hours: float,
) -> None:
    normalized_subject = subject.strip()
    normalized_title = title.strip()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO tasks(subject, title, deadline, difficulty, importance, estimated_hours, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                normalized_subject,
                normalized_title,
                deadline.isoformat(),
                difficulty,
                importance,
                estimated_hours,
                datetime.utcnow().isoformat(),
            ),
        )
    _log_progress_event(
        event_type="task_added",
        subject=normalized_subject,
        value=estimated_hours,
        notes=f"{normalized_title} (deadline {deadline.isoformat()})",
    )


def list_tasks(status: str | None = None) -> list[dict]:
    query = (
        """
        SELECT
            t.*,
            COALESCE(SUM(sl.hours), 0) AS logged_hours
        FROM tasks t
        LEFT JOIN study_logs sl ON sl.task_id = t.id
        """
    )
    params: list[str] = []
    if status:
        query += " WHERE t.status = ?"
        params.append(status)
    query += " GROUP BY t.id ORDER BY date(t.deadline) ASC"

    with get_conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def mark_task_completed(task_id: int) -> None:
    subject: str | None = None
    with get_conn() as conn:
        row = conn.execute("SELECT subject, title FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.execute(
            """
            UPDATE tasks
            SET status = 'completed', completed_at = ?
            WHERE id = ?
            """,
            (datetime.utcnow().isoformat(), task_id),
        )
        if row:
            subject = row["subject"]
            title = row["title"]
        else:
            title = ""
    _log_progress_event(
        event_type="task_completed",
        task_id=task_id,
        subject=subject,
        notes=title,
    )


def log_study_session(task_id: int | None, subject: str, study_date: date, hours: float) -> None:
    normalized_subject = subject.strip()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO study_logs(task_id, subject, study_date, hours)
            VALUES (?, ?, ?, ?)
            """,
            (task_id, normalized_subject, study_date.isoformat(), hours),
        )
    _log_progress_event(
        event_type="study_session_logged",
        task_id=task_id,
        subject=normalized_subject,
        value=hours,
        notes=study_date.isoformat(),
    )


def get_setting(key: str, default: str) -> str:
    with get_conn() as conn:
        row = conn.execute("SELECT value FROM app_settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO app_settings(key, value)
            VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )


def get_due_reminders(days_ahead: int = 2) -> list[dict]:
    today = date.today().isoformat()
    max_day = (date.today() + timedelta(days=days_ahead)).isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE status = 'pending'
              AND date(deadline) BETWEEN date(?) AND date(?)
            ORDER BY date(deadline) ASC
            """,
            (today, max_day),
        ).fetchall()
    return [dict(row) for row in rows]


def get_study_streak() -> int:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT DISTINCT study_date
            FROM study_logs
            ORDER BY study_date DESC
            """
        ).fetchall()

    if not rows:
        return 0

    study_days = {date.fromisoformat(row["study_date"]) for row in rows}
    streak = 0
    cursor = date.today()
    while cursor in study_days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def get_subject_performance() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT
                subject,
                COUNT(*) AS total_tasks,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks
            FROM tasks
            GROUP BY subject
            ORDER BY subject ASC
            """
        ).fetchall()

    result: list[dict] = []
    for row in rows:
        total = row["total_tasks"]
        completed = row["completed_tasks"]
        completion_rate = (completed / total) if total else 0.0
        result.append(
            {
                "subject": row["subject"],
                "total_tasks": total,
                "completed_tasks": completed,
                "completion_rate": completion_rate,
            }
        )
    return result


def get_recent_subject_hours(days: int = 7) -> list[dict]:
    start_day = (date.today() - timedelta(days=days - 1)).isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT subject, COALESCE(SUM(hours), 0) AS total_hours
            FROM study_logs
            WHERE date(study_date) >= date(?)
            GROUP BY subject
            ORDER BY total_hours ASC
            """,
            (start_day,),
        ).fetchall()
    return [dict(row) for row in rows]
