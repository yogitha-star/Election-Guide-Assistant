from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 🔥 Cache for efficiency
cache = {}

def get_response(msg):
    msg = msg.lower()

    # ✅ Check cache first
    if msg in cache:
        return cache[msg]

    # 🗳️ Logic
    if "how to vote" in msg:
        response = "🗳️ Steps to vote: Check voter list → Go to polling station → Show ID → Vote using EVM."

    elif "voter id" in msg:
        response = "🪪 Voter ID (EPIC) is an identity card issued by Election Commission for voting."

    elif "register" in msg:
        response = "📝 Register via NVSP portal → Fill Form 6 → Upload documents → Submit."

    elif "election process" in msg:
        response = "🗳️ Notification → Nomination → Campaign → Voting → Counting → Results."

    else:
        response = "🤖 Ask about voting, voter ID, registration, or election process."

    # ✅ Store in cache
    cache[msg] = response

    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    return jsonify({"response": get_response(msg)})


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))