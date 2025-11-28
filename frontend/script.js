async function analyzeTasks() {
    const text = document.getElementById("taskInput").value;

    try {
        const tasks = JSON.parse(text);

        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        });

        const data = await response.json();
        displayResults(data);

    } catch (err) {
        alert("Invalid JSON. Please check your input.");
    }
}

function displayResults(tasks) {
    const resultsDiv = document.getElementById("results");
    const topDiv = document.getElementById("topTasks");

    // Clear previous placeholder or results
    resultsDiv.innerHTML = "";
    topDiv.innerHTML = "";

    if (tasks.length === 0) {
        resultsDiv.innerHTML = "<p>No tasks found.</p>";
        return;
    }

    // Show top 3 tasks
    const topTasks = tasks.slice(0, 3);
    topTasks.forEach(task => {
        let level = getPriorityLevel(task.score);
        topDiv.innerHTML += createTaskCard(task, level);
    });

    // Show all tasks
    tasks.forEach(task => {
        let level = getPriorityLevel(task.score);
        resultsDiv.innerHTML += createTaskCard(task, level);
    });
}

// Determine priority level
function getPriorityLevel(score) {
    if (score >= 80) return "high";
    if (score >= 40) return "medium";
    return "low";
}

// Create HTML for a task card
function createTaskCard(task, level) {
    return `
        <div class="task-card">
            <div class="task-info">
                <h3>${task.title}</h3>
                <p><b>Due:</b> ${task.due_date}</p>
                <p><b>Importance:</b> ${task.importance}</p>
                <p><b>Estimated Hours:</b> ${task.estimated_hours}</p>
                <p><b>Score:</b> ${task.score}</p>
            </div>
            <div class="priority ${level}"></div>
        </div>
    `;
}
