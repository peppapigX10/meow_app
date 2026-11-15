const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const box = document.getElementById('chat-box');

const history = [];   // remembers the conversation

function addMessage(text, who) {
    const div = document.createElement('div');
    div.className = 'message ' + who;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    return div;                       // so we can change it later
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    history.push({ role: 'user', content: text });
    input.value = '';

    const thinking = addMessage('...', 'bot');   // "typing" bubble

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ history: history })
        });
        const data = await res.json();
        thinking.textContent = data.reply;        // swap "..." for the answer
        history.push({ role: 'assistant', content: data.reply });
    } catch (err) {
        thinking.textContent = 'Could not reach the AI. Is Ollama running?';
    }
    box.scrollTop = box.scrollHeight;
});