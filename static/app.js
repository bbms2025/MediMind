// DOM Elements
const sidebar = document.getElementById('sidebar');
const openSidebarBtn = document.getElementById('openSidebar');
const closeSidebarBtn = document.getElementById('closeSidebar');
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const helpBtn = document.getElementById('helpBtn');
const voiceBtn = document.getElementById('voiceBtn');
const stopBtn = document.getElementById('stopBtn');
const saveBtn = document.getElementById('saveBtn');
const suggestionList = document.getElementById('suggestionList');
const historyList = document.getElementById('historyList');
const normalChatHistorySidebar = document.getElementById('normalChatHistorySidebar');
const diagnosisBtn = document.getElementById('diagnosisBtn');
const diagnosisModal = document.getElementById('diagnosisModal');
const diagnosisModalText = document.getElementById('diagnosisModalText');
const closeDiagnosisModal = document.getElementById('closeDiagnosisModal');
const chatModal = document.getElementById('chatModal');
const closeModalBtn = document.getElementById('closeModal');

// Function to format date as relative time
function formatRelativeTime(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    
    // Handle invalid dates
    if (isNaN(date.getTime())) {
        return 'Just now';
    }
    
    // Convert both dates to timestamps in milliseconds
    const timestamp = date.getTime();
    const currentTime = now.getTime();
    
    // Calculate time differences with more precision
    const diffInMilliseconds = currentTime - timestamp;
    const diffInSeconds = Math.round(diffInMilliseconds / 1000);
    const diffInMinutes = Math.round(diffInSeconds / 60);
    const diffInHours = Math.round(diffInMinutes / 60);
    const diffInDays = Math.round(diffInHours / 24);
    const diffInWeeks = Math.round(diffInDays / 7);
    const diffInMonths = Math.round(diffInDays / 30.44); // More accurate month calculation
    const diffInYears = Math.round(diffInDays / 365.25); // Account for leap years
    
    // Future dates
    if (diffInSeconds < 0) {
        return 'Just now';
    }
    
    // Less than 30 seconds
    if (diffInSeconds < 30) {
        return 'Just now';
    }
    
    // Less than 1 minute
    if (diffInSeconds < 60) {
        return `${diffInSeconds} secs ago`;
    }
    
    // Less than 1 hour
    if (diffInMinutes < 60) {
        return diffInMinutes === 1 ? '1 min ago' : `${diffInMinutes} mins ago`;
    }
    
    // Less than 1 day
    if (diffInHours < 24) {
        return diffInHours === 1 ? '1 hour ago' : `${diffInHours} hours ago`;
    }
    
    // Less than 1 week
    if (diffInDays < 7) {
        return diffInDays === 1 ? 'Yesterday' : `${diffInDays} days ago`;
    }
    
    // Less than 1 month
    if (diffInWeeks < 4) {
        return diffInWeeks === 1 ? '1 week ago' : `${diffInWeeks} weeks ago`;
    }
    
    // Less than 1 year
    if (diffInMonths < 12) {
        return diffInMonths === 1 ? '1 month ago' : `${diffInMonths} months ago`;
    }
    
    // 1 year or more
    return diffInYears === 1 ? '1 year ago' : `${diffInYears} years ago`;
}

