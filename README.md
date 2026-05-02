# Election Guide AI Assistant

## Problem Statement
Navigating the election process, understanding voter ID requirements, and finding election timelines can be confusing for many citizens, especially first-time voters. Information is often scattered across various official documents and websites.

## Solution
The **Election Guide AI Assistant** is an interactive, user-friendly chatbot designed to simplify the voting process. It guides users step-by-step through election procedures, voter registration, and voter ID queries. 

## Features
- 💬 **Interactive Chat Interface**: Clean, modern, and mobile-responsive UI inspired by top AI assistants.
- 🌐 **Multi-language Support**: Easily switch between English and Telugu.
- ⚡ **Quick Suggestions**: One-click buttons for common queries like "How to vote" and "Registration steps".
- 🌗 **Light/Dark Theme**: Integrated theme toggle for user preference.
- 🔄 **Guided Flows**: Follow-up questions to understand user context (e.g., asking if they have a voter ID).

## Tech Stack
- **Frontend**: HTML5, CSS3 (Custom properties, Flexbox), Vanilla JavaScript
- **Backend**: Python, Flask
- **AI/Logic**: Rule-based fallback system (Ready for Google Gemini API integration)

## Project Structure
```text
Election-Guide-Assistant/
│
├── app.py                  # Main Flask application and routing
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/
│   └── index.html          # Main HTML UI
│
└── static/
    ├── style.css           # Modern CSS styling and themes
    └── script.js           # Frontend logic, Fetch API, animations
```

## How to Run

1. **Prerequisites**: Ensure you have Python 3.x installed.
2. **Clone/Navigate** to the project directory.
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python app.py
   ```
5. **Access the App**: Open your browser and go to `http://127.0.0.1:5000/`.

## Google Services Integration
- Google Cloud App Engine (Deployment)
- Google Antigravity (Development Platform)
- Designed for integration with Google Gemini API

## Testing
Basic testing implemented using pytest:
- Home page test
- Chat response test
- Empty input handling
- Unknown query handling

## Efficiency
- Lightweight rule-based NLP
- Caching used for faster responses
