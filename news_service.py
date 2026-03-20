
import re, time, requests
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

NEWS_API_KEY = "7339d2263e694d578f970e46fbdf8da5"

SOURCES = {
    "bbc-news":            {"name": "BBC News",         "color": "#c4122c", "bias": "Center"},
    "cnn":                 {"name": "CNN",               "color": "#cc0000", "bias": "Center-Left"},
    "reuters":             {"name": "Reuters",           "color": "#ff8000", "bias": "Center"},
    "al-jazeera-english":  {"name": "Al Jazeera",        "color": "#009944", "bias": "Center-Left"},
    "fox-news":            {"name": "Fox News",          "color": "#003f87", "bias": "Right"},
    "associated-press":    {"name": "AP News",           "color": "#333333", "bias": "Center"},
    "nbc-news":            {"name": "NBC News",          "color": "#fa6700", "bias": "Center-Left"},
    "the-guardian":        {"name": "The Guardian",      "color": "#005689", "bias": "Center-Left"},
    "the-washington-post": {"name": "Washington Post",   "color": "#231f20", "bias": "Center-Left"},
    "sky-news":            {"name": "Sky News",          "color": "#e4003b", "bias": "Center"},
}

_cache = {"data": None, "timestamp": 0}
CACHE_TTL = 1800

def fetch_all_news():
    now = time.time()
    if _cache["data"] and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["data"]
    articles = []
    source_ids = ",".join(SOURCES.keys())
    params = {"sources": source_ids, "pageSize": 100, "apiKey": NEWS_API_KEY, "language": "en"}
    try:
        r = requests.get("https://newsapi.org/v2/top-headlines", params=params, timeout=10)
        for a in r.json().get("articles", []):
            sid = a.get("source", {}).get("id", "")
            if sid not in SOURCES:
                continue
            articles.append({
                "id": len(articles),
                "source_id": sid,
                "source_name": SOURCES[sid]["name"],
                "source_color": SOURCES[sid]["color"],
                "source_bias": SOURCES[sid]["bias"],
                "title": a.get("title") or "",
                "description": a.get("description") or "",
                "url": a.get("url") or "#",
                "publishedAt": a.get("publishedAt") or "",
                "claims": extract_claims((a.get("title") or "") + " " + (a.get("description") or "")),
            })
    except Exception as e:
        print(f"NewsAPI error: {e}")
    result = group_stories(articles)
    _cache["data"] = result
    _cache["timestamp"] = now
    return result

def extract_claims(text):
    claims = []
    for p in re.findall(r"\b(\d+(?:\.\d+)?)\s*(?:percent|%)", text, re.IGNORECASE):
        claims.append({"type": "percentage", "value": f"{p}%"})
    for n, u in re.findall(r"\b(\d{2,})\s*(people|soldiers|troops|dead|killed|injured|wounded|civilians|billion|million|thousand)", text, re.IGNORECASE):
        claims.append({"type": "number", "value": f"{n} {u}"})
    for t, u in re.findall(r"\b(\d+)\s*(hours?|days?|weeks?|months?|years?)\b", text, re.IGNORECASE):
        claims.append({"type": "time", "value": f"{t} {u}"})
    for m, u in re.findall(r"\$\s*(\d+(?:\.\d+)?)\s*(billion|million|trillion|thousand)?", text, re.IGNORECASE):
        claims.append({"type": "money", "value": f"${m} {u}".strip()})
    return claims[:5]

def group_stories(articles):
    if not articles:
        return []
    texts = [a["title"] + " " + a["description"] for a in articles]
    try:
        vec = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf = vec.fit_transform(texts)
        sim = cosine_similarity(tfidf)
    except:
        return [{"topic": a["title"], "articles": [a], "divergence": 0, "claim_conflicts": [], "source_count": 1} for a in articles]
    used, groups = set(), []
    for i in range(len(articles)):
        if i in used:
            continue
        group = [articles[i]]
        used.add(i)
        for j in range(i + 1, len(articles)):
            if j not in used and sim[i][j] > 0.22:
                group.append(articles[j])
                used.add(j)
        source_ids = set(a["source_id"] for a in group)
        topic = re.sub(r"\s*[-|]\s*(BBC|CNN|Reuters|Fox News|Al Jazeera|NBC|AP|Guardian|Washington Post|Sky News).*$", "", articles[i]["title"], flags=re.IGNORECASE).strip()
        conflicts = find_conflicts(group)
        indices = [a["id"] for a in group]
        scores = [1 - sim[indices[x]][indices[y]] for x in range(len(indices)) for y in range(x+1, len(indices)) if indices[x] < sim.shape[0] and indices[y] < sim.shape[0]]
        divergence = round(float(np.mean(scores)) * 100, 1) if scores else 0
        groups.append({"topic": topic, "articles": group, "divergence": divergence, "source_count": len(source_ids), "claim_conflicts": conflicts})
    groups.sort(key=lambda g: (-g["source_count"], -g["divergence"]))
    return groups[:30]

def find_conflicts(group):
    conflicts, claim_map = [], {}
    for article in group:
        for claim in article.get("claims", []):
            claim_map.setdefault(claim["type"], []).append({"source": article["source_name"], "value": claim["value"], "color": article["source_color"]})
    for ctype, entries in claim_map.items():
        if len(set(e["value"] for e in entries)) > 1:
            conflicts.append({"type": ctype, "entries": entries})
    return conflicts[:3]

def get_stats(groups):
    return {
        "total_stories": len(groups),
        "total_articles": sum(len(g["articles"]) for g in groups),
        "total_conflicts": sum(len(g["claim_conflicts"]) for g in groups),
        "multi_source_stories": sum(1 for g in groups if g["source_count"] > 1),
        "last_updated": datetime.utcnow().strftime("%H:%M UTC"),
    }
