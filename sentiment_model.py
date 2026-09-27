"""
Trains a TF-IDF + Naive Bayes sentiment classifier at startup (training
takes under a second on this dataset size, so no need to persist a
model file — this keeps the repo lightweight and the model always
reproducible from source).
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def train_model(data_path="data.csv"):
    df = pd.read_csv(data_path)
    X, y = df["text"], df["label"]

    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)

    return model, vectorizer

def predict_sentiment(text, model, vectorizer):
    vec = vectorizer.transform([text])
    label = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]
    confidence = float(max(probs))
    return label, confidence
