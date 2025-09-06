import requests
from typing import Dict, Any
import json

class AIEngine:
    """
    AI engine using Hugging Face router API with gpt-oss models.
    """

    def __init__(self):
        # 🔑 Hugging Face API token
        self.hf_token = "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"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}

        # Router endpoint (OpenAI-compatible)
        self.api_url = "https://router.huggingface.co/v1/chat/completions"

        # Models
        self.storyteller_model = "openai/gpt-oss-120b"
        self.emergency_model   = "openai/gpt-oss-20b"

    def _make_api_call(self, model: str, prompt: str) -> str:
        """Call Hugging Face router API"""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful medical assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500
                }
            )

            print(f"Hugging Face API call to {model} status: {response.status_code}")
            print(f"Response text: {response.text}")

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API call failed with status {response.status_code}: {response.text}")
        except Exception as e:
            print("Exception in _make_api_call:", str(e))
            raise

    def generate_cultural_context(self, condition: str, modern_info: Dict[str, Any] = None, traditional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate cultural context when it's not available in the database"""
        if not condition:
            return {
                "error": "No condition provided",
                "title": "Unknown Condition",
                "analogy": "Health is a universal journey",
                "reassurance": "Every culture has its own way of understanding health",
                "self_care": "Consider both traditional and modern approaches to healing",
                "cultural_wisdom": "Health wisdom transcends boundaries"
            }
            
        prompt = f"""Create a culturally sensitive explanation for '{condition}'.

        Available Information:
        {f"Modern Medicine: {modern_info.get('explanation', '')}" if modern_info else ""}
        {f"Traditional Medicine: {traditional_info.get('explanation', '')}" if traditional_info else ""}
        
        Please provide:
        1. A cultural analogy that helps understand the condition
        2. A reassuring message that considers different cultural perspectives
        3. Self-care advice that respects cultural practices
        4. A relevant cultural wisdom or proverb about healing
        
        Response format (JSON):
        {{
            "title": "{condition}",
            "analogy": "cultural analogy here",
            "reassurance": "reassuring message here",
            "self_care": "culturally sensitive self-care advice",
            "cultural_wisdom": "relevant proverb or wisdom"
        }}"""

        try:
            response = self._make_api_call(self.storyteller_model, prompt)
            # Try to parse as JSON, if fails, structure the text response
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Extract information from text response
                return {
                    "title": condition,
                    "analogy": "Understanding through cultural lens: " + response.split('\n')[0],
                    "reassurance": "Cultural perspective: Every culture has its own way of healing.",
                    "self_care": "Blend of traditional and modern approaches recommended",
                    "cultural_wisdom": "Health wisdom is universal across cultures"
                }
        except Exception as e:
            print(f"Error generating cultural context: {str(e)}")
            return {
                "title": condition,
                "analogy": "Every culture understands illness differently",
                "reassurance": "Healing practices vary across cultures",
                "self_care": "Consider both traditional and modern approaches",
                "cultural_wisdom": "Health is a universal language"
            }

    def process_query(self, user_input: str, knowledge_context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a normal query using the storyteller model"""
        try:
            # Improved prompt engineering
            prompt = f"""
You are a medical assistant. Use the following context to answer the user's question:
Traditional Medicine: {knowledge_context.get('traditional_medicine', '')}
Modern Medicine: {knowledge_context.get('modern_medicine', '')}
User Query: {user_input}
Please provide clear, concise, and actionable advice for both traditional and modern approaches. If you don't know, say so.
"""
            # Build separate sections for traditional and modern medicine
            traditional_section = ""
            modern_section = ""
            # Traditional medicine
            if knowledge_context.get('traditional_medicine'):
                for item in knowledge_context['traditional_medicine']:
                    if item.get('condition'):
                        traditional_section += f"<b>Traditional Medicine for {item['condition']}:</b><br>"
                        if item.get('traditional_remedy'):
                            traditional_section += f"Remedy: {item['traditional_remedy']}<br>"
                        if item.get('traditional_explanation'):
                            traditional_section += f"Explanation: {item['traditional_explanation']}<br>"
                        if item.get('wisdom_saying'):
                            traditional_section += f"Wisdom: {item['wisdom_saying']}<br>"
                        traditional_section += "<br>"
            # Modern medicine
            if knowledge_context.get('modern_medicine'):
                for item in knowledge_context['modern_medicine']:
                    if item.get('condition'):
                        modern_section += f"<b>Modern Medicine for {item['condition']}:</b><br>"
                        if item.get('simple_explanation'):
                            modern_section += f"Explanation: {item['simple_explanation']}<br>"
                        if item.get('common_symptoms'):
                            modern_section += f"Symptoms: {', '.join(item['common_symptoms'])}<br>"
                        if item.get('reassurance_note'):
                            modern_section += f"Doctor's advice: {item['reassurance_note']}<br>"
                        modern_section += "<br>"
            # Compose final message
            message = f"<div class='traditional-section'>{traditional_section}</div><div class='modern-section'>{modern_section}</div>"
            if not message.strip():
                return {"message": "I'm sorry, I couldn't find an answer for your query.", "status": "error"}
            return {"message": message, "status": "success"}
        except Exception as e:
            return {
                "message": "I apologize, but I'm having technical difficulties right now. Please try again later.",
                "status": "error",
                "error": str(e)
            }

    def get_emergency_response(self, user_input: str) -> Dict[str, str]:
        """Generate emergency response using the emergency model"""
        prompt = f"""Assess this emergency situation and provide immediate guidance:

Symptoms/Situation: {user_input}

Provide:
1. Quick assessment
2. Immediate actions needed
3. Whether emergency services should be called"""
        try:
            response_text = self._make_api_call(self.emergency_model, prompt)
            lines = response_text.split("\n")
            diagnosis = next((line for line in lines if "assessment" in line.lower()), "Emergency assessment needed")
            actions = "\n".join(line for line in lines if line.startswith("-") or line.startswith("*"))

            return {
                "diagnosis": diagnosis,
                "actions": actions if actions else "Seek immediate medical attention",
                "seek_help": "Please contact emergency services immediately"
            }
        except Exception as e:
            raise Exception(f"Error generating emergency response: {str(e)}")

    def check_models_status(self) -> Dict[str, bool]:
        """Check if router API responds for both models"""
        status = {}
        for name, model in [("storyteller_model", self.storyteller_model),
                            ("emergency_model", self.emergency_model)]:
            try:
                test_prompt = "Say 'OK' if you are working."
                response = self._make_api_call(model, test_prompt)
                status[name] = "OK" in response
            except:
                status[name] = False
        return status

