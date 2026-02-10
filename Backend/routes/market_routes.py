"""
Market & Competitive Intelligence Module
Analyzes customer sentiment and competitor benchmarking
"""
from flask import Blueprint, request, jsonify
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_service import AIService

market_bp = Blueprint('market', __name__, url_prefix='/api/market')

# AI service dependency - will be injected by app.py
ai_service: Optional['AIService'] = None

def set_ai_service(service):
    """Inject the AI service instance"""
    global ai_service
    ai_service = service

@market_bp.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    """
    POST /api/market/sentiment
    Analyzes customer feedback sentiment and confidence
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        if not data or 'feedback' not in data:
            return jsonify({'error': 'Missing feedback field'}), 400
        
        result = ai_service.analyze_sentiment(data['feedback'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/benchmark', methods=['POST'])
def competitor_benchmark():
    """
    POST /api/market/benchmark
    Benchmarks competitor market position and trends
    """
    assert ai_service is not None, "AI service not initialized"
    try:
        data = request.get_json()
        if not data or 'brand' not in data:
            return jsonify({'error': 'Missing brand field'}), 400
        
        result = ai_service.competitor_benchmark(data['brand'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
