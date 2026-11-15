const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const box = document.getElementById('chat-box');

// history
let history = [];
try {
    history = JSON.parse(localStorage.getItem('meowHistory')) || [];
} catch (e) {
    history = [];
}

function saveHistory() {
    if (history.length > 100) history = history.slice(-100);   // keep it from growing forever
    try {
        localStorage.setItem('meowHistory', JSON.stringify(history));
    } catch (e) {}
}

function addMessage(text, who) {
    const div = document.createElement('div');
    div.className = 'message ' + who;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    return div;
}

// show saved convo
history.forEach(m => addMessage(m.content, m.role === 'user' ? 'user' : 'bot'));

// send new msg
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    history.push({ role: 'user', content: text });
    saveHistory();
    input.value = '';

    const thinking = addMessage('...', 'bot');

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, history: history })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.reply || 'Server error');

        thinking.textContent = data.reply;
        history.push({ role: 'assistant', content: data.reply });
        saveHistory();
    } catch (err) {
        thinking.textContent = 'Something went wrong. Check the Flask terminal for the error.';
    }
    box.scrollTop = box.scrollHeight;
});