document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
});

function loadTasks() {
    fetch('/tasks/api/tasks')
    .then(response => response.json())
    .then(data => {
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';
        data.forEach(task => {
            const taskDiv = document.createElement('div');
            taskDiv.textContent = `${task.description} - ${task.status} (Assigned to: ${task.assignedTo})`;
            taskList.appendChild(taskDiv);
        });
    })
    .catch(error => console.error('Error:', error));
}

function assignTasks() {
    fetch('/tasks/api/tasks/assign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        loadTasks();
    })
    .catch(error => console.error('Error:', error));
}

function deferTask(taskId, memberId) {
    fetch('/tasks/api/tasks/defer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task_id: taskId, member_id: memberId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        loadTasks();
    })
    .catch(error => console.error('Error:', error));
}
