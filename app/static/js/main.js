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
        const messageElement = document.createElement('p');
        messageElement.textContent = `${message.user}: ${message.content}`;

        const timestamp = document.createElement('span');
        timestamp.textContent = `${message.created_at}`;

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

    socket.on('message', (message) => {
        addMessage(message);
    });

});

