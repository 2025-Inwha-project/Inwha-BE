# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_config import db
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)  # 모든 도메인 허용 (개발용)

@app.route("/write", methods=["POST"])
def write():
    data = request.get_json()

    item = data.get("item")
    author = data.get("author")
    color = data.get("color")

    if not item or not author or not color:
        return jsonify({"error": "Missing one or more fields"}), 400

    # 현재 시각 timestamp 추가
    timestamp = datetime.now(timezone.utc)

    db.collection("entries").add({
        "item": item,
        "author": author,
        "color": color,
        "timestamp": timestamp
    })

    return jsonify({"message": "Successfully saved"}), 200


from collections import defaultdict

@app.route("/word", methods=["GET"])
def get_words():
    docs = db.collection("entries").stream()

    word_map = defaultdict(lambda: {
        "weight": 0,
        "color": "",
        "latest_timestamp": None,
        "first_timestamp": None
    })

    for doc in docs:
        data = doc.to_dict()
        item = data.get("item")
        timestamp = data.get("timestamp")
        color = data.get("color")

        if item and timestamp:
            if word_map[item]["weight"] == 0:
                word_map[item]["first_timestamp"] = timestamp

            word_map[item]["weight"] += 1
            word_map[item]["latest_timestamp"] = timestamp
            word_map[item]["color"] = color

    # 정렬: 최신 등장 순 (latest_timestamp 기준 내림차순)
    sorted_words = sorted(
        word_map.items(),
        key=lambda x: x[1]["latest_timestamp"],
        reverse=True
    )

    # 상위 20개만 자르기
    result = []
    for item, meta in sorted_words[:20]:
        result.append({
            "item": item,
            "weight": meta["weight"],
            "color": meta["color"],
            "latest_timestamp": meta["latest_timestamp"].isoformat(),
            "first_timestamp": meta["first_timestamp"].isoformat()
        })

    return jsonify(result), 200



if __name__ == "__main__":
    app.run(debug=True)