// Updated renderSidebar function with properly formatted dates
function renderSidebar(filteredPairs) {
    normalChatHistorySidebar.innerHTML = '';
    filteredPairs.forEach(pair => {
        const item = document.createElement('div');
        item.className = 'history-item';
        
        // Format the timestamp properly
        const date = new Date(pair.timestamp);
        const formattedDate = date.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        });
        
        // Create structured HTML with formatted date
        item.innerHTML = `
            <div class="history-title">${pair.question}</div>
            <div class="history-date" title="Created: ${formattedDate}">${formattedDate}</div>
        `;
        
        item.style.cursor = 'pointer';
        item.onclick = () => {
            // Modal content with full date for reference
            document.getElementById('modalChatText').innerHTML = `
                <strong>Q:</strong> ${pair.question}<br>
                <strong>A:</strong> ${pair.answer}<br>
                <span style='font-size:12px;color:#888;'>(${formattedDate})</span>
            `;
            
            // Diagnosis summary (stub: extract first sentence from answer)
            document.getElementById('modalDiagnosisSummary').innerHTML = `
                <strong>Diagnosis Summary:</strong> ${pair.answer.split('.')[0]}.
            `;
            
            // Follow-up suggestions (stub: suggest based on keywords)
            let followups = [];
            if (pair.question.toLowerCase().includes('headache')) followups.push('Do you also have nausea or vision changes?');
            if (pair.question.toLowerCase().includes('skin')) followups.push('Is there any fever or spreading redness?');
            if (pair.question.toLowerCase().includes('flu') || pair.question.toLowerCase().includes('influenza')) followups.push('Are you experiencing body aches or high fever?');
            if (pair.question.toLowerCase().includes('cough')) followups.push('Is the cough dry or producing phlegm?');
            if (followups.length === 0) followups.push('Would you like more details or advice?');
            
            document.getElementById('modalFollowupSuggestions').innerHTML = `
                <strong>Follow-up Suggestions:</strong> 
                <ul>${followups.map(f=>`<li>${f}</li>`).join('')}</ul>
            `;
            
            // Personalized recommendations (stub: extract advice from answer)
            let rec = pair.answer.match(/advice:(.*)/i);
            document.getElementById('modalRecommendations').innerHTML = `
                <strong>Recommendations:</strong> ${rec ? rec[1] : 'Maintain a healthy lifestyle and follow medical advice.'}
            `;
            
            // Urgency detection (stub: if answer contains "urgent" or "immediate")
            let urgent = /urgent|immediate|emergency|serious|severe|critical/i.test(pair.answer);
            document.getElementById('modalUrgencyWarning').style.display = urgent ? 'block' : 'none';
            document.getElementById('modalUrgencyWarning').innerHTML = urgent ? 
                'Warning: Immediate medical attention may be required!' : '';
            
            // // Tagging (stub: show input for tags)
            // document.getElementById('modalTagging').innerHTML = `
            //     <strong>Tags:</strong> 
            //     <input type='text' style='padding: 8px; margin: 0 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;' class='text-input' id='tagInput' placeholder='e.g. headache, skin, flu'> 
            //     <button style='padding: 6px 12px; font-size: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;' id='saveTagBtn' class='btn-primary' style='padding: 6px 12px; font-size: 12px;'>Save</button>
            // `;
            
            // document.getElementById('saveTagBtn').onclick = function() { 
            //     const tagValue = document.getElementById('tagInput').value;
            //     if (tagValue.trim()) {
            //         alert('Tag saved: ' + tagValue);
            //         // Here you could save to localStorage or send to server
            //     } else {
            //         alert('Please enter a tag');
            //     }
            // };
            
            // Rating (stub: 5 stars)
            document.getElementById('modalRating').innerHTML = `
                <strong>Rate this answer:</strong> 
                <span id='starRating'>${Array(5).fill('<span style="font-size:20px;cursor:pointer;color:#ddd;">&#9734;</span>').join('')}</span>
            `;
            
            Array.from(document.getElementById('starRating').children).forEach((star, idx) => {
                star.onclick = function() {
                    Array.from(document.getElementById('starRating').children).forEach((s, i) => {
                        s.innerHTML = i <= idx ? '&#9733;' : '&#9734;';
                        s.style.color = i <= idx ? '#ffd700' : '#ddd';
                    });
                    alert('Rated ' + (idx+1) + ' stars!');
                    // Here you could save the rating to localStorage or send to server
                };
            });
            
            // Voice output (stub: use browser TTS)
            document.getElementById('modalVoiceOutput').innerHTML = `
                <button style='padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px;' id='playAnswerVoice' class='btn-icon' title='Listen to answer'>
                    <i class='fas fa-volume-up'></i> Listen
                </button>
            `;
            
            document.getElementById('playAnswerVoice').onclick = function() {
                // Stop any ongoing speech
                window.speechSynthesis.cancel();
                
                let utter = new SpeechSynthesisUtterance(pair.answer);
                utter.rate = 0.8;
                utter.pitch = 1;
                utter.volume = 0.8;
                
                window.speechSynthesis.speak(utter);
            };
            
            document.getElementById('chatModal').style.display = 'flex';
        };
        
        normalChatHistorySidebar.appendChild(item);
    });
}

