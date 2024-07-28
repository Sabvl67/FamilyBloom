function submitMood() {
    const userId = document.getElementById('userId').value;
    const mood = document.getElementById('mood').value;
    const description = document.getElementById('description').value;

    fetch('/mood/api/mood', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, mood: mood, description: description })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        loadMoodEntries(userId);
    })
    .catch(error => console.error('Error:', error));
}

function loadMoodEntries(userId) {
    fetch(`/mood/api/mood/${userId}`)
    .then(response => response.json())
    .then(data => {
        const moodEntries = document.getElementById('moodEntries');
        moodEntries.innerHTML = '';
        data.forEach(entry => {
            const entryDiv = document.createElement('div');
            entryDiv.textContent = `${entry.mood} - ${entry.description || ''} (${entry.created_at})`;
            moodEntries.appendChild(entryDiv);
        });
    })
    .catch(error => console.error('Error:', error));
}
