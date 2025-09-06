from gtts import gTTS
import base64
import io

class VoiceProcessor:
    def __init__(self):
        self.language = 'en'
    
    def text_to_speech(self, text: str) -> str:
        """
        Convert text to speech and return as base64 encoded audio
        """
        try:
            # Create a bytes buffer for the audio
            audio_buffer = io.BytesIO()
            
            # Generate speech
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.write_to_fp(audio_buffer)
            
            # Get the audio data and encode it
            audio_buffer.seek(0)
            audio_data = base64.b64encode(audio_buffer.read()).decode()
            
            return audio_data
        
        except Exception as e:
            raise Exception(f"Error in text-to-speech conversion: {str(e)}")
    
    def set_language(self, language_code: str):
        """
        Set the language for text-to-speech conversion
        """
        self.language = language_code
