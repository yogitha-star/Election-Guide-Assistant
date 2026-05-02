document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const themeToggle = document.getElementById('theme-toggle');
    const langSelect = document.getElementById('language-select');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');

    // Theme Toggle Logic
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode');
        
        if (document.body.classList.contains('dark-mode')) {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'inline';
        } else {
            sunIcon.style.display = 'inline';
            moonIcon.style.display = 'none';
        }
    });

    // Auto-scroll to bottom of chat
    const scrollToBottom = () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Add a message to the chat
    const addMessage = (text, isUser = false) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        msgDiv.appendChild(contentDiv);
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    };

    // Show typing indicator
    const showTypingIndicator = () => {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    };

    // Remove typing indicator
    const removeTypingIndicator = () => {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    };

    // Handle sending a message to backend
    const sendMessage = async (messageText) => {
        if (!messageText.trim()) return;

        // 1. Show user message
        addMessage(messageText, true);
        userInput.value = '';
        
        // 2. Show typing indicator
        showTypingIndicator();

        const language = langSelect.value;

        try {
            // 3. Fetch from backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText, language: language })
            });

            const data = await response.json();
            
            // Artificial delay to make typing animation visible and feel more "human"
            setTimeout(() => {
                removeTypingIndicator();
                if (data.response) {
                    addMessage(data.response, false);
                } else {
                    addMessage("Sorry, I couldn't process that.", false);
                }
            }, 800);

        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage("Error connecting to the server. Please try again later.", false);
        }
    };

    // Event Listeners for sending
    sendBtn.addEventListener('click', () => {
        sendMessage(userInput.value);
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(userInput.value);
        }
    });

    // Event Listeners for suggestion buttons
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.getAttribute('data-query');
            sendMessage(query);
        });
    });
});
