import random
from flask import Flask, render_template
import joblib
import numpy as np
from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

try:
    model = joblib.load('meow_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

responses = {
    "greeting": ["Oh hi, I just noticed you.", "Hello, human. You may proceed.","MEoo hi human :3"],
    "excited greeting": ["YOU'RE HOME! I missed you so much!", "Hi hi hi hi! Where were you?!"],
    "demands food": ["I NEED WORMS :3 I'm hungy", "Hungy ToT"],
    "wants attention": ["LOOK AT MEE PWEASE :3", "Pet me. THIS IS A COMMAND"],
    "complaint": ["EXCUSE ME :(", "MEANIE"],
    "distress or confusion": ["Where are you?? I can't find you!", "It's dark and I'm confused. Come get me."],
    "playful": ["Meooo I wanna play", "Chase me! Chase me! Chase me!"],
    "kitten calling": ["Mama? Where are you? I'm little!", "I'm cold and hungry, come here please."],
    "follow me": ["Follow me, I want to show you something.", "Hey, this way! Keep up!"],
    "friendly greeting": ["Hello, friend. I'm happy to see you.", "Oh good, you're here. Everything's fine now."],
    "excited about prey": ["THERE IS A BIRD. I MUST GET IT.", "Why is the window in the way. I am a hunter."],
    "content": [":D HAPPEH", "I am the happiest cat in the world right now :D"],
    "stressed or self-soothing": ["I'm nervous. Please stay close to me.", "I'm trying to stay calm, but I'm scared."],
    "fear or defensive": ["Back off.", "HISSSSSSSSSSSSS >:("],
    "warning": ["Warning u, my food hymp", "Take one more step. I dare you."],
    "angry or aggressive": ["Touch me and you will regret it.", "This is MY territory. Leave. Now."],
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    if model is None:
        return jsonify({'reply': 'Model not loaded.'}), 500

    data = request.get_json()
    meow = data['message']                    #new text to translate
    history = data.get('history', [])         # convo history

    label = str(model.predict([meow])[0])
    confidence = float(model.predict_proba([meow]).max())
    reply = random.choice(responses.get(label, ["...(the cat stares at you)"]))

    return jsonify({'reply': reply, 'label': label,
                    'confidence': round(confidence, 2)})

if __name__ == "__main__":
    app.run(debug=True)