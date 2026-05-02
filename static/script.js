document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const langSelect = document.getElementById('language-select');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    
    // Mobile Sidebar Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Auto-scroll to bottom of chat
    const scrollToBottom = () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Add a message to the chat
    const addMessage = (text, isUser = false) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-card';
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
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot-message';
        msgDiv.id = 'typing-container';
        msgDiv.appendChild(typingDiv);

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    };

    // Remove typing indicator
    const removeTypingIndicator = () => {
        const indicator = document.getElementById('typing-container');
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
        
        // Close sidebar if on mobile after clicking a suggestion
        if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
        
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
            
            // Artificial delay
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

    // Event Listeners for suggestion buttons (sidebar and bottom)
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.getAttribute('data-query');
            sendMessage(query);
        });
    });
});
