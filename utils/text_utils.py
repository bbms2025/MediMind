from typing import List, Dict, Any
import re

class TextProcessor:
    def __init__(self):
        self.emergency_patterns = [
            r"(severe|intense|extreme)\s+pain",
            r"difficulty\s+breathing",
            r"chest\s+pain",
            r"unconscious",
            r"not\s+breathing",
            r"severe\s+bleeding",
            r"head\s+injury",
            r"seizure",
            r"stroke",
            r"heart\s+attack"
        ]

    def assess_urgency(self, text: str) -> int:
        """Return an urgency score based on emergency patterns found in the text."""
        text = text.lower()
        score = 0
        for pattern in self.emergency_patterns:
            if re.search(pattern, text):
                score += 8  # Arbitrary high score for emergency keyword
        return score
    
    def detect_emergency(self, text: str) -> bool:
        """
        Detect if the text contains emergency keywords
        """
        text = text.lower()
        return any(re.search(pattern, text) for pattern in self.emergency_patterns)
    
    def extract_symptoms(self, text: str) -> List[str]:
        """
        Extract potential symptoms from user input
        """
        # Common symptom patterns
        symptom_patterns = [
            r"(feeling|feel|felt)\s+(.*?)(\.|\n|$)",
            r"(having|have|had)\s+(.*?)(\.|\n|$)",
            r"(suffering from)\s+(.*?)(\.|\n|$)"
        ]
        
        symptoms = []
        for pattern in symptom_patterns:
            matches = re.finditer(pattern, text.lower())
            symptoms.extend(match.group(2).strip() for match in matches)
        
        return symptoms
    
    def format_response(self, response_data: Dict[str, Any]) -> str:
        """
        Format the response in a user-friendly way
        """
        if response_data.get('type') == 'emergency':
            return self._format_emergency_response(response_data)
        return self._format_normal_response(response_data)
    
    def _format_emergency_response(self, data: Dict[str, Any]) -> str:
        """
        Format emergency response with clear instructions
        """
        return f"""
        🚨 EMERGENCY ALERT 🚨
        
        {data.get('message', '')}
        
        IMMEDIATE ACTIONS:
        {data.get('recommendations', {}).get('immediate_actions', '')}
        
        SEEK MEDICAL HELP:
        {data.get('recommendations', {}).get('seek_help', '')}
        """
    
    def _format_normal_response(self, data: Dict[str, Any]) -> str:
        """
        Format normal response with cultural context and medical advice
        """
        response = f"""
        {data.get('message', '')}
        
        """
        
        if data.get('cultural_context'):
            response += f"\nCultural Wisdom:\n{data['cultural_context']}\n"
        
        if data.get('medical_advice'):
            response += f"\nMedical Context:\n{data['medical_advice']}\n"
        
        response += f"\nDisclaimer:\n{data.get('disclaimer', '')}"
        
        return response
