from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from sentiment_model import train_model, predict_sentiment
from youtube_fetch import fetch_comments

load_dotenv()  # reads YOUTUBE_API_KEY from a local .env file, never committed to git

app = Flask(__name__)

print("Training sentiment model...")
model, vectorizer = train_model("data.csv")
print("Model ready.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    video_url = data.get("video_url", "").strip()

    if not video_url:
        return jsonify({"error": "Please provide a YouTube video URL or ID."}), 400

    try:
        comments = fetch_comments(video_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if not comments:
        return jsonify({"error": "No comments found for this video."}), 404

    results = []
    counts = {"positive": 0, "negative": 0, "neutral": 0}

    for c in comments:
        label, confidence = predict_sentiment(c["text"], model, vectorizer)
        counts[label] += 1
        results.append({
            "author": c["author"],
            "text": c["text"],
            "sentiment": label,
            "confidence": round(confidence * 100, 1)
        })

    total = len(results)
    summary = {
        "total": total,
        "positive": counts["positive"],
        "negative": counts["negative"],
        "neutral": counts["neutral"],
        "positive_pct": round(counts["positive"] / total * 100, 1),
        "negative_pct": round(counts["negative"] / total * 100, 1),
        "neutral_pct": round(counts["neutral"] / total * 100, 1),
    }

    return jsonify({"summary": summary, "comments": results})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
