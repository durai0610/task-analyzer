import json
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_task_score


@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=400)

    try:
        tasks = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Calculate score for each task
    for task in tasks:
        task["score"] = calculate_task_score(task)

    # Sort by score DESC
    tasks_sorted = sorted(tasks, key=lambda x: x["score"], reverse=True)

    return JsonResponse(tasks_sorted, safe=False)


@csrf_exempt
def suggest_top_tasks(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=400)

    # In a real app we would fetch from DB.
    # For this assignment, return sample.
    example_tasks = [
        {"title": "Complete Django Practice", "due_date": "2025-01-02", "importance": 9, "estimated_hours": 3},
        {"title": "Fix UI Bugs", "due_date": "2024-12-31", "importance": 7, "estimated_hours": 1},
    ]

    for t in example_tasks:
        t["score"] = calculate_task_score(t)

    sorted_tasks = sorted(example_tasks, key=lambda x: x["score"], reverse=True)

    return JsonResponse(sorted_tasks[:3], safe=False)
