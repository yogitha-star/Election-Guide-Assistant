import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Basic rule-based responses if Gemini is not available or for simple queries
RULE_BASED_RESPONSES = {
    "english": {
        "how to vote": "To vote, follow these steps:\n1. Check your name in the voter list.\n2. Go to your designated polling booth.\n3. Show your Voter ID or an approved ID.\n4. Press the button against your chosen candidate on the EVM.\n\nDo you have a voter ID?",
        "what is voter id": "A Voter ID (EPIC) is an identity document issued by the Election Commission. It allows eligible citizens to cast their vote. You can apply for it online through the NVSP portal.",
        "election process": "The election process involves:\n1. Announcement of dates.\n2. Filing of nominations by candidates.\n3. Campaigning.\n4. Voting day.\n5. Counting of votes and declaration of results.",
        "registration steps": "To register to vote:\n1. Visit the official voter registration portal.\n2. Fill out Form 6.\n3. Upload your photo and address proof.\n4. Submit the form. A blo will verify your details.",
        "default": "I'm your Election Guide Assistant. I can help you with 'how to vote', 'what is voter id', 'election process', or 'registration steps'. Please ask a specific question!",
        "yes_voter_id": "Great! You are ready to vote. Check your polling station online before election day.",
        "no_voter_id": "You need to apply for a Voter ID. Visit the official NVSP portal to register online using Form 6."
    },
    "telugu": {
        "how to vote": "ఓటు వేయడానికి, ఈ దశలను అనుసరించండి:\n1. ఓటర్ల జాబితాలో మీ పేరును తనిఖీ చేయండి.\n2. మీకు కేటాయించిన పోలింగ్ బూత్‌కు వెళ్లండి.\n3. మీ ఓటరు ID లేదా ఆమోదించబడిన IDని చూపండి.\n4. EVMలో మీరు ఎంచుకున్న అభ్యర్థికి ఎదురుగా ఉన్న బటన్‌ను నొక్కండి.\n\nమీకు ఓటరు ID ఉందా?",
        "what is voter id": "ఓటర్ ID (EPIC) అనేది ఎన్నికల సంఘం జారీ చేసిన గుర్తింపు పత్రం. ఇది అర్హులైన పౌరులను ఓటు వేయడానికి అనుమతిస్తుంది. మీరు NVSP పోర్టల్ ద్వారా ఆన్‌లైన్‌లో దీని కోసం దరఖాస్తు చేసుకోవచ్చు.",
        "election process": "ఎన్నికల ప్రక్రియలో ఇవి ఉంటాయి:\n1. తేదీల ప్రకటన.\n2. అభ్యర్థుల నామినేషన్ల దాఖలు.\n3. ప్రచారం.\n4. ఓటింగ్ రోజు.\n5. ఓట్ల లెక్కింపు మరియు ఫలితాల ప్రకటన.",
        "registration steps": "ఓటు వేయడానికి నమోదు చేసుకోవడానికి:\n1. అధికారిక ఓటరు నమోదు పోర్టల్‌ను సందర్శించండి.\n2. ఫారం 6 నింపండి.\n3. మీ ఫోటో మరియు చిరునామా రుజువును అప్‌లోడ్ చేయండి.\n4. ఫారమ్‌ను సమర్పించండి. బూత్ లెవల్ ఆఫీసర్ (BLO) మీ వివరాలను ధృవీకరిస్తారు.",
        "default": "నేను మీ ఎన్నికల గైడ్ అసిస్టెంట్‌ని. 'ఓటు ఎలా వేయాలి', 'ఓటరు ID అంటే ఏమిటి', 'ఎన్నికల ప్రక్రియ' లేదా 'నమోదు దశలు' వంటి విషయాల్లో నేను మీకు సహాయం చేయగలను. దయచేసి ఒక నిర్దిష్ట ప్రశ్న అడగండి!",
        "yes_voter_id": "చాలా సంతోషం! మీరు ఓటు వేయడానికి సిద్ధంగా ఉన్నారు. ఎన్నికల రోజుకు ముందు మీ పోలింగ్ స్టేషన్‌ను ఆన్‌లైన్‌లో తనిఖీ చేయండి.",
        "no_voter_id": "మీరు ఓటరు ID కోసం దరఖాస్తు చేసుకోవాలి. ఫారం 6ని ఉపయోగించి ఆన్‌లైన్‌లో నమోదు చేసుకోవడానికి అధికారిక NVSP పోర్టల్‌ను సందర్శించండి."
    }
}

def get_intent(user_input, language="english"):
    input_lower = user_input.lower()
    
    # Handle follow-up responses based on context
    if "yes" in input_lower or "have it" in input_lower or "అవును" in input_lower:
        return "yes_voter_id"
    if "no" in input_lower or "don't" in input_lower or "లేదు" in input_lower:
        return "no_voter_id"

    # Core intents
    if "how to vote" in input_lower or "steps to vote" in input_lower or "ఓటు ఎలా" in input_lower:
        return "how to vote"
    if "voter id" in input_lower or "what is" in input_lower and "id" in input_lower or "ఓటరు id" in input_lower:
        return "what is voter id"
    if "process" in input_lower or "timeline" in input_lower or "ప్రక్రియ" in input_lower:
        return "election process"
    if "register" in input_lower or "registration" in input_lower or "నమోదు" in input_lower:
        return "registration steps"
    
    return "default"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    language = data.get("language", "english")
    
    if not user_message:
        return jsonify({"response": "Please provide a message."}), 400

    # Optional: Integration with Gemini API could go here
    # Since we are building a lightweight reliable assistant first, we use the rule-based system.
    # If API key is available in env vars, we could use it as an advanced fallback.
    
    intent = get_intent(user_message, language)
    
    # Get the appropriate response from our predefined dataset
    bot_response = RULE_BASED_RESPONSES.get(language, RULE_BASED_RESPONSES["english"]).get(intent, RULE_BASED_RESPONSES["english"]["default"])

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
