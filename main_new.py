from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from models.ai_engine_new import AIEngine
from models.symptom_analyzer import SymptomAnalyzer
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# Initialize components
ai_engine = AIEngine()
symptom_analyzer = SymptomAnalyzer()

@app.route('/')
def index():
    return app.send_static_file('user.html')

@app.route('/api/health-query', methods=['POST'])
def health_query():
    try:
        data = request.json
        user_input = data.get('message', '')
        
        # Get enhanced response using new AI engine
        response = ai_engine.get_enhanced_response(user_input)
        
        # Format the response for the frontend
        formatted_response = {
            "status": "success",
            "response": _format_response_for_frontend(response),
            "matched_conditions": response['matched_conditions'],
            "urgency_level": response['urgency_level'],
            "cultural_wisdom": response['cultural_wisdom']
        }
        
        return jsonify(formatted_response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "response": f"Error processing request: {str(e)}"
        })

def _format_response_for_frontend(response: dict) -> str:
    """Format the enhanced response for frontend display"""
    parts = []
    
    # Add AI Analysis
    parts.append(response['ai_analysis'])
    
    # Add Modern Medicine Advice
    if response['modern_advice']:
        parts.append("\n🏥 Modern Medicine Perspective:")
        for advice in response['modern_advice']:
            parts.append(f"\nFor {advice['condition']}:")
            parts.append(f"• {advice['explanation']}")
            if advice['care']:
                parts.append("• Self-care tips:")
                parts.extend(f"  - {tip}" for tip in advice['care'])
    
    # Add Traditional Medicine Advice
    if response['traditional_advice']:
        parts.append("\n🌿 Traditional Medicine Perspective:")
        for advice in response['traditional_advice']:
            parts.append(f"\nFor {advice['condition']}:")
            parts.append(f"• {advice['remedy']}")
            parts.append(f"• {advice['explanation']}")
    
    # Add Cultural Wisdom
    if response['cultural_wisdom']:
        parts.append("\n🌏 Cultural Wisdom:")
        for wisdom in response['cultural_wisdom']:
            parts.append(f"\nFor {wisdom['condition']}:")
            parts.append(f"• {wisdom['wisdom']}")
            parts.append(f"• {wisdom['reassurance']}")
    
    # Add Urgency Notice if HIGH
    if response['urgency_level'] == "HIGH":
        parts.append("\n⚠️ URGENT: Please seek immediate medical attention!")
    
    return "\n".join(parts)

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
