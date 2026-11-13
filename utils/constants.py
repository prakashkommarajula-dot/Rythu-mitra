"""
Application constants for Rythu Mithra.
"""

# Supported Languages and Web Speech API Language Tags
SUPPORTED_LANGUAGES = {
    'te': {
        'name': 'Telugu',
        'native': 'తెలుగు',
        'speech_tag': 'te-IN',
        'fallback_message': 'క్షమించండి, మీ ప్రశ్నను అర్థం చేసుకోలేకపోయాము. దయచేసి స్పష్టంగా అడగండి.'
    },
    'hi': {
        'name': 'Hindi',
        'native': 'हिन्दी',
        'speech_tag': 'hi-IN',
        'fallback_message': 'क्षमा करें, हम आपके प्रश्न को समझ नहीं पाए। कृपया पुनः प्रयास करें।'
    },
    'en': {
        'name': 'English',
        'native': 'English',
        'speech_tag': 'en-IN',
        'fallback_message': 'Sorry, could not interpret your agricultural query. Please rephrase.'
    },
    'ta': {
        'name': 'Tamil',
        'native': 'தமிழ்',
        'speech_tag': 'ta-IN',
        'fallback_message': 'மன்னிக்கவும், உங்கள் கேள்வியை புரிந்து கொள்ள முடியவில்லை.'
    },
    'kn': {
        'name': 'Kannada',
        'native': 'ಕನ್ನಡ',
        'speech_tag': 'kn-IN',
        'fallback_message': 'ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.'
    }
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

SEVERITY_LEVELS = ['None', 'Low', 'Moderate', 'High', 'Critical']
