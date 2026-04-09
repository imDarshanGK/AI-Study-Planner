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
