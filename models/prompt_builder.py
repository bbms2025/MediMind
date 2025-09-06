class AIPromptBuilder:
    """Builds structured medical prompts for the AI engine."""
    
    @staticmethod
    def create_diagnostic_prompt(symptoms: str, conditions_data: dict) -> str:
        """
        Creates a detailed diagnostic prompt that guides the AI to provide focused,
        relevant medical advice based on symptoms and our knowledge base.
        """
        prompt = f"""As a medical expert, analyze these symptoms: {symptoms}

Using our verified medical knowledge base and your expertise, please provide a structured analysis:

1. PRIMARY SYMPTOM ANALYSIS:
- Analyze how these symptoms might be related
- Identify potential underlying conditions
- Note any concerning combinations

2. LIKELY CONDITIONS:
{AIPromptBuilder._format_conditions_data(conditions_data)}

3. RESPONSE STRUCTURE:
- Start with the most likely condition based on the symptom combination
- Explain why this combination of symptoms suggests this condition
- Provide specific advice for managing these symptoms together
- Include relevant traditional and cultural perspectives
- Clearly state when immediate medical attention is needed

4. ADDITIONAL GUIDELINES:
- Focus on conditions that match multiple symptoms
- Consider both obvious and subtle connections
- Maintain medical accuracy while being easy to understand
- Include practical, actionable advice
- Note any red flags or warning signs

Remember to:
- Be precise and focused on the specific symptoms mentioned
- Avoid listing unrelated conditions
- Emphasize when professional medical evaluation is needed
- Include both immediate relief suggestions and long-term management strategies"""

        return prompt

    @staticmethod
    def _format_conditions_data(conditions: dict) -> str:
        """Formats condition data for inclusion in the prompt."""
        formatted = []
        for source, data in conditions.items():
            for condition in data:
                if 'common_symptoms' in condition:
                    symptoms = ', '.join(condition['common_symptoms'])
                    formatted.append(f"- {condition['condition']}: {symptoms}")
        
        return "Available conditions in our database:\n" + "\n".join(formatted)