// Optional: Function to refresh relative times periodically
function refreshRelativeTimes() {
    const historyItems = document.querySelectorAll('.history-item .history-date');
    historyItems.forEach(dateElement => {
        const fullDate = dateElement.getAttribute('title');
        if (fullDate) {
            dateElement.textContent = (new Date(fullDate));
        }
    });
}

// Optional: Update relative times every minute
// setInterval(refreshRelativeTimes, 60000);

// Initialize search functionality
function initializeSearch(pairs) {
    const sidebarSearchBox = document.getElementById('sidebarSearchBox');
    if (!sidebarSearchBox) return;

    sidebarSearchBox.oninput = function() {
        try {
            const val = this.value.toLowerCase();
            if (!pairs || !Array.isArray(pairs)) {
                console.warn('No valid chat history to search');
                return;
            }
            
            const filtered = pairs.filter(pair => {
                if (!pair || typeof pair !== 'object') return false;
                
                const questionMatch = pair.question ? pair.question.toLowerCase().includes(val) : false;
                const answerMatch = pair.answer ? pair.answer.toLowerCase().includes(val) : false;
                const dateMatch = pair.timestamp ? new Date(pair.timestamp).toLocaleString().toLowerCase().includes(val) : false;
                
                return questionMatch || answerMatch || dateMatch;
            });
            
            renderSidebar(filtered);
        } catch (error) {
            console.error('Error in search:', error);
        }
    };
}

// Handle search input changes
function handleSearch(searchText) {
    if (!window.normalChatPairs || !Array.isArray(window.normalChatPairs)) {
        console.warn('No chat history available');
        return;
    }

    searchText = searchText.toLowerCase().trim();
    const filtered = window.normalChatPairs.filter(pair => {
        if (!pair || typeof pair !== 'object') return false;
        
        const questionMatch = pair.question && pair.question.toLowerCase().includes(searchText);
        const answerMatch = pair.answer && pair.answer.toLowerCase().includes(searchText);
        const dateMatch = pair.timestamp && new Date(pair.timestamp).toLocaleString().toLowerCase().includes(searchText);
        
        return questionMatch || answerMatch || dateMatch;
    });

    renderSidebar(filtered);
}

// Function to handle search input
function handleSearch(query) {
    if (!window.normalChatPairs || !Array.isArray(window.normalChatPairs)) {
        console.warn('No chat history available');
        return;
    }

    const searchText = query.toLowerCase().trim();
    
    const filtered = window.normalChatPairs.filter(pair => {
        // Check if pair exists and is an object
        if (!pair || typeof pair !== 'object') {
            return false;
        }
        
        // Safely check each property with null/undefined checks
        const questionMatch = pair.question ? pair.question.toLowerCase().includes(searchText) : false;
        const answerMatch = pair.answer ? pair.answer.toLowerCase().includes(searchText) : false;
        
        // For timestamp, convert to string first, then check
        const dateMatch = pair.timestamp ? 
            new Date(pair.timestamp).toLocaleString().toLowerCase().includes(searchText) : false;
        
        return questionMatch || answerMatch || dateMatch;
    });

    renderSidebar(filtered);
}

// Load normal chat history from DB and show in sidebar
async function loadNormalChatHistory() {
    try {
        const response = await fetch('/api/session/1/history');
        const messages = await response.json();
        
        // Group by conversation (user+ai pairs), sort by latest
        let pairs = [];
        for (let i = 0; i < messages.length - 1; i++) {
            if (messages[i].sender === 'user' && messages[i+1].sender === 'ai') {
                pairs.push({
                    question: messages[i].message,
                    answer: messages[i+1].message,
                    timestamp: messages[i+1].timestamp // use AI answer timestamp
                });
            }
        }
        
        // Sort by latest
        pairs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        window.normalChatPairs = pairs;
        renderSidebar(pairs);
        
        // Set up search functionality
        const searchBox = document.getElementById('sidebarSearchBox');
        if (searchBox) {
            searchBox.value = ''; // Clear any existing search
            searchBox.addEventListener('input', (e) => handleSearch(e.target.value));
        }
        
        // Knowledge source toggle logic
        const toggleTraditional = document.getElementById('toggleTraditional');
        const toggleModern = document.getElementById('toggleModern');
        const toggleBoth = document.getElementById('toggleBoth');
        
        if (toggleTraditional) {
            toggleTraditional.onclick = function() {
                console.log('Traditional button clicked');
                renderSidebar(window.normalChatPairs.filter(p => /traditional medicine/i.test(p.answer)));
            };
        }
        
        if (toggleModern) {
            toggleModern.onclick = function() {
                console.log('Modern button clicked');
                renderSidebar(window.normalChatPairs.filter(p => /modern medicine/i.test(p.answer)));
            };
        }
        
        if (toggleBoth) {
            toggleBoth.onclick = function() {
                console.log('Both button clicked');
                renderSidebar(window.normalChatPairs);
            };
        }
        
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Modal close functionality
if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
        chatModal.style.display = 'none';
    });
}

