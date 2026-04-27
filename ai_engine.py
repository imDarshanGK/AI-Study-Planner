from __future__ import annotations

from datetime import date, datetime

from sklearn.ensemble import RandomForestClassifier
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


def _build_completion_dataset(all_tasks: list[dict]) -> tuple[list[list[float]], list[int]]:
    x_data: list[list[float]] = []
    y_data: list[int] = []

    for task in all_tasks:
        estimated = max(0.1, float(task["estimated_hours"]))
        logged_ratio = min(2.0, float(task.get("logged_hours", 0.0)) / estimated)
        features = [
            float(task["difficulty"]),
            float(task["importance"]),
            float(task["estimated_hours"]),
            float(_days_left(task["deadline"])),
            float(logged_ratio),
        ]
        label = 1 if task["status"] == "completed" else 0

        x_data.append(features)
        y_data.append(label)

    return x_data, y_data


def score_tasks(pending_tasks: list[dict], completed_tasks: list[dict], all_tasks: list[dict]) -> list[dict]:
    scored: list[dict] = []
    score_model: LinearRegression | None = None
    completion_model: RandomForestClassifier | None = None

    x_data, y_data = _build_training_data(completed_tasks)
    if len(x_data) >= 5:
        score_model = LinearRegression()
        score_model.fit(x_data, y_data)

    completion_x, completion_y = _build_completion_dataset(all_tasks)
    if len(completion_x) >= 10 and len(set(completion_y)) >= 2:
        completion_model = RandomForestClassifier(n_estimators=150, random_state=42)
        completion_model.fit(completion_x, completion_y)

    for task in pending_tasks:
        heuristic = heuristic_priority(task)
        ml_adjustment = 0.0
        if score_model is not None:
            features = [
                float(task["difficulty"]),
                float(task["importance"]),
                float(task["estimated_hours"]),
                float(max(0, 14 - _days_left(task["deadline"]))),
            ]
            prediction = float(score_model.predict([features])[0])
            ml_adjustment = 0.25 * prediction

        completion_probability = 0.5
        if completion_model is not None:
            estimated = max(0.1, float(task["estimated_hours"]))
            logged_ratio = min(2.0, float(task.get("logged_hours", 0.0)) / estimated)
            completion_features = [
                float(task["difficulty"]),
                float(task["importance"]),
                float(task["estimated_hours"]),
                float(_days_left(task["deadline"])),
                float(logged_ratio),
            ]
            completion_probability = float(completion_model.predict_proba([completion_features])[0][1])

        # Risk boost prioritizes tasks likely to be missed unless acted on now.
        risk_boost = (1.0 - completion_probability) * 4.0

        final_score = round(heuristic + ml_adjustment + risk_boost, 2)
        remaining_hours = max(0.0, float(task["estimated_hours"]) - float(task.get("logged_hours", 0)))

        enriched = dict(task)
        enriched["priority_score"] = final_score
        enriched["remaining_hours"] = round(remaining_hours, 2)
        enriched["completion_probability"] = round(completion_probability, 2)
        scored.append(enriched)

    scored.sort(key=lambda t: (-t["priority_score"], t["deadline"]))
    return scored


def recommend_next_task(
    scored_tasks: list[dict],
    weak_subject: str | None,
    recent_subject_hours: list[dict],
) -> tuple[dict | None, str, list[str]]:
    hours_map = {row["subject"]: float(row["total_hours"]) for row in recent_subject_hours}

    best_task: dict | None = None
    best_score = -1.0
    best_reasons: list[str] = []

    for task in scored_tasks:
        if task["remaining_hours"] <= 0 or task["status"] != "pending":
            continue

        subject = task["subject"]
        behavior_score = float(task["priority_score"])
        reasons = ["high priority"]

        if weak_subject and subject == weak_subject:
            behavior_score += 3.0
            reasons.append("low completion rate in this subject")

        recent_hours = hours_map.get(subject, 0.0)
        if recent_hours < 2.0:
            behavior_score += 2.0
            reasons.append("low recent study time")

        completion_probability = float(task.get("completion_probability", 0.5))
        if completion_probability < 0.45:
            behavior_score += 1.0
            reasons.append("high delay risk")

        if behavior_score > best_score:
            best_score = behavior_score
            best_task = task
            best_reasons = reasons

    if best_task is None:
        return None, "No recommendation available.", []

    reason_text = ", ".join(best_reasons)
    message = (
        f"Based on your past behavior, you should study {best_task['subject']} today: "
        f"{best_task['title']} ({reason_text})."
    )
    return best_task, message, best_reasons
