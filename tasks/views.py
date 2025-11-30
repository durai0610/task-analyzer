from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
import json

from .models import Task
from .scoring import calculate_task_score


def _parse_due_date(value):
    """Helper to safely parse date string 'YYYY-MM-DD'."""
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return date.today()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return date.today()


@csrf_exempt
def analyze_tasks(request):
    """
    POST /api/tasks/analyze/
    Body: JSON array of tasks.
    Returns: same tasks + 'score', sorted by score desc.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

    try:
        tasks = json.loads(request.body or "[]")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON input"}, status=400)

    if not isinstance(tasks, list):
        return JsonResponse({"error": "Input must be a list of tasks"}, status=400)

    if len(tasks) == 0:
        return JsonResponse([], safe=False)

    result = []

    for raw in tasks:
        if not isinstance(raw, dict):
            # skip non-dict entries
            continue

        # Defaults for missing fields
        title = raw.get("title") or "Untitled Task"
        importance = raw.get("importance", 5)
        estimated_hours = raw.get("estimated_hours", 1)
        due_date = _parse_due_date(raw.get("due_date"))
        dependencies = raw.get("dependencies", [])

        task_data = {
            "title": title,
            "importance": importance,
            "estimated_hours": estimated_hours,
            "due_date": due_date,
            "dependencies": dependencies,
        }

        score = calculate_task_score(task_data)

        # convert back to JSON-serializable dict
        result.append({
            "title": title,
            "importance": importance,
            "estimated_hours": estimated_hours,
            "due_date": due_date.isoformat(),
            "dependencies": dependencies,
            "score": score,
        })

    # sort by score desc
    result.sort(key=lambda t: t["score"], reverse=True)
    return JsonResponse(result, safe=False)


@csrf_exempt
def suggest_tasks(request):
    """
    GET /api/tasks/suggest/
    Returns top 3 tasks (from DB) for today or earlier,
    with scores. If DB has none, returns default example tasks.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method. Use GET."}, status=405)

    today = date.today()
    tasks = Task.objects.filter(due_date__lte=today)

    scored = []

    if tasks.exists():
        for t in tasks:
            task_data = {
                "title": t.title,
                "due_date": t.due_date,
                "importance": t.importance,
                "estimated_hours": t.estimated_hours,
                "dependencies": t.dependencies or [],
            }
            score = calculate_task_score(task_data)
            scored.append((score, t))
    else:
        # Default example tasks if DB is empty
        default_tasks = [
            {
                "title": "Finish Django Assignment",
                "due_date": today,
                "importance": 9,
                "estimated_hours": 4,
                "dependencies": [],
            },
            {
                "title": "Fix Critical Bug",
                "due_date": today,
                "importance": 10,
                "estimated_hours": 2,
                "dependencies": [],
            },
            {
                "title": "Prepare Presentation",
                "due_date": today,
                "importance": 7,
                "estimated_hours": 3,
                "dependencies": [],
            },
        ]
        for t in default_tasks:
            score = calculate_task_score(t)
            scored.append((score, t))

    # Sort by score descending and get top 3
    scored.sort(key=lambda x: x[0], reverse=True)
    top3 = scored[:3]

    response = []
    for score, t in top3:
        response.append({
            "title": t["title"] if isinstance(t, dict) else t.title,
            "due_date": (t["due_date"] if isinstance(t, dict) else t.due_date).isoformat() if isinstance(t, dict) else t.due_date.isoformat(),
            "importance": t["importance"] if isinstance(t, dict) else t.importance,
            "estimated_hours": t["estimated_hours"] if isinstance(t, dict) else t.estimated_hours,
            "dependencies": t["dependencies"] if isinstance(t, dict) else (t.dependencies or []),
            "score": score,
            "reason": "High priority based on urgency, importance and effort.",
        })

    return JsonResponse(response, safe=False)
