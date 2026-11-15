import pandas as pd
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Minimum confidence required
CONFIDENCE_THRESHOLD = 0.65

def translate_cat(text):

    # Get prediction probabilities
    probabilities = model.predict_proba([text])[0]

    # Find the most likely meaning
    best_index = probabilities.argmax()

    confidence = probabilities[best_index]

    prediction = model.classes_[best_index]

    # Check confidence threshold
    if confidence < CONFIDENCE_THRESHOLD:
        return "I don't recognize this cat sound!"

    return prediction

df = pd.read_csv('meow_data2.csv')            # columns: text, meaning

model = make_pipeline(
    TfidfVectorizer(analyzer='char', ngram_range=(1, 4), lowercase=False),
    LogisticRegression(max_iter=2000)
)
model.fit(df['text'], df['meaning'])

joblib.dump(model, 'meow_model.pkl')         # saves the trained pipeline
print('saved!')