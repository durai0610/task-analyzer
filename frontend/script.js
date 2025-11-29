const API_BASE = window.location.hostname === "localhost"
  ? "http://127.0.0.1:8000"
  : "https://task-analyzer-backend.onrender.com";

async function analyzeTasks() {
    const text = document.getElementById("taskInput").value;

    let tasks;
    try {
        tasks = JSON.parse(text);
    } catch (err) {
        alert("Invalid JSON. Please check your input.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/tasks/analyze/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend error:", errorText);
            alert("Backend error. Check console/logs.");
            return;
        }

        const data = await response.json();
        displayResults(data);
    } catch (err) {
        console.error(err);
        alert("Network error. Check API_BASE URL or server.");
    }
}

function displayResults(tasks) {
    const topDiv = document.getElementById("topTasks");
    const resultsDiv = document.getElementById("results");

    topDiv.innerHTML = "";
    resultsDiv.innerHTML = "";

    if (!tasks || tasks.length === 0) {
        resultsDiv.innerHTML = '<p class="placeholder">No tasks found.</p>';
        return;
    }

    // Top 3
    const top3 = tasks.slice(0, 3);
    top3.forEach(task => {
        const level = getPriorityLevel(task.score);
        topDiv.innerHTML += createTaskCard(task, level);
    });

    // All tasks
    tasks.forEach(task => {
        const level = getPriorityLevel(task.score);
        resultsDiv.innerHTML += createTaskCard(task, level);
    });
}

function getPriorityLevel(score) {
    if (score >= 80) return "high";
    if (score >= 40) return "medium";
    return "low";
}

function createTaskCard(task, level) {
    return `
        <div class="task-card">
            <div class="task-info">
                <h3>${task.title}</h3>
                <p><b>Due:</b> ${task.due_date}</p>
                <p><b>Importance:</b> ${task.importance}</p>
                <p><b>Estimated Hours:</b> ${task.estimated_hours}</p>
                <p><b>Dependencies:</b> ${Array.isArray(task.dependencies) ? task.dependencies.length : 0}</p>
                <p><b>Score:</b> ${task.score}</p>
            </div>
            <div class="priority ${level}"></div>
        </div>
    `;
}

function loadExample() {
    const example = [
        {
            "title": "Fix Critical Bug",
            "due_date": "2025-11-28",
            "importance": 10,
            "estimated_hours": 2,
            "dependencies": [1]
        },
        {
            "title": "Finish Django Assignment",
            "due_date": "2025-11-30",
            "importance": 9,
            "estimated_hours": 4,
            "dependencies": []
        },
        {
            "title": "Team Meeting",
            "due_date": "2025-11-29",
            "importance": 5,
            "estimated_hours": 1,
            "dependencies": []
        },
        {
            "title": "Prepare Presentation",
            "due_date": "2025-12-05",
            "importance": 7,
            "estimated_hours": 3,
            "dependencies": []
        },
        {
            "title": "Quick Code Refactor",
            "due_date": "2025-12-10",
            "importance": 6,
            "estimated_hours": 1,
            "dependencies": []
        },
        {
            "title": "Write Documentation",
            "due_date": "2025-12-15",
            "importance": 4,
            "estimated_hours": 2,
            "dependencies": []
        }
    ];

    document.getElementById("taskInput").value = JSON.stringify(example, null, 2);
}
