# AI Medical Assistant

A sophisticated medical assistant application that bridges traditional and modern medicine approaches, providing users with comprehensive health insights and recommendations.

## Features

### Core Functionality
- **Dual Medicine Approach**: Integrates both traditional and modern medical knowledge
- **Interactive Chat Interface**: Real-time conversation with AI for medical inquiries
- **Voice Input Support**: Speech-to-text capability for easier interaction
- **Smart Search**: Search through past conversations and medical information
- **Session Management**: Maintains chat history and user sessions
- **Responsive UI**: Mobile-friendly interface with sidebar navigation

### Knowledge Management
- **Knowledge Base Integration**: 
  - Traditional Medicine Database
  - Modern Medicine Database
  - Cultural Bridge Information
- **Smart Filtering**: Toggle between traditional, modern, or combined medical advice
- **Real-time Search**: Search through past conversations and medical knowledge

### User Interface
- **Modal System**: Information displays in clean, modal windows
- **Sidebar Navigation**: Easy access to chat history and filters
- **Responsive Design**: Works on desktop and mobile devices
- **Chat History**: Chronological display of past conversations
- **Timestamp Display**: Relative time formatting for better readability

### Technical Features
- **Real-time Processing**: Async handling of user inputs
- **Error Handling**: Robust error management system
- **Voice Recognition**: Browser-based speech recognition
- **Session Management**: Server-side session handling
- **Database Integration**: SQLite database for knowledge storage

## Project Structure
```
ai_medical_assistant/
├── admin.py                 # Admin interface handler
├── clean_db.py             # Database maintenance script
├── knowledge.db            # SQLite database
├── main.py                 # Main application file
├── main_new.py            # Updated main application logic
├── requirements.txt        # Python dependencies
├── user.py                # User management
├── data/
│   ├── cultural_bridge.json    # Cultural context data
│   ├── modern_medicine.json    # Modern medical knowledge
│   └── traditional_medicine.json# Traditional medical knowledge
├── models/
│   ├── __init__.py
│   ├── ai_engine.py           # AI processing core
│   ├── knowledge_base.py      # Knowledge management
│   ├── prompt_builder.py      # AI prompt construction
│   └── symptom_analyzer.py    # Symptom analysis logic
├── static/
│   ├── app.js               # Main JavaScript
│   ├── disease_matcher.css  # Disease matcher styling
│   ├── disease_matcher.js   # Disease matching logic
│   ├── style.css          # Main styling
│   ├── user.html         # User interface
│   └── welcome.js        # Welcome page logic
└── utils/
    ├── __init__.py
    ├── text_utils.py      # Text processing utilities
    └── voice_processing.py# Voice processing functions
```

## Setup Instructions

1. **Environment Setup**
   ```bash
   python -m venv .env
   .env\Scripts\activate  # Windows
   source .env/bin/activate  # Linux/Mac
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   python clean_db.py  # Initialize/reset database
   ```

4. **Model Setup**
   
   The application can use either Hugging Face API (default) or local models.

   ### Using Local Models
   
   1. Install additional requirements:
      ```bash
      pip install torch transformers accelerate
      ```

   2. Download models:
      ```bash
      # Create models directory
      mkdir models/weights
      
      # Download storyteller model (larger model for cultural context)
      python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('YOUR_CHOSEN_MODEL', trust_remote_code=True).save_pretrained('models/weights/storyteller'); AutoTokenizer.from_pretrained('YOUR_CHOSEN_MODEL').save_pretrained('models/weights/storyteller')"
      
      # Download emergency model (smaller, faster model)
      python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('YOUR_CHOSEN_MODEL', trust_remote_code=True).save_pretrained('models/weights/emergency'); AutoTokenizer.from_pretrained('YOUR_CHOSEN_MODEL').save_pretrained('models/weights/emergency')"
      ```

   3. Update `models/ai_engine.py`:
      - Set `USE_LOCAL_MODELS = True`
      - Update model paths if needed in `LOCAL_MODEL_PATHS`

   ### Hardware Requirements for Local Models
   - Minimum 16GB RAM
   - GPU with 8GB+ VRAM recommended
   - SSD storage for faster model loading

5. **Running the Application**
   ```bash
   python main.py
   ```

## Configuration

- Configure database settings in knowledge_base.py
- Adjust AI parameters in ai_engine.py
- Modify UI settings in static/style.css

### Model Configuration

The application supports both API-based and local model configurations:

#### API Configuration (Default)
```python
# In models/ai_engine.py
USE_LOCAL_MODELS = False
HF_TOKEN = "your_hugging_face_token"
```

#### Local Model Configuration
```python
# In models/ai_engine.py
USE_LOCAL_MODELS = True

LOCAL_MODEL_PATHS = {
    'storyteller': 'models/weights/storyteller',
    'emergency': 'models/weights/emergency'
}

MODEL_SETTINGS = {
    'max_length': 500,
    'temperature': 0.7,
    'top_p': 0.9,
    'device_map': 'auto',  # Uses available GPUs or falls back to CPU
    'torch_dtype': 'float16'  # Use half precision to save memory
}
```

## Usage

1. **Starting a Session**
   - Open the application in a web browser
   - Log in or continue as a guest
   - Start chatting with the AI assistant

2. **Using Voice Input**
   - Click the microphone button
   - Speak your query
   - Wait for AI response

3. **Searching Past Conversations**
   - Use the search bar in the sidebar
   - Filter by traditional/modern medicine
   - View chronological history

4. **Admin Functions**
   - Access admin panel through /admin
   - Manage knowledge base
   - View usage statistics

## Security

- Session-based authentication
- Secure database operations
- Input validation and sanitization
- Error logging and monitoring

## Browser Support

- Chrome (recommended for voice features)
- Firefox
- Safari
- Edge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Python and JavaScript
- Uses SQLite for data storage
- Implements modern web standards
- Voice recognition via Web Speech API
