"""
24/7 AI Chatbot Module
Conversational assistant for customer inquiries
"""
from flask import Blueprint, request, jsonify
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_service import AIService

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chat')

# AI service dependency - will be injected by app.py
ai_service: Optional['AIService'] = None

def set_ai_service(service):
    """Inject the AI service instance"""
    global ai_service
    ai_service = service

@chatbot_bp.route('', methods=['POST'])
def chat():
    """
    POST /api/chat
    24/7 AI chatbot for customer inquiries
    
    Expected JSON:
    {
        "message": string,
        "history": [optional list of previous messages]
    }
    
    Returns:
    {
        "response": string,
        "status": "success/error"
    }
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        history = data.get('history', [])
        result = ai_service.ai_chat_response(data['message'], history)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'response': str(e), 'status': 'error'}), 500
