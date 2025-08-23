from flask import Flask, request, jsonify   # ✅ FIXED: added request & jsonify imports

app = Flask(__name__)

# --- Flask Route ---
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400

    user_query = data.get("query")
    name = data.get("name", "user")
    age = data.get("age", 18)

    result = get_response(user_query, name, age)

    # ✅ Format only the keys you want in response
    filtered_result = {
        "response": result.get("final_response", ""),
        "related_doctor": result.get("respective_doctor", "")
    }

    return jsonify(filtered_result), 200

# --- Run Server ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
