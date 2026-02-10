"""
Smart Pricing Engine Module
Dynamic pricing based on cost, demand, and competitor prices
"""
from flask import Blueprint, request, jsonify
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_service import AIService

pricing_bp = Blueprint('pricing', __name__, url_prefix='/api/pricing')

# AI service dependency - will be injected by app.py
ai_service: Optional['AIService'] = None

def set_ai_service(service):
    """Inject the AI service instance"""
    global ai_service
    ai_service = service

@pricing_bp.route('/optimize', methods=['POST'])
def optimize_pricing():
    """
    POST /api/pricing/optimize
    Calculates optimal dynamic pricing based on market conditions
    
    Expected JSON:
    {
        "cost": float,
        "demand_index": float (0.5-1.5),
        "competitor_price": float
    }
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['cost', 'demand_index', 'competitor_price']
        if not all(field in data for field in required):
            return jsonify({'error': f'Missing fields. Required: {required}'}), 400
        
        result = ai_service.dynamic_price(
            data['cost'],
            data['demand_index'],
            data['competitor_price']
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
