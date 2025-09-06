import sqlite3
from flask import Flask, request, jsonify, Response, stream_with_context, send_from_directory
from flask_cors import CORS
import json
import psutil
from datetime import datetime
import os

# Project imports
from models.ai_engine import AIEngine
from models.knowledge_base import KnowledgeBase
from utils.text_utils import TextProcessor
from utils.voice_processing import VoiceProcessor

# --- Flask setup ---
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# --- Initialize components ---
knowledge_base = KnowledgeBase()
ai_engine = AIEngine()
text_processor = TextProcessor()
voice_processor = VoiceProcessor()

# --- SQLite DB Setup ---
def get_db():
    conn = sqlite3.connect('knowledge.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        date TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        sender TEXT,
        message TEXT,
        timestamp TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'user.html')

# Session APIs
@app.route('/api/session', methods=['POST'])
def create_session():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    date = data.get('date')
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO sessions (name, age, gender, date) VALUES (?, ?, ?, ?)', (name, age, gender, date))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'session_id': session_id})

@app.route('/api/session/<int:session_id>/message', methods=['POST'])
def add_message(session_id):
    data = request.json
    sender = data.get('sender')
    message = data.get('message')
    # Use current UTC timestamp
    timestamp = datetime.utcnow().isoformat()
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO messages (session_id, sender, message, timestamp) VALUES (?, ?, ?, ?)',
              (session_id, sender, message, timestamp))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/session/<int:session_id>/history', methods=['GET'])
def get_session_history(session_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE session_id=? ORDER BY timestamp', (session_id,))
    messages = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(messages)

# Emergency check
@app.route('/api/emergency-check', methods=['GET'])
def emergency_check():
    try:
        symptoms = request.args.get('symptoms', '')
        urgency_assessment = text_processor.assess_urgency(symptoms)
        is_urgent = urgency_assessment > 7
        return jsonify({
            'urgent': is_urgent,
            'urgency_level': urgency_assessment,
            'action': "SEEK IMMEDIATE MEDICAL ATTENTION" if is_urgent else "Monitor symptoms"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health topics
@app.route('/api/health-topics', methods=['GET'])
def health_topics():
    try:
        category = request.args.get('category', '')
        if category == 'symptoms':
            with open('data/modern_medicine.json', 'r') as f:
                medical_data = json.load(f)
                symptoms = []
                for condition in medical_data:
                    if 'common_symptoms' in condition:
                        symptoms.extend(condition['common_symptoms'])
                return jsonify(list(set(symptoms)))
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Voice interaction
@app.route('/api/voice-interaction', methods=['POST'])
def voice_interaction():
    try:
        audio_stream = request.get_data()
        text = voice_processor.speech_to_text(audio_stream)
        response = ai_engine.process_query(text, knowledge_base.get_relevant_knowledge(text))
        audio_response = voice_processor.text_to_speech(response['message'])
        return Response(stream_with_context(audio_response), mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cultural story
@app.route('/api/cultural-story', methods=['POST'])
def cultural_story():
    try:
        data = request.json
        scenario = data.get('scenario', '')
        story = knowledge_base.get_cultural_story(scenario)
        return jsonify(story)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Sickness names
@app.route('/api/sickness-names', methods=['GET'])
def sickness_names():
    try:
        with open('data/modern_medicine.json', 'r') as f:
            medical_data = json.load(f)
            names = [item['condition'] for item in medical_data if 'condition' in item]
        return jsonify(names)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# System status
@app.route('/api/system-status', methods=['GET'])
def system_status():
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return jsonify({
            'models_status': ai_engine.check_models_status(),
            'memory_usage': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent
            },
            'disk_usage': {
                'total': disk.total,
                'free': disk.free,
                'percent': disk.percent
            },
            'knowledge_base_status': knowledge_base.get_status(),
            'last_updated': knowledge_base.last_update_time
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update knowledge
@app.route('/api/update-knowledge', methods=['POST'])
def update_knowledge():
    try:
        files = request.files
        updated_files = []
        for file_key in files:
            file = files[file_key]
            if file.filename.endswith('.json'):
                success = knowledge_base.update_knowledge_file(file)
                if success:
                    updated_files.append(file.filename)
        return jsonify({
            'success': True,
            'updated_files': updated_files,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Usage stats
@app.route('/api/usage-stats', methods=['GET'])
def usage_stats():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        stats = knowledge_base.get_usage_stats(start_date, end_date)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Text to speech
@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        text = data.get('text', '')
        audio_data = voice_processor.text_to_speech(text)
        return jsonify({'audio_data': audio_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health query
@app.route('/api/health-query', methods=['POST'])
def health_query():
    try:
        data = request.json
        message = data.get('message', '')
        audio = data.get('audio')
        language = data.get('language', 'en')

        # If audio is provided, convert to text
        if audio:
            message = voice_processor.speech_to_text(audio)

        # Check for emergency keywords
        urgency_level = text_processor.assess_urgency(message)
        if urgency_level > 7:
            response = ai_engine.get_emergency_response(message)
        else:
            response = ai_engine.process_query(
                message,
                knowledge_base.get_relevant_knowledge(message)
            )

        # Generate audio if needed
        audio_response = None
        message_text = response.get('message', 'Sorry, there was an error processing your request.')
        if audio or data.get('require_audio'):
            voice_processor.set_language(language)
            audio_response = voice_processor.text_to_speech(message_text)

        return jsonify({
            'response': message_text,
            'audio': audio_response,
            'urgency': urgency_level,
            'status': response.get('status', 'success')
        })

    except Exception as e:
        import traceback
        print('Error in /api/health-query:', str(e))
        traceback.print_exc()
        return jsonify({'error': str(e), 'status': 'error'}), 500

# Serve data files
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

# --- Run ---
if __name__ == '__main__':
    knowledge_base.init_db()
    app.run(debug=True, port=5000)
