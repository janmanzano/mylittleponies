# -*- coding: utf-8 -*-
"""Streamlit Deployment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1odYeA5ltOuUUuum3aXk53u3StTIc-hxi
"""

import streamlit as st
import joblib
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')

# Load models and vectorizers
models = {
    "Toxic": joblib.load("model_toxic.pkl"),
    "Racist": joblib.load("model_racist.pkl"),
    "Abusive": joblib.load("model_abusive.pkl"),
    "Obscene": joblib.load("model_obscene.pkl"),
    "Threat": joblib.load("model_threat.pkl"),
    "Provocative": joblib.load("model_provocative.pkl"),
    "Hatespeech": joblib.load("model_hate.pkl"),
    "Nationalist": joblib.load("model_nationalist.pkl"),
    "Religious Hate": joblib.load("model_relhate.pkl")
}

vectorizers = {
    "Toxic": joblib.load("vectorizer_toxic.pkl"),
    "Racist": joblib.load("vectorizer_racist.pkl"),
    "Abusive": joblib.load("vectorizer_abusive.pkl"),
    "Obscene": joblib.load("vectorizer_obscene.pkl"),
    "Threat": joblib.load("vectorizer_threat.pkl"),
    "Provocative": joblib.load("vectorizer_provocative.pkl"),
    "Hatespeech": joblib.load("vectorizer_hate.pkl"),
    "Nationalist": joblib.load("vectorizer_nationalist.pkl"),
    "Religious Hate": joblib.load("vectorizer_relhate.pkl")
}

# Preprocessing function
stemmer = PorterStemmer()
def preprocess(text):
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stopwords.words('english')]
    return ' '.join(words)

# Streamlit UI
st.title("Multi-label Hate Speech Classifier")
user_input = st.text_area("Enter a comment to classify")

if st.button("Classify"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        preprocessed = preprocess(user_input)
        results = {}
        for label, model in models.items():
            vect = vectorizers[label].transform([preprocessed])
            prediction = model.predict(vect)[0]
            results[label] = "✅ Yes" if prediction == 1 else "❌ No"

        st.subheader("Classification Results:")
        for label, result in results.items():
            st.write(f"**{label}**: {result}")
