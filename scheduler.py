from __future__ import annotations

from datetime import date, timedelta


def generate_timetable(scored_tasks: list[dict], daily_hours: float, days: int = 7) -> list[dict]:
    if daily_hours <= 0:
        return []

    work_items = []
    for task in scored_tasks:
        if task["remaining_hours"] <= 0 or task["status"] != "pending":
            continue
        task_copy = dict(task)
        task_copy["remaining_hours"] = float(task["remaining_hours"])
        work_items.append(task_copy)

    schedule: list[dict] = []
    current_day = date.today()

    for day_offset in range(days):
        day_date = current_day + timedelta(days=day_offset)
        capacity = float(daily_hours)
        if not work_items:
            break

        for task in work_items:
            if capacity <= 0:
                break
            if task["remaining_hours"] <= 0:
                continue

            allocated = min(capacity, task["remaining_hours"])
            if allocated <= 0:
                continue

            schedule.append(
                {
                    "date": day_date.isoformat(),
                    "subject": task["subject"],
                    "task": task["title"],
                    "hours": round(allocated, 2),
                }
            )

            task["remaining_hours"] -= allocated
            capacity -= allocated

        work_items = [task for task in work_items if task["remaining_hours"] > 0]

    return schedule


def _priority_for_week(task: dict, weak_subject: str | None, weak_allocated: float, weak_target: float) -> float:
    completion_probability = float(task.get("completion_probability", 0.5))
    days_left = max(0, (date.fromisoformat(task["deadline"]) - date.today()).days)
    urgency = max(0.0, 1.0 - (days_left / 14.0))
    computed_risk = ((1.0 - completion_probability) * 0.7 + urgency * 0.3) * 100.0

    base_priority = float(task.get("delay_risk_score", computed_risk)) + float(task.get("priority_score", 0.0))
    weak_bonus = 0.0
    if weak_subject and weak_subject != "None" and task["subject"] == weak_subject and weak_allocated < weak_target:
        weak_bonus = 22.0

    return base_priority + weak_bonus


def generate_weekly_action_plan(
    scored_tasks: list[dict],
    daily_hours: float,
    weak_subject: str | None,
    days: int = 7,
) -> list[dict]:
    if daily_hours <= 0 or days <= 0:
        return []

    work_items: list[dict] = []
    for task in scored_tasks:
        if task.get("status") != "pending":
            continue
        remaining = float(task.get("remaining_hours", 0.0))
        if remaining <= 0:
            continue
        cloned = dict(task)
        cloned["remaining_hours"] = remaining
        work_items.append(cloned)

    if not work_items:
        return []

    weekly_capacity = float(daily_hours) * float(days)
    weak_target = 0.30 * weekly_capacity
    weak_allocated = 0.0
    plan: list[dict] = []

    for day_offset in range(days):
        if not work_items:
            break

        day_date = date.today() + timedelta(days=day_offset)
        capacity = float(daily_hours)

        while capacity > 0 and work_items:
            ranked = sorted(
                work_items,
                key=lambda item: (
                    -_priority_for_week(item, weak_subject, weak_allocated, weak_target),
                    item["deadline"],
                ),
            )
            task = ranked[0]
            block = min(1.5, capacity, float(task["remaining_hours"]))
            if block <= 0:
                break

            focus_type = "risk-priority"
            if weak_subject and weak_subject != "None" and task["subject"] == weak_subject and weak_allocated < weak_target:
                focus_type = "weak-subject-balance"

            plan.append(
                {
                    "date": day_date.isoformat(),
                    "subject": task["subject"],
                    "task": task["title"],
                    "hours": round(block, 2),
                    "focus_type": focus_type,
                }
            )

            task["remaining_hours"] = round(float(task["remaining_hours"]) - block, 4)
            capacity = round(capacity - block, 4)

            if weak_subject and weak_subject != "None" and task["subject"] == weak_subject:
                weak_allocated += block

            work_items = [item for item in work_items if float(item["remaining_hours"]) > 0]

    return plan
