"""
Compliance & Risk Monitoring Module
Checks marketing text for legal, GDPR, and claim risks
"""
from flask import Blueprint, request, jsonify
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_service import AIService

compliance_bp = Blueprint('compliance', __name__, url_prefix='/api/compliance')

# AI service dependency - will be injected by app.py
ai_service: Optional['AIService'] = None

def set_ai_service(service):
    """Inject the AI service instance"""
    global ai_service
    ai_service = service

@compliance_bp.route('/check', methods=['POST'])
def compliance_check():
    """
    POST /api/compliance/check
    Analyzes marketing text for compliance risks (GDPR, claims, legal issues)
    
    Expected JSON:
    {
        "marketing_text": string
    }
    
    Returns:
    {
        "risk_level": "low/medium/high",
        "flagged_phrases": [list],
        "suggestions": [list],
        "gdpr_compliant": bool
    }
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        if not data or 'marketing_text' not in data:
            return jsonify({'error': 'Missing marketing_text field'}), 400
        
        result = ai_service.compliance_check(data['marketing_text'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