// Close modal when clicking outside
if (chatModal) {
    chatModal.addEventListener('click', (e) => {
        if (e.target === chatModal) {
            chatModal.style.display = 'none';
        }
    });
}

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (chatModal && chatModal.style.display === 'flex') {
            chatModal.style.display = 'none';
        }
        if (diagnosisModal && diagnosisModal.style.display === 'flex') {
            diagnosisModal.style.display = 'none';
        }
    }
});

// Only load when on normal chat page
// Always load chat history in sidebar on page load
document.addEventListener('DOMContentLoaded', function() {
    loadNormalChatHistory();
});

// State
let chatHistory = [];
let isProcessing = false;
let sicknessNames = [];
let currentAudio = null;

// Event Listeners
openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));

// Load sickness names from backend
async function loadSicknessNames() {
    try {
        const response = await fetch('/api/sickness-names');
        const data = await response.json();
        sicknessNames = Array.isArray(data) ? data : [];
    } catch (error) {
        console.error('Error loading sickness names:', error);
    }
}
loadSicknessNames();

// Auto-suggestion for sickness names
userInput.addEventListener('input', function() {
    const value = userInput.value.toLowerCase();
    suggestionList.innerHTML = '';
    if (value.length === 0) return;
    const matches = sicknessNames.filter(name => name.toLowerCase().includes(value));
    if (matches.length > 0) {
        matches.slice(0, 5).forEach(name => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = name;
            item.onclick = () => {
                userInput.value = name;
                suggestionList.innerHTML = '';
                userInput.focus();
            };
            suggestionList.appendChild(item);
        });
    }
});

// Handle Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        helpBtn.click();
    }
});

// Handle help button click
helpBtn.addEventListener('click', async () => {
    if (isProcessing || !userInput.value.trim()) return;
    try {
        isProcessing = true;
        helpBtn.disabled = true;
        const input = userInput.value;
        addMessageToChat('user', input);
        const response = await getAIResponse(input);
        addMessageToChat('ai', response.response, response.status, input);
        saveToHistory(input, response.response);
        userInput.value = '';
    } catch (error) {
        console.error('Error:', error);
    } finally {
        isProcessing = false;
        helpBtn.disabled = false;
    }
});

// Text to Speech
voiceBtn.addEventListener('click', async () => {
    const lastAiMessage = chatContainer.querySelector('.ai-message:last-child');
    if (!lastAiMessage || voiceBtn.disabled) return;
    voiceBtn.disabled = true;
    voiceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    stopBtn.style.display = 'inline-block';
    try {
        const response = await fetch('/api/text-to-speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
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
                voiceBtn.disabled = false;
                voiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                stopBtn.style.display = 'none';
            };
            currentAudio.play();
        } else {
            voiceBtn.disabled = false;
            voiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
            stopBtn.style.display = 'none';
        }
    } catch (error) {
        console.error('Error playing audio:', error);
        voiceBtn.disabled = false;
        voiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
        stopBtn.style.display = 'none';
    }
});

stopBtn.addEventListener('click', () => {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
    voiceBtn.disabled = false;
    voiceBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
    stopBtn.style.display = 'none';
});

