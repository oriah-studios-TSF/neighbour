// Section apperance for all sections and navigation activeness (using active class) making sure that Home button is active by default
document.addEventListener('DOMContentLoaded', () => {
    const buttons = {
        homeBtn: document.getElementById('homeBtn'),
        chatBtn: document.getElementById('chatBtn'),
        alertBtn: document.getElementById('alertBtn'),
        profileBtn: document.getElementById('profileBtn')
    };

    const sections = {
        home: document.getElementById('home'),
        chat: document.getElementById('chat'),
        alerts: document.getElementById('alerts'),
        profile: document.getElementById('profile')
    };
    
    // Reusable function
    function activateSection(activeBtn, activeSection) {
        // Remove active class from all buttons
        Object.values(buttons).forEach(button => {
            button.classList.remove('active');
        });
        // Remove active class from all sections
        Object.values(sections).forEach(section => {
            section.style.display = 'none';
        });
        // Add active class to clicked button
        activeBtn.classList.add('active');
        activeSection.style.display = 'block';
    }

    // Activate home section by default
    activateSection(buttons.homeBtn, sections.home);

    // Event listeners
    buttons.homeBtn.addEventListener('click', () => {
        activateSection(buttons.homeBtn, sections.home);
    });

    buttons.chatBtn.addEventListener('click', () => {
        activateSection(buttons.chatBtn, sections.chat);
    });

    buttons.alertBtn.addEventListener('click', () => {
        activateSection(buttons.alertBtn, sections.alerts);
    });

    buttons.profileBtn.addEventListener('click', () => {
        activateSection(buttons.profileBtn, sections.profile);
    });


    // Socket
    const socket = io();
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');

    function addMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');

        const userElement = document.createElement('span');
        userElement.classList.add('chat-user');
        userElement.textContent = `${message.user}`;

        messageElement.appendChild(userElement);

        const messageContent = document.createElement('span');
        messageContent.classList.add('chat-message-content');
        messageContent.textContent = `${message.content}`;

        messageElement.appendChild(messageContent);


        const timestamp = document.createElement('span');
        const date = new Date(message.created_at + 'Z');

        timestamp.classList.add('chat-message-timestamp');
        timestamp.textContent = date.toLocaleString([], {hour: '2-digit', minute: '2-digit'}); // With proper date format and date

        messageElement.appendChild(timestamp);
        chatMessages.appendChild(messageElement);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendMessageBtn.addEventListener('click', () => {
        const content = chatInput.value.trim();

        if (!content) {
            return;
        }

        socket.emit('send_message', {
            content: content,
        });
        
        chatInput.value = '';
        chatInput.focus();

    });

    chatInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessageBtn.click();
        }
    });

    socket.on('chat_history', (messages) => {
        chatMessages.innerHTML = '';

        messages.forEach(message => {
            addMessage(message);
        });
    });

    socket.emit('request_chat_history');
    

    socket.on('new_message', (message) => {
        addMessage(message);
    });




});

