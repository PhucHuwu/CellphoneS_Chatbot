from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_pipeline import get_answer_from_query, build_index


app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Thiếu câu hỏi đầu vào."}), 400
    result = get_answer_from_query(query)
    return jsonify(result)


@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


if __name__ == "__main__":
    build_index()
    app.run(host="0.0.0.0", port=8000, debug=True)