// Diagnosis button logic
if (diagnosisBtn) {
    diagnosisBtn.onclick = async function() {
        // Gather all user inputs from chatHistory
        const userInputs = chatHistory.filter(m => m.type === 'user').map(m => m.content);
        if (userInputs.length === 0) {
            diagnosisModalText.innerHTML = '<strong>Start a chat and get the diagnosis.</strong>';
            diagnosisModal.style.display = 'flex';
            return;
        }
        diagnosisModalText.innerHTML = '<strong>Generating diagnosis summary...</strong>';
        diagnosisModal.style.display = 'flex';
        try {
            // Combined summary prompt (concise, predictive, max 800 words)
            const summaryPrompt = `Based on these symptoms: ${userInputs.join(', ')}.\nSummarize the most likely conditions and give overall advice in clear, simple language.\nInclude possible causes and predictions for why these symptoms may occur together.\nInclude traditional medicine insights if relevant.\nLimit the summary to 800 words or less.\nEnd with a clear disclaimer that this summary is AI-generated and not a substitute for professional medical advice. Encourage consulting a doctor if symptoms worsen or cause concern.`;
            const summaryRes = await fetch('/api/health-query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: summaryPrompt, model: 'summary' })
            });
            const summaryData = await summaryRes.json();
            // Only show the concise summary in the modal
            const summaryText = summaryData.response || '<em>No summary available. Please try again.</em>';
            let tokenInfo = '';
            if (summaryData.prompt_tokens || summaryData.completion_tokens || summaryData.total_tokens) {
                tokenInfo = `<div style='font-size:12px;color:#888;margin-top:8px;'>Token usage: prompt ${summaryData.prompt_tokens || 0}, completion ${summaryData.completion_tokens || 0}, total ${summaryData.total_tokens || 0}</div>`;
            }
            diagnosisModalText.innerHTML = `<div style='margin-top:16px;'><span style='font-size:1.2em;'>🩺 <strong>Diagnosis Summary (AI-Generated)</strong></span><br>${summaryText}${tokenInfo}</div>`;
            // Add rating stars
            document.getElementById('diagnosisModalRating').innerHTML = `<strong>Rate this diagnosis:</strong> <span id='diagnosisStarRating'>${Array(5).fill('<span style=\"font-size:20px;cursor:pointer;\">&#9734;</span>').join(' ')}</span>`;
            Array.from(document.getElementById('diagnosisStarRating').children).forEach((star, idx) => {
                star.onclick = function() {
                    Array.from(document.getElementById('diagnosisStarRating').children).forEach((s, i) => {
                        s.innerHTML = i <= idx ? '&#9733;' : '&#9734;';
                    });
                    alert('Rated diagnosis ' + (idx+1) + ' stars!');
                };
            });
            // Add voice output button
            document.getElementById('diagnosisModalVoiceOutput').innerHTML = `<button id='playDiagnosisVoice' class='btn-icon'><i class='fas fa-volume-up'></i> Listen</button>`;
            document.getElementById('playDiagnosisVoice').onclick = function() {
                let utter = new SpeechSynthesisUtterance(summaryText);
                window.speechSynthesis.speak(utter);
            };
        } catch (err) {
            diagnosisModalText.innerHTML = '<strong>Error generating diagnosis. Please try again.</strong>';
        }
    };
}
if (closeDiagnosisModal) closeDiagnosisModal.onclick = function() {
    diagnosisModal.style.display = 'none';
};
diagnosisModal.onclick = function(e) {
    if (e.target === diagnosisModal) diagnosisModal.style.display = 'none';
};

// Language/translation button logic (stub: show modal with language options)
const languageBtn = document.getElementById('languageBtn');
if (languageBtn) {
    languageBtn.onclick = function() {
        alert('Language/translation feature coming soon!');
        // You can add a modal here for language selection and translation
    };
}

// Load cultural_bridge.json for Cultural Wisdom section
let culturalBridgeData = {};
fetch('/data/cultural_bridge.json')
    .then(res => res.json())
    .then(data => {
        data.forEach(item => {
            if (item.condition) {
                culturalBridgeData[item.condition.toLowerCase()] = item;
            }
        });
        console.log('[CulturalBridge] Loaded conditions:', Object.keys(culturalBridgeData));
    });

