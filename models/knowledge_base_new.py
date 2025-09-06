from typing import Dict, List, Any
import json
import sqlite3

class KnowledgeBase:
    def __init__(self):
        self.db_path = "knowledge.db"
        self.cultural_data = self._load_json("data/cultural_bridge.json")
        self.modern_data = self._load_json("data/modern_medicine.json")
        self.traditional_data = self._load_json("data/traditional_medicine.json")
        self.ai_engine = None  # Will be initialized when needed

    def _load_json(self, file_path: str) -> List[Dict[str, Any]]:
        """Load and parse JSON data file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
            return []

    def get_relevant_knowledge(self, query: str) -> Dict[str, Any]:
        """Retrieve relevant knowledge from all sources"""
        try:
            query = query.lower()
            relevant_data = {
                'modern_medicine': [],
                'traditional_medicine': [],
                'cultural_bridge': [],
                'data_sources': {
                    'modern': False,
                    'traditional': False,
                    'cultural': False
                }
            }

            # Get knowledge from each source
            modern_results = self._search_modern_knowledge(query)
            traditional_results = self._search_traditional_knowledge(query)
            cultural_results = self._search_cultural_knowledge(query)

            # Update data and availability flags
            if modern_results:
                relevant_data['modern_medicine'] = modern_results
                relevant_data['data_sources']['modern'] = True

            if traditional_results:
                relevant_data['traditional_medicine'] = traditional_results
                relevant_data['data_sources']['traditional'] = True

            if cultural_results:
                relevant_data['cultural_bridge'] = cultural_results
                relevant_data['data_sources']['cultural'] = True

            # Format and return response
            return self._format_response(relevant_data, query)

        except Exception as e:
            print(f"Error in get_relevant_knowledge: {str(e)}")
            return self._format_response({
                'modern_medicine': [],
                'traditional_medicine': [],
                'cultural_bridge': [],
                'data_sources': {
                    'modern': False,
                    'traditional': False,
                    'cultural': False
                }
            }, query)

    def _search_cultural_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search through cultural knowledge base"""
        try:
            relevant_entries = []
            query_lower = query.lower()
            
            # First try exact match on condition
            for entry in self.cultural_data:
                if entry.get('condition', '').lower() == query_lower:
                    return [entry]
            
            # If no exact match, try keyword matching
            keywords = set(query_lower.split())
            for entry in self.cultural_data:
                entry_text = f"{entry.get('title', '')} {entry.get('scenario', '')} {entry.get('story_narrative', '')} {entry.get('wisdom_lesson', '')}".lower()
                if any(keyword in entry_text for keyword in keywords):
                    relevant_entries.append(entry)
            
            # Return matches or default response
            if relevant_entries:
                return relevant_entries[:3]

            # Try to generate cultural context using AI
            if not self.ai_engine:
                from .ai_engine import AIEngine
                self.ai_engine = AIEngine()

            try:
                cultural_context = self.ai_engine.generate_cultural_context(query)
                return [{
                    'title': query,
                    'cultural_context': cultural_context,
                    'is_generated': True
                }]
            except:
                return [{
                    'title': query,
                    'note': 'No specific cultural context found.',
                    'general_advice': 'Health practices vary across cultures. Consider both traditional and modern approaches.',
                    'is_generated': True
                }]

        except Exception as e:
            print(f"Error in cultural knowledge search: {str(e)}")
            return [{
                'title': query,
                'note': 'Unable to retrieve cultural context.',
                'general_advice': 'Please consult healthcare providers for guidance.',
                'is_generated': True
            }]

    def _search_modern_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search through modern medicine knowledge base"""
        try:
            results = []
            query_lower = query.lower()
            
            # First try exact match
            exact_matches = [entry for entry in self.modern_data 
                           if entry.get('condition', '').lower() == query_lower]
            if exact_matches:
                return exact_matches[:1]
            
            # Then try keyword matching
            results = [entry for entry in self.modern_data 
                      if any(keyword.lower() in query_lower 
                            for keyword in entry.get('keywords', []))]
            
            return results[:3] if results else []

        except Exception as e:
            print(f"Error in modern knowledge search: {str(e)}")
            return []

    def _search_traditional_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search through traditional medicine knowledge base"""
        try:
            results = []
            query_lower = query.lower()
            
            # First try exact match
            exact_matches = [entry for entry in self.traditional_data 
                           if entry.get('condition', '').lower() == query_lower]
            if exact_matches:
                return exact_matches[:1]
            
            # Then try keyword matching
            results = [entry for entry in self.traditional_data 
                      if any(keyword.lower() in query_lower 
                            for keyword in entry.get('keywords', []))]
            
            return results[:3] if results else []

        except Exception as e:
            print(f"Error in traditional knowledge search: {str(e)}")
            return []

    def _format_response(self, data: Dict[str, Any], query: str = '') -> Dict[str, Any]:
        """Format response with data availability flags and placeholders"""
        modern_available = bool(data['modern_medicine'])
        traditional_available = bool(data['traditional_medicine'])
        cultural_available = bool(data['cultural_bridge'])
        
        # Add data availability information
        data['data_sources'] = {
            'modern': modern_available,
            'traditional': traditional_available,
            'cultural': cultural_available
        }

        # Add placeholders for missing data
        if not modern_available and (traditional_available or cultural_available):
            data['modern_medicine'] = [{
                'condition': query,
                'note': 'No specific modern medical information is available.',
                'general_advice': 'Please consult a healthcare professional for proper medical advice.'
            }]
        
        if not traditional_available and (modern_available or cultural_available):
            data['traditional_medicine'] = [{
                'condition': query,
                'note': 'No traditional medicine information is available.',
                'general_advice': 'Consider exploring general wellness practices while consulting healthcare providers.'
            }]
        
        if not cultural_available:
            data['cultural_bridge'] = [{
                'title': query,
                'note': 'Cultural context is being generated.',
                'general_advice': 'Health practices vary across cultures. Consider discussing with community health advisors.',
                'is_generated': True
            }]
        
        return data
