# YouTube Comment Sentiment Analyzer

Paste a YouTube video link, and every comment gets classified as positive, negative, or neutral in real time, with a live chart and color-coded comment cards.

## How it works

- **Backend (Flask):** trains a TF-IDF + Naive Bayes sentiment model at startup (reused from the standalone `sentiment-analysis-tool` project, ~94% test accuracy), fetches comments via the YouTube Data API v3, classifies each one, and returns a JSON summary.
- **Frontend:** a single page with a search bar, a live doughnut chart (Chart.js) showing the sentiment split, and individual comment cards color-coded by sentiment.
- **Offline demo mode:** if no API key is configured, the app automatically falls back to a small local sample comment set — so it's fully demoable without any setup.

## Setup

```bash
pip install -r requirements.txt
```

To use real YouTube data:
1. Get a free API key from [Google Cloud Console](https://console.cloud.google.com/) — enable **YouTube Data API v3**, create credentials → API key.
2. Copy `.env.example` to `.env` and paste your key in:
```
YOUTUBE_API_KEY=your_actual_key_here
```
`.env` is already in `.gitignore` — it will never be pushed to GitHub.

## Run

```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

## Tech stack

Python · Flask · scikit-learn (TF-IDF, Naive Bayes) · YouTube Data API v3 · Chart.js
