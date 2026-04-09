from __future__ import annotations

from datetime import date, datetime

from sklearn.linear_model import LinearRegression


def _days_left(deadline_iso: str) -> int:
    deadline = date.fromisoformat(deadline_iso)
    return (deadline - date.today()).days


def heuristic_priority(task: dict) -> float:
    # Deadline component follows the simple base rule: nearer deadlines increase priority.
    days_left = _days_left(task["deadline"])
    deadline_score = max(0, 14 - days_left)
    difficulty_score = float(task["difficulty"])
    importance_score = float(task["importance"])
    workload_score = float(task["estimated_hours"]) * 0.5
    return deadline_score + difficulty_score + importance_score + workload_score


def _build_training_data(completed_tasks: list[dict]) -> tuple[list[list[float]], list[float]]:
    x_data: list[list[float]] = []
    y_data: list[float] = []
    for task in completed_tasks:
        if not task.get("completed_at"):
            continue
        completed_day = datetime.fromisoformat(task["completed_at"]).date()
        deadline_day = date.fromisoformat(task["deadline"])

        delay_days = (completed_day - deadline_day).days
        on_time_bonus = 10.0 if delay_days <= 0 else max(0.0, 10.0 - delay_days)
        target_score = (
            float(task["difficulty"]) + float(task["importance"]) + on_time_bonus + float(task["estimated_hours"]) * 0.5
        )

        x_data.append(
            [
                float(task["difficulty"]),
                float(task["importance"]),
                float(task["estimated_hours"]),
                float(max(0, 14 - _days_left(task["deadline"]))),
            ]
        )
        y_data.append(target_score)
    return x_data, y_data


def score_tasks(pending_tasks: list[dict], completed_tasks: list[dict]) -> list[dict]:
    scored: list[dict] = []
    model: LinearRegression | None = None

    x_data, y_data = _build_training_data(completed_tasks)
    if len(x_data) >= 5:
        model = LinearRegression()
        model.fit(x_data, y_data)

    for task in pending_tasks:
        heuristic = heuristic_priority(task)
        ml_adjustment = 0.0
        if model is not None:
            features = [
                float(task["difficulty"]),
                float(task["importance"]),
                float(task["estimated_hours"]),
                float(max(0, 14 - _days_left(task["deadline"]))),
            ]
            prediction = float(model.predict([features])[0])
            ml_adjustment = 0.25 * prediction

        final_score = round(heuristic + ml_adjustment, 2)
        remaining_hours = max(0.0, float(task["estimated_hours"]) - float(task.get("logged_hours", 0)))

        enriched = dict(task)
        enriched["priority_score"] = final_score
        enriched["remaining_hours"] = round(remaining_hours, 2)
        scored.append(enriched)

    scored.sort(key=lambda t: (-t["priority_score"], t["deadline"]))
    return scored


def recommend_next_task(scored_tasks: list[dict]) -> dict | None:
    for task in scored_tasks:
        if task["remaining_hours"] > 0 and task["status"] == "pending":
            return task
    return None
