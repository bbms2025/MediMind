import json
import sqlite3
from typing import Dict, List, Any
from pathlib import Path

class KnowledgeBase:
    def __init__(self):
        self.db_path = "knowledge.db"
        self.cultural_data = self._load_json("data/cultural_bridge.json")
        self.modern_data = self._load_json("data/modern_medicine.json")
        self.traditional_data = self._load_json("data/traditional_medicine.json")
    
    def init_db(self):
        """Initialize SQLite database for caching and logging"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for caching and logging
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_cache (
                query_hash TEXT PRIMARY KEY,
                query TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interaction_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                response_type TEXT,
                effectiveness_rating INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_relevant_knowledge(self, query: str) -> Dict[str, Any]:
        """
        Retrieve relevant knowledge from all sources based on the query
        """
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
            
            # Modern medicine: match by condition, keywords, or symptoms
            if self.modern_data:
                for item in self.modern_data:
                    if item.get('condition', '').lower() in query:
                        relevant_data['modern_medicine'].append(item)
                        continue
                    keywords = [kw.lower() for kw in item.get('keywords', [])]
                    symptoms = [s.lower() for s in item.get('common_symptoms', [])]
                    if any(kw in query for kw in keywords) or any(s in query for s in symptoms):
                        relevant_data['modern_medicine'].append(item)
            
            # Traditional medicine: match by condition
            if self.traditional_data:
                for item in self.traditional_data:
                    if item.get('condition', '').lower() in query:
                        relevant_data['traditional_medicine'].append(item)
            
            # Cultural bridge: match by scenario, title, or condition
            if self.cultural_data:
                for item in self.cultural_data:
                    if (item.get('title', '').lower() in query or 
                        item.get('scenario', '').lower() in query or 
                        item.get('condition', '').lower() in query):
                        relevant_data['cultural_bridge'].append(item)
            
            # Format the response with data availability information
            return self._format_response(relevant_data)
            
        except Exception as e:
            print(f"Error in get_relevant_knowledge: {str(e)}")
            return self._format_response({
                'modern_medicine': [],
                'traditional_medicine': [],
                'cultural_bridge': []
            })
    
    def log_interaction(self, query: str, response_type: str, effectiveness: int = None):
        """Log user interaction and its effectiveness"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interaction_log (query, response_type, effectiveness_rating)
            VALUES (?, ?, ?)
        ''', (query, response_type, effectiveness))
        
        conn.commit()
        conn.close()
    
    def _load_json(self, file_path: str) -> List[Dict[str, Any]]:
        """Load and parse JSON data file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
            return []
    
    def _check_cache(self, query: str) -> Dict[str, Any]:
        """Check if query result is cached"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT response FROM query_cache 
            WHERE query_hash = ? AND 
            datetime(timestamp) > datetime('now', '-1 day')
        ''', (hash(query),))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
    
    def _cache_response(self, query: str, response: Dict[str, Any]):
        """Cache the query response"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO query_cache (query_hash, query, response)
            VALUES (?, ?, ?)
        ''', (hash(query), query, json.dumps(response)))
        
        conn.commit()
        conn.close()
    
    def _search_cultural_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search through cultural knowledge base"""
        try:
            relevant_entries = []
            query_lower = query.lower()
            
            # First try exact match
            for entry in self.cultural_data:
                if entry.get('condition', '').lower() == query_lower:
                    return [entry]
            
            # If no exact match, try keyword matching
            keywords = set(query_lower.split())
            for entry in self.cultural_data:
                entry_text = ' '.join([
                    entry.get('title', ''),
                    entry.get('scenario', ''),
                    entry.get('story_narrative', ''),
                    entry.get('wisdom_lesson', '')
                ]).lower()
                
                if any(keyword in entry_text for keyword in keywords):
                    relevant_entries.append(entry)
            
            return relevant_entries[:3]
            
        except Exception as e:
            print(f"Error in cultural knowledge search: {str(e)}")
            return []
    
    def _search_modern_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search through modern medicine knowledge base"""
        results = [entry for entry in self.modern_data 
                  if any(keyword in query.lower() 
                        for keyword in entry.get('keywords', []))]
        return results
    
    def _search_traditional_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search through traditional medicine knowledge base"""
        results = [entry for entry in self.traditional_data 
                  if any(keyword in query.lower() 
                        for keyword in entry.get('keywords', []))]
        return results
    
    def _format_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format response with data availability flags"""
        modern_available = bool(data['modern_medicine'])
        traditional_available = bool(data['traditional_medicine'])
        cultural_available = bool(data['cultural_bridge'])
        
        # Add data availability information
        data['data_sources'] = {
            'modern': modern_available,
            'traditional': traditional_available,
            'cultural': cultural_available
        }
        
        # Initialize AI engine if needed
        if not hasattr(self, 'ai_engine'):
            try:
                from .ai_engine import AIEngine
                self.ai_engine = AIEngine()
            except ImportError:
                print("AI engine not available")
                self.ai_engine = None
        
        # Get condition name from available data
        condition = None
        if modern_available and data['modern_medicine']:
            condition = data['modern_medicine'][0].get('condition')
        elif traditional_available and data['traditional_medicine']:
            condition = data['traditional_medicine'][0].get('condition')
            
        # Add placeholders for missing data
        if not modern_available and (traditional_available or cultural_available):
            data['modern_medicine'] = [{
                'note': 'No specific modern medical information is available for this condition.',
                'general_advice': 'Please consult a healthcare professional for proper medical advice.'
            }]
            
        if not traditional_available and (modern_available or cultural_available):
            data['traditional_medicine'] = [{
                'note': 'No traditional medicine information is available for this condition.',
                'general_advice': 'While we don\'t have specific traditional remedies, consider exploring general wellness practices.'
            }]
            
        # Generate cultural context if not available or empty
        if (not cultural_available or not data['cultural_bridge']) and condition and self.ai_engine:
            try:
                # Get modern and traditional info if available
                modern_info = data['modern_medicine'][0] if modern_available and data['modern_medicine'] else None
                traditional_info = data['traditional_medicine'][0] if traditional_available and data['traditional_medicine'] else None
                
                # Generate cultural context
                cultural_context = self.ai_engine.generate_cultural_context(
                    condition,
                    modern_info=modern_info,
                    traditional_info=traditional_info
                )
                
                # Ensure we have valid data
                if isinstance(cultural_context, dict) and any(cultural_context.values()):
                    data['cultural_bridge'] = [{
                        'title': condition,
                        'analogy': cultural_context.get('analogy', 'Every culture understands health differently'),
                        'reassurance': cultural_context.get('reassurance', 'Each person\'s healing journey is unique'),
                        'self_care': cultural_context.get('self_care', 'Consider both traditional and modern approaches'),
                        'cultural_wisdom': cultural_context.get('cultural_wisdom', 'Health wisdom transcends cultures'),
                        'note': '(AI-assisted cultural insights)',
                        'is_generated': True
                    }]
                    data['data_sources']['cultural'] = 'ai-generated'
                else:
                    raise ValueError("Invalid cultural context generated")
                    
            except Exception as e:
                print(f"Error generating cultural context: {str(e)}")
                data['cultural_bridge'] = [{
                    'title': condition,
                    'note': 'Cultural context is currently being generated.',
                    'general_advice': 'Health practices vary across cultures. Consider discussing with community health advisors.',
                    'is_generated': False
                }]
            
        return data