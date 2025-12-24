document.addEventListener('DOMContentLoaded', () => {
    const messagesDiv = document.getElementById('messages');
    const form = document.getElementById('chat-form');
    const input = document.getElementById('message-input');
    const clearBtn = document.getElementById('clear-btn');

    // Load history
    fetch('/api/history')
        .then(res => res.json())
        .then(data => {
            data.forEach(msg => addMessageToUI(msg.role, msg.content));
        });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = input.value.trim();
        if (!content) return;

        // Add user message to UI immediately
        addMessageToUI('user', content);
        input.value = '';

        // Send to API
        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content })
            });
            const data = await res.json();
            addMessageToUI(data.role, data.content);
        } catch (err) {
            console.error('Error:', err);
            addMessageToUI('assistant', 'Error sending message.');
        }
    });

    clearBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear chat history?')) {
            await fetch('/api/history', { method: 'DELETE' });
            messagesDiv.innerHTML = '';
        }
    });

    function addMessageToUI(role, content) {
        const div = document.createElement('div');
        div.className = `message ${role}`;
        div.textContent = content;
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
