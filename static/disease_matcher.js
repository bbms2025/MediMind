// Disease Matcher module for smart autocomplete
let diseaseData = {
    names: [],
    symptoms: {},
    commonPhrases: ['i have', 'suffering from', 'experiencing', 'feeling']
};

// Load disease data from JSON files
async function loadDiseaseData() {
    try {
        const [modern, traditional, cultural] = await Promise.all([
            fetch('data/modern_medicine.json').then(r => r.json()),
            fetch('data/traditional_medicine.json').then(r => r.json()),
            fetch('data/cultural_bridge.json').then(r => r.json())
        ]);
        
        // Combine all disease names and symptoms
        const allDiseases = [...modern, ...traditional, ...cultural];
        diseaseData.names = [...new Set(allDiseases.map(d => d.condition))];
        
        // Create symptoms mapping
        allDiseases.forEach(disease => {
            if (disease.common_symptoms) {
                diseaseData.symptoms[disease.condition] = disease.common_symptoms;
            }
        });
        
        console.log('Disease data loaded successfully');
        return true;
    } catch (error) {
        console.error('Error loading disease data:', error);
        return false;
    }
}

// Initialize the disease matcher
async function initDiseaseMatcher() {
    const loaded = await loadDiseaseData();
    if (!loaded) {
        console.error('Failed to initialize disease matcher');
        return;
    }

    const userInput = document.getElementById('userInput');
    const suggestionList = document.getElementById('suggestionList');

    if (!userInput || !suggestionList) {
        console.error('Required DOM elements not found');
        return;
    }

    let selectedIndex = -1;
    
    userInput.addEventListener('input', handleInput);
    userInput.addEventListener('keydown', (e) => {
        const items = suggestionList.querySelectorAll('.suggestion-item');
        if (items.length === 0) return;

        // Remove previous selection
        items.forEach(item => item.classList.remove('selected'));

        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = (selectedIndex + 1) % items.length;
                items[selectedIndex].classList.add('selected');
                items[selectedIndex].scrollIntoView({ block: 'nearest' });
                break;
            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = selectedIndex <= 0 ? items.length - 1 : selectedIndex - 1;
                items[selectedIndex].classList.add('selected');
                items[selectedIndex].scrollIntoView({ block: 'nearest' });
                break;
            case 'Enter':
                if (selectedIndex >= 0 && selectedIndex < items.length) {
                    e.preventDefault();
                    items[selectedIndex].click();
                }
                break;
            case 'Escape':
                suggestionList.style.display = 'none';
                selectedIndex = -1;
                break;
        }
    });

    document.addEventListener('click', (e) => {
        if (!suggestionList.contains(e.target) && e.target !== userInput) {
            suggestionList.style.display = 'none';
            selectedIndex = -1;
        }
    });
}

// Handle input changes
function handleInput(event) {
    const input = event.target.value;
    const lastWord = input.split(' ').pop().toLowerCase();
    const suggestionList = document.getElementById('suggestionList');
    suggestionList.innerHTML = '';
    
    // Don't show suggestions for empty input or short words
    if (!input || lastWord.length < 2) {
        suggestionList.style.display = 'none';
        return;
    }
    
    // Find matches in disease names and symptoms
    const matches = [];
    
    // Check if input starts with common phrases
    const isDescribingSymptoms = diseaseData.commonPhrases.some(phrase => 
        input.toLowerCase().includes(phrase)
    );
    
    if (isDescribingSymptoms) {
        // Look for diseases that match symptoms
        Object.entries(diseaseData.symptoms).forEach(([disease, symptoms]) => {
            if (symptoms.some(s => s.toLowerCase().includes(lastWord))) {
                matches.push({
                    text: disease,
                    type: 'disease',
                    symptom: symptoms.find(s => s.toLowerCase().includes(lastWord))
                });
            }
        });
    }
    
    // Also check direct disease name matches
    diseaseData.names.forEach(name => {
        if (name.toLowerCase().includes(lastWord)) {
            matches.push({
                text: name,
                type: 'disease'
            });
        }
    });
    
    // Show matches
    if (matches.length > 0) {
        matches.slice(0, 5).forEach(match => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.innerHTML = `
                <strong>${match.text}</strong>
                ${match.symptom ? `<br><small>Symptom match: ${match.symptom}</small>` : ''}
            `;
            item.onclick = () => {
                event.target.value = match.text;
                suggestionList.innerHTML = '';
                suggestionList.style.display = 'none';
                event.target.focus();
            };
            suggestionList.appendChild(item);
        });
        suggestionList.style.display = 'block';
    } else {
        suggestionList.style.display = 'none';
    }
}

// Initialize when the DOM is ready
document.addEventListener('DOMContentLoaded', initDiseaseMatcher);
