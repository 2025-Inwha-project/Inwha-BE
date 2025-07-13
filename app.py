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

if __name__ == "__main__":
    app.run(debug=True)
