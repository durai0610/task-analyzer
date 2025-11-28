from datetime import date

def calculate_task_score(task_data):
    """
    Calculate a priority score for each task.
    Higher score = higher priority.
    """

    score = 0
    today = date.today()

    # ----- 1. Urgency -----
    due_date = task_data.get("due_date")
    if isinstance(due_date, str):
        due_date = date.fromisoformat(due_date)

    days_left = (due_date - today).days

    if days_left < 0:
        score += 100          # Overdue
    elif days_left <= 3:
        score += 50           # Due soon
    else:
        score += max(0, 20 - days_left)  # Gradual urgency

    # ----- 2. Importance -----
    importance = task_data.get("importance", 5)
    score += importance * 5

    # ----- 3. Effort Bonus -----
    hours = task_data.get("estimated_hours", 1)
    if hours < 2:
        score += 10  # quick task bonus

    # ----- 4. Dependencies -----
    deps = task_data.get("dependencies", [])
    if deps:
        score -= len(deps) * 5  # more dependencies = slightly lower priority

    return score
