"""
Fetches comments for a YouTube video using the YouTube Data API v3.
Requires a free API key from Google Cloud Console (YouTube Data API v3 enabled).

If no API key is configured, falls back to a small local sample dataset
(sample_comments.json) so the app is still fully demoable without
network access or an API key — useful for testing/dev.
"""

import os
import re
import json

def extract_video_id(url_or_id):
    """Accepts a full YouTube URL or a bare video ID and returns the video ID."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"^([0-9A-Za-z_-]{11})$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

def fetch_comments(video_url_or_id, max_results=50):
    api_key = os.environ.get("YOUTUBE_API_KEY")
    video_id = extract_video_id(video_url_or_id)

    if not video_id:
        raise ValueError("Could not extract a video ID from that input.")

    if not api_key:
        return _fetch_mock_comments()

    from googleapiclient.discovery import build
    youtube = build("youtube", "v3", developerKey=api_key)

    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=min(max_results, 100),
        textFormat="plainText"
    )
    response = request.execute()

    for item in response.get("items", []):
        text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        comments.append({"author": author, "text": text})

    return comments

def _fetch_mock_comments():
    """Used when no API key is set — lets the app run fully offline for demos."""
    with open("sample_comments.json") as f:
        return json.load(f)
