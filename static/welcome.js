// Welcome section handling
function initializeWelcomeSection() {
    const startChatBtn = document.getElementById('startChatBtn');
    const welcomeSections = document.getElementById('welcomeSections');
    const chatMessages = document.getElementById('chatMessages');

    function showChat() {
        welcomeSections.style.display = 'none';
        chatMessages.style.display = 'block';
    }

    function showWelcome() {
        welcomeSections.style.display = 'block';
        chatMessages.style.display = 'none';
        chatMessages.innerHTML = '<div id="traditionalBubble"></div><div id="modernBubble"></div>';
    }

    // Event listeners
    startChatBtn?.addEventListener('click', showChat);

    // Handle New Chat link
    document.querySelector('a[href="user.html"]')?.addEventListener('click', function(e) {
        e.preventDefault();
        showWelcome();
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeWelcomeSection);
