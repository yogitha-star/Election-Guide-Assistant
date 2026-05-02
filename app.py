from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_response(msg):
    msg = msg.lower()

    if "how to vote" in msg:
        return "🗳️ Steps to vote: Check voter list → Go to polling station → Show ID → Vote using EVM."

    if "voter id" in msg:
        return "🪪 Voter ID (EPIC) is an identity card issued by Election Commission for voting."

    if "register" in msg:
        return "📝 Register via NVSP portal → Fill Form 6 → Upload documents → Submit."

    if "election process" in msg:
        return "🗳️ Notification → Nomination → Campaign → Voting → Counting → Results."

    return "🤖 Ask about voting, voter ID, registration, or election process."

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