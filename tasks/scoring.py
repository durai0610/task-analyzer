from datetime import date

def calculate_task_score(task_data):
    """
    Calculates a priority score.
    Higher score = higher priority.
    Uses:
      - Urgency (due_date vs today)
      - Importance (1–10)
      - Effort (estimated_hours)
      - Dependencies
    """
    score = 0
    today = date.today()

    # ---- 1. Urgency ----
    due_date = task_data.get('due_date', today)
    if isinstance(due_date, str):
        # if still string, just treat as today
        due_date = today

    days_until_due = (due_date - today).days

    if days_until_due < 0:
        score += 100  # overdue
    elif days_until_due <= 3:
        score += 50   # due very soon

    # ---- 2. Importance (1–10) ----
    importance = task_data.get('importance', 5)
    try:
        importance = int(importance)
    except (ValueError, TypeError):
        importance = 5

    # Clamp between 1 and 10
    importance = max(1, min(importance, 10))
    score += importance * 5

    # ---- 3. Effort (quick wins) ----
    hours = task_data.get('estimated_hours', 1)
    try:
        hours = float(hours)
    except (ValueError, TypeError):
        hours = 1.0

    if hours < 2:
        score += 10  # quick win
    elif hours > 8:
        score -= 5   # very big task, slightly lower

    # ---- 4. Dependencies ----
    deps = task_data.get('dependencies', [])
    if not isinstance(deps, list):
        deps = []
    # Each dependency slightly reduces score
    score -= 5 * len(deps)

    return score
