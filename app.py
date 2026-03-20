
from flask import Flask, render_template, jsonify
from news_service import fetch_all_news, get_stats

app = Flask(__name__)

@app.route("/")
def index():
    groups = fetch_all_news()
    stats = get_stats(groups)
    return render_template("index.html", groups=groups, stats=stats)

@app.route("/api/refresh")
def refresh():
    from news_service import _cache
    _cache["timestamp"] = 0
    groups = fetch_all_news()
    stats = get_stats(groups)
    return jsonify({"status": "ok", "stats": stats})

@app.route("/api/stories")
def stories_api():
    groups = fetch_all_news()
    stats = get_stats(groups)
    return jsonify({"stories": groups, "stats": stats})
