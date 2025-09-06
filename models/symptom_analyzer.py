from typing import Dict, List, Set, Tuple
import json
from pathlib import Path

class SymptomAnalyzer:
    def __init__(self):
        self.condition_data = self._load_all_conditions()
        self.symptom_index = self._build_symptom_index()
    
    def _load_all_conditions(self) -> Dict:
        """Load and combine all condition data"""
        base_path = Path("data")
        data = {
            "cultural": self._load_json(base_path / "cultural_bridge.json"),
            "modern": self._load_json(base_path / "modern_medicine.json"),
            "traditional": self._load_json(base_path / "traditional_medicine.json")
        }
        return data
    
    def _load_json(self, path: Path) -> List[Dict]:
        """Load JSON file safely"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return []

    def _build_symptom_index(self) -> Dict[str, Set[str]]:
        """Build an index of symptoms to conditions"""
        index = {}
        for source, conditions in self.condition_data.items():
            for condition in conditions:
                if 'common_symptoms' in condition:
                    for symptom in condition['common_symptoms']:
                        symptom_lower = symptom.lower()
                        if symptom_lower not in index:
                            index[symptom_lower] = set()
                        index[symptom_lower].add(f"{source}:{condition['condition']}")
        return index

    def analyze_symptoms(self, symptoms: str) -> Dict:
        """Analyze a set of symptoms and return relevant conditions"""
        symptoms_lower = symptoms.lower()
        matched_conditions = {}
        urgency_level = "LOW"
        
        # Split input into individual symptoms
        symptom_list = [s.strip() for s in symptoms_lower.split('and')]
        
        # Match symptoms to conditions
        for symptom in symptom_list:
            # Direct matches
            for indexed_symptom, conditions in self.symptom_index.items():
                if symptom in indexed_symptom or indexed_symptom in symptom:
                    for condition_key in conditions:
                        source, condition = condition_key.split(':')
                        if condition not in matched_conditions:
                            matched_conditions[condition] = {
                                'source': source,
                                'matched_symptoms': set(),
                                'relevance_score': 0
                            }
                        matched_conditions[condition]['matched_symptoms'].add(symptom)
                        matched_conditions[condition]['relevance_score'] += 1

        # Calculate confidence and urgency
        for condition, data in matched_conditions.items():
            total_symptoms = len(self._get_condition_symptoms(condition))
            matched = len(data['matched_symptoms'])
            data['confidence'] = (matched / total_symptoms) * 100
            
            # Check urgency indicators
            if self._check_urgency_indicators(condition, data['matched_symptoms']):
                urgency_level = "HIGH"
        
        return {
            'matched_conditions': matched_conditions,
            'urgency_level': urgency_level,
            'total_symptoms': len(symptom_list)
        }

    def _get_condition_symptoms(self, condition_name: str) -> List[str]:
        """Get all symptoms for a condition"""
        for source, conditions in self.condition_data.items():
            for cond in conditions:
                if cond['condition'] == condition_name and 'common_symptoms' in cond:
                    return cond['common_symptoms']
        return []

    def _check_urgency_indicators(self, condition: str, symptoms: Set[str]) -> bool:
        """Check if symptoms indicate high urgency"""
        urgent_indicators = {
            'severe', 'emergency', 'immediate', 'critical',
            'chest pain', 'difficulty breathing', 'unconscious',
            'severe bleeding', 'stroke', 'heart attack'
        }
        return any(indicator in ' '.join(symptoms).lower() for indicator in urgent_indicators)

    def get_combined_response(self, analysis_results: Dict) -> Dict:
        """Generate a complete response combining all medical perspectives"""
        response = {
            'primary_conditions': [],
            'traditional_advice': [],
            'modern_advice': [],
            'cultural_wisdom': [],
            'urgency_level': analysis_results['urgency_level']
        }
        
        # Sort conditions by confidence
        sorted_conditions = sorted(
            analysis_results['matched_conditions'].items(),
            key=lambda x: x[1]['confidence'],
            reverse=True
        )
        
        # Get detailed information for each condition
        for condition_name, data in sorted_conditions:
            for source, conditions in self.condition_data.items():
                for cond in conditions:
                    if cond['condition'] == condition_name:
                        if source == 'cultural':
                            response['cultural_wisdom'].append({
                                'condition': condition_name,
                                'wisdom': cond.get('everyday_analogy', ''),
                                'reassurance': cond.get('reassurance_note', '')
                            })
                        elif source == 'modern':
                            response['modern_advice'].append({
                                'condition': condition_name,
                                'explanation': cond.get('simple_explanation', ''),
                                'care': cond.get('self_care_basics', [])
                            })
                        elif source == 'traditional':
                            response['traditional_advice'].append({
                                'condition': condition_name,
                                'remedy': cond.get('remedy', ''),
                                'explanation': cond.get('explanation', '')
                            })
        
        return response
