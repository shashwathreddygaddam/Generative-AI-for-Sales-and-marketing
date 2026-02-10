"""
Advanced Personalization Engine Module
AI-powered product recommendations based on user profile
"""
from flask import Blueprint, request, jsonify
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_service import AIService

personalization_bp = Blueprint('personalization', __name__, url_prefix='/api/personalize')

# AI service dependency - will be injected by app.py
ai_service: Optional['AIService'] = None

def set_ai_service(service):
    """Inject the AI service instance"""
    global ai_service
    ai_service = service

@personalization_bp.route('', methods=['POST'])
def personalize():
    """
    POST /api/personalize
    Generates AI-powered product recommendations
    
    Expected JSON:
    {
        "user_profile": string or dict (user information)
    }
    
    Returns:
    {
        "recommended_products": [
            {
                "name": string,
                "reason": string,
                "priority": "high/medium/low"
            }
        ]
    }
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        if not data or 'user_profile' not in data:
            return jsonify({'error': 'Missing user_profile field'}), 400
        
        result = ai_service.recommend_products(data['user_profile'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
