// Session Chat JS
const sidebar = document.getElementById('sidebar');
const openSidebarBtn = document.getElementById('openSidebar');
const closeSidebarBtn = document.getElementById('closeSidebar');
openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));

const sessionForm = document.getElementById('sessionForm');
const chatContainer = document.getElementById('chatContainer');
let sessionInfo = {};
let sessionMessages = {};

const sessionUserInput = document.getElementById('sessionUserInput');
const sessionSendBtn = document.getElementById('sessionSendBtn');
const diagnosisBtn = document.getElementById('diagnosisBtn');
const sessionVoiceBtn = document.getElementById('sessionVoiceBtn');
const sessionStopBtn = document.getElementById('sessionStopBtn');
const sessionSaveBtn = document.getElementById('sessionSaveBtn');
const suggestionList = document.getElementById('suggestionList');
let currentAudio = null;

// Store all queries for diagnosis
let sessionQueries = [];

if (sessionForm) {
    sessionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        sessionInfo = {
            name: document.getElementById('personName').value,
            age: document.getElementById('personAge').value,
            gender: document.getElementById('personGender').value,
            date: new Date().toLocaleString()
        };
        sessionForm.style.display = 'none';
        document.getElementById('sessionInfoDisplay').textContent = `Session for ${sessionInfo.name} (${sessionInfo.gender}, ${sessionInfo.age}) - ${sessionInfo.date}`;
        // Enable input and buttons
        document.getElementById('sessionUserInput').disabled = false;
        document.getElementById('sessionSendBtn').disabled = false;
        document.getElementById('sessionVoiceBtn').disabled = false;
        document.getElementById('sessionStopBtn').disabled = false;
        document.getElementById('sessionSaveBtn').disabled = false;
        document.getElementById('diagnosisBtn').disabled = false;
        // Save session to localStorage
        saveSessionToStorage(sessionInfo);
        updateSessionHistory(sessionInfo.name, sessionInfo.date);
    });
// ...existing code...

// Save session history to localStorage
function saveSessionToStorage(info) {
    let sessions = JSON.parse(localStorage.getItem('sessionHistory') || '[]');
    sessions.push(info);
    localStorage.setItem('sessionHistory', JSON.stringify(sessions));
}

// Load session history from localStorage on page load
function loadSessionHistory() {
    let sessions = JSON.parse(localStorage.getItem('sessionHistory') || '[]');
    sessions.forEach(s => updateSessionHistory(s.name, s.date));
}
loadSessionHistory();

// Send chat message
sessionSendBtn.addEventListener('click', async () => {
    const text = sessionUserInput.value.trim();
    if (!text) return;
    addSessionMessage('user', text);
    sessionQueries.push(text);
    sessionUserInput.value = '';
    // Get AI response
    const response = await getAIResponse(text);
    addSessionMessage('ai', response.response);
});

// Diagnosis summary
diagnosisBtn.addEventListener('click', async () => {
    if (sessionQueries.length === 0) return;
    // Send all queries as a summary request
    const summaryPrompt = 'Patient symptoms: ' + sessionQueries.join(' | ') + '\nPlease provide a diagnosis summary and advice.';
    const response = await getAIResponse(summaryPrompt);
    addSessionMessage('diagnosis', response.response);
    // TODO: Save session info, queries, and diagnosis to backend/db
});

// Voice button logic
sessionVoiceBtn.addEventListener('click', async () => {
    const lastAiMessage = chatContainer.querySelector('.ai-message:last-child');
    if (!lastAiMessage || sessionVoiceBtn.disabled) return;
    sessionVoiceBtn.disabled = true;
    sessionVoiceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    sessionStopBtn.style.display = 'inline-block';
    try {
        const response = await fetch('/api/text-to-speech', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: lastAiMessage.textContent })
        });
        const data = await response.json();
        if (data.audio_data) {
            if (currentAudio) {
                currentAudio.pause();
                currentAudio = null;
            }
            currentAudio = new Audio(`data:audio/mp3;base64,${data.audio_data}`);
            currentAudio.onended = () => {
                sessionVoiceBtn.disabled = false;
                sessionVoiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                sessionStopBtn.style.display = 'none';
            };
            currentAudio.play();
        } else {
            sessionVoiceBtn.disabled = false;
            sessionVoiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
            sessionStopBtn.style.display = 'none';
        }
    } catch (error) {
        console.error('Error playing audio:', error);
        sessionVoiceBtn.disabled = false;
        sessionVoiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
        sessionStopBtn.style.display = 'none';
    }
});

sessionStopBtn.addEventListener('click', () => {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
    sessionVoiceBtn.disabled = false;
    sessionVoiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
    sessionStopBtn.style.display = 'none';
});

// Save session button (for future DB integration)
document.addEventListener('DOMContentLoaded', function() {
    // Save session button (for future DB integration)
    sessionSaveBtn.addEventListener('click', () => {
        // TODO: Save sessionInfo, sessionQueries, and diagnosis to backend/db
        alert('Session saved! (DB integration needed)');
    });

    // Session history in sidebar (demo)
    const menuList = document.querySelector('.menu-list');
    function updateSessionHistory(name, date) {
        const item = document.createElement('a');
        item.className = 'menu-link';
        item.textContent = `${name} (${date})`;
        item.href = '#';
        item.onclick = () => {
            // TODO: Load session history for this person
            alert(`Show history for ${name}`);
        };
        menuList.appendChild(item);
    }
    window.updateSessionHistory = updateSessionHistory;

    function addSessionMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        if (type === 'ai' || type === 'diagnosis') {
            messageDiv.innerHTML = content;
        } else {
            // ...existing code...
        }
    }
    window.addSessionMessage = addSessionMessage;
    // ...existing code...
});
// ...existing code...
    const response = await fetch('/api/health-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    if (!response.ok) throw new Error('Failed to get response');
    return response.json();
}
