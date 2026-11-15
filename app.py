import random
import joblib
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    history = request.json['history']        # the whole conversation so far

    r = requests.post(
        'http://localhost:11434/api/chat',   # Ollama's address on your computer
        json={'model': 'llama3.2', 'messages': history, 'stream': False},
        timeout=120
    )
    reply = r.json()['message']['content']
    return jsonify({'reply': reply})

if __name__ == "__main__":
    app.run(debug=True)