// Add Cultural Wisdom section to chat after each AI answer
function addMessageToChat(type, content, status, userInput) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    if (type === 'ai') {
        if (status && status !== 'success') {
            messageDiv.textContent = content;
        } else {
            messageDiv.innerHTML = content;
            // Fuzzy/partial match for Cultural Wisdom
            if (userInput && culturalBridgeData) {
                const inputLower = userInput.toLowerCase();
                let matchedKey = null;
                for (const key in culturalBridgeData) {
                    if (inputLower.includes(key) || key.includes(inputLower)) {
                        matchedKey = key;
                        break;
                    }
                }
                console.log('[CulturalBridge] User input:', userInput, '| Matched key:', matchedKey);
                if (matchedKey) {
                    const wisdom = culturalBridgeData[matchedKey];
                    messageDiv.innerHTML += `
                        <div class='cultural-wisdom' style='margin-top:12px;padding:12px;background:#f9f6e7;border-radius:8px;'>
                            <span style='font-size:1.2em;color:#8e44ad;'>🌏 Cultural Wisdom</span><br>
                            <span style='color:#2980b9;'><strong>Analogy:</strong> ${wisdom.everyday_analogy || ''}</span><br>
                            <span style='color:#16a085;'><strong>Reassurance:</strong> ${wisdom.reassurance_note || ''}</span><br>
                            <span style='color:#e67e22;'><strong>Self-care:</strong> ${wisdom.self_care_basics ? wisdom.self_care_basics.join(', ') : ''}</span><br>
                            <span style='color:#d35400;'><strong>Prevention:</strong> ${wisdom.prevention_tips ? wisdom.prevention_tips.join(', ') : ''}</span>
                        </div>
                    `;
                    console.log('[CulturalBridge] Wisdom section rendered for:', matchedKey);
                } else {
                    console.log('[CulturalBridge] No match found for user input:', userInput);
                }
            }
        }
    } else {
        messageDiv.textContent = content;
    }
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    chatHistory.push({ type, content });
}

// Utility functions
async function getAIResponse(message) {
    const response = await fetch('/api/health-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    const data = await response.json();
    // Show token usage in chat div if available
    if (data.prompt_tokens || data.completion_tokens || data.total_tokens) {
        const tokenDiv = document.createElement('div');
        tokenDiv.className = 'token-usage';
        tokenDiv.style.fontSize = '12px';
        tokenDiv.style.color = '#888';
        tokenDiv.textContent = `Token usage: prompt ${data.prompt_tokens || 0}, completion ${data.completion_tokens || 0}, total ${data.total_tokens || 0}`;
        chatContainer.appendChild(tokenDiv);
    }
    return data;
}

// ...existing code...

function saveToHistory(question, answer) {
    // Get current timestamp in local time
    const now = new Date();
    const localTime = now.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
    
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    
    // Create structured HTML with formatted timestamp
    historyItem.innerHTML = `
        <div class="history-title">${question}</div>
        <div class="history-date" title="Created: ${localTime}">${localTime}</div>
    `;
    
    // Update timestamps periodically
    setInterval(() => {
        const dateDiv = historyItem.querySelector('.history-date');
        if (dateDiv) {
            const itemTimestamp = dateDiv.getAttribute('data-timestamp');
            dateDiv.textContent = (itemTimestamp);
        }
    }, 60000); // Update every minute
    
    historyItem.onclick = () => {
        showChatModal(question, answer, timestamp);
    };

    // Add to normalChatHistorySidebar instead of historyList
    if (normalChatHistorySidebar) {
        normalChatHistorySidebar.insertBefore(historyItem, normalChatHistorySidebar.firstChild);
    }

    // Save chat to DB (session_id=1 for normal chat) with local timestamp
    const currentTime = new Date();
    const localTimestamp = currentTime.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
    
    // Save user message
    fetch('/api/session/1/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            sender: 'user', 
            message: question,
            timestamp: localTimestamp
        })
    });
    
    // Save AI response
    fetch('/api/session/1/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            sender: 'ai', 
            message: answer,
            timestamp: localTimestamp
        })
    });
}

// Voice input (stub: browser speech recognition)
const micBtn = document.getElementById('micBtn');
if (micBtn) {
    micBtn.onclick = function() {
        if (!('webkitSpeechRecognition' in window)) {
            alert('Speech recognition not supported in this browser.');
            return;
        }
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.onresult = function(event) {
            userInput.value = event.results[0][0].transcript;
        };
        recognition.start();
    };
}
