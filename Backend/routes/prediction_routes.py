"""
Predictive Customer Analytics Module
Predicts customer behavior and optimal touchpoints
"""
from flask import Blueprint, request, jsonify
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_service import AIService

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/predict')

# AI service dependency - will be injected by app.py
ai_service: Optional['AIService'] = None

def set_ai_service(service):
    """Inject the AI service instance"""
    global ai_service
    ai_service = service

@prediction_bp.route('/customer', methods=['POST'])
def predict_customer_behavior():
    """
    POST /api/predict/customer
    Predicts customer behavior, churn risk, and optimal engagement timing
    
    Expected JSON:
    {
        "history_data": string or dict (customer interaction history)
    }
    
    Returns:
    {
        "churn_risk": "high/medium/low",
        "churn_probability": 0-100,
        "next_best_action": string,
        "campaign_timing": string,
        "recommended_channel": string
    }
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        if not data or 'history_data' not in data:
            return jsonify({'error': 'Missing history_data field'}), 400
        
        result = ai_service.predict_behavior(data['history_data'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
