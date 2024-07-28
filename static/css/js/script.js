document.addEventListener('DOMContentLoaded', function() {
    const moodForm = document.getElementById('moodForm');
    const moodEntries = document.getElementById('moodEntries');
    const userId = document.getElementById('userId').value;

    moodForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const mood = document.getElementById('mood').value;
        const description = document.getElementById('description').value;

        fetch('/api/mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, mood: mood, description: description })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Mood entry created') {
                loadMoodEntries();
            }
        });
    });

    function loadMoodEntries() {
        fetch(`/api/mood/${userId}`)
            .then(response => response.json())
            .then(entries => {
                moodEntries.innerHTML = '';
                entries.forEach(entry => {
                    const entryDiv = document.createElement('div');
                    entryDiv.classList.add('mood-entry');
                    entryDiv.innerHTML = `
                        <p><strong>Mood:</strong> ${entry.mood}</p>
                        <p><strong>Description:</strong> ${entry.description}</p>
                        <p><small><strong>Date:</strong> ${new Date(entry.created_at).toLocaleString()}</small></p>
                    `;
                    moodEntries.appendChild(entryDiv);
                });
            });
    }

    loadMoodEntries();
});
