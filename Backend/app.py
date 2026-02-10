import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ai_service import AIService

# Import all blueprint modules
from routes.market_routes import market_bp, set_ai_service as set_ai_market
from routes.pricing_routes import pricing_bp, set_ai_service as set_ai_pricing
from routes.compliance_routes import compliance_bp, set_ai_service as set_ai_compliance
from routes.chatbot_routes import chatbot_bp, set_ai_service as set_ai_chatbot
from routes.prediction_routes import prediction_bp, set_ai_service as set_ai_prediction
from routes.personalization_routes import personalization_bp, set_ai_service as set_ai_personalization

# Configure Flask to look in the sibling 'frontend' directory
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
CORS(app)

# Initialize AI Service
ai = AIService()

# Inject AI service into all blueprints
set_ai_market(ai)
set_ai_pricing(ai)
set_ai_compliance(ai)
set_ai_chatbot(ai)
set_ai_prediction(ai)
set_ai_personalization(ai)

# Register all blueprints
app.register_blueprint(market_bp)
app.register_blueprint(pricing_bp)
app.register_blueprint(compliance_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(personalization_bp)

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Landing page / dashboard redirect"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard with all 6 AI modules"""
    return render_template('index.html')

@app.route('/generator-hub-test')
def generator_hub_test():
    """Testing interface for Generator Hub modules"""
    return render_template('generator_hub_test.html')

# ==================== LEGACY API ROUTES ====================
# Keeping legacy endpoints for backward compatibility

@app.route('/api/campaign', methods=['POST'])
def campaign():
    data = request.form
    result = ai.generate_campaign(data['product'], data['audience'], data['platform'])
    return jsonify({'result': result})

@app.route('/api/pitch', methods=['POST'])
def pitch():
    data = request.form
    result = ai.generate_pitch(data['product'], data['customer'])
    return jsonify({'result': result})

@app.route('/api/score', methods=['POST'])
def score():
    data = request.form
    result = ai.score_lead(data['name'], data['budget'], data['need'], data['urgency'])
    return jsonify({'result': result})

# ==================== NEW ENHANCED ENDPOINTS ====================
# These handle both form data and JSON for unified API

@app.route('/api/market/sentiment', methods=['POST'])
def sentiment_endpoint():
    """Sentiment analysis endpoint"""
    try:
        data = request.get_json()
        if not data or 'feedback' not in data:
            return jsonify({'error': 'Missing feedback field'}), 400
        
        result = ai.analyze_sentiment(data['feedback'])
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pricing/optimize', methods=['POST'])
def pricing_endpoint():
    """Dynamic pricing endpoint"""
    try:
        data = request.get_json()
        required = ['cost', 'demand_index', 'competitor_price']
        if not all(field in data for field in required):
            return jsonify({'error': f'Missing fields. Required: {required}'}), 400
        
        result = ai.dynamic_price(data['cost'], data['demand_index'], data['competitor_price'])
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compliance/check', methods=['POST'])
def compliance_endpoint():
    """Compliance check endpoint"""
    try:
        data = request.get_json()
        if not data or 'marketing_text' not in data:
            return jsonify({'error': 'Missing marketing_text field'}), 400
        
        result = ai.compliance_check(data['marketing_text'])
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chatbot_endpoint():
    """AI Chatbot endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': 'No message provided', 'status': 'error'}), 400
        
        history = data.get('history', [])
        result = ai.ai_chat_response(data['message'], history)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'response': str(e), 'status': 'error'}), 500

@app.route('/api/predict/customer', methods=['POST'])
def prediction_endpoint():
    """Predictive analytics endpoint"""
    try:
        data = request.get_json()
        if not data or 'history_data' not in data:
            return jsonify({'error': 'Missing history_data field'}), 400
        
        result = ai.predict_behavior(data['history_data'])
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/personalize', methods=['POST'])
def personalization_endpoint():
    """Personalization engine endpoint"""
    try:
        data = request.get_json()
        if not data or 'user_profile' not in data:
            return jsonify({'error': 'Missing user_profile field'}), 400
        
        result = ai.recommend_products(data['user_profile'])
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Platform is running'}), 200

# ==================== GENERATOR HUB ENDPOINTS ====================

@app.route('/api/generator/marketing-campaign', methods=['POST'])
def generator_marketing_campaign():
    """
    AI Marketing Strategist Endpoint
    Generates comprehensive marketing campaign strategy
    """
    try:
        data = request.get_json()
        if not data or 'product_details' not in data or 'linkedin_demographics' not in data:
            return jsonify({'error': 'Missing required fields: product_details, linkedin_demographics'}), 400
        
        result = ai.generate_marketing_campaign_strategy(
            data['product_details'],
            data['linkedin_demographics']
        )
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generator/sales-pitch', methods=['POST'])
def generator_sales_pitch():
    """
    B2B Sales Pitch Architect Endpoint
    Generates personalized sales pitch based on prospect profile
    """
    try:
        data = request.get_json()
        if not data or 'prospect_title' not in data or 'company_tier' not in data:
            return jsonify({'error': 'Missing required fields: prospect_title, company_tier'}), 400
        
        result = ai.generate_sales_pitch(
            data['prospect_title'],
            data['company_tier'],
            data.get('product_info', '')
        )
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generator/lead-score', methods=['POST'])
def generator_lead_score():
    """
    Intelligent Lead Scorer Endpoint
    Calculates lead score and provides reasoning
    """
    try:
        data = request.get_json()
        if not data or 'budget' not in data or 'timeline' not in data or 'urgency' not in data:
            return jsonify({'error': 'Missing required fields: budget, timeline, urgency'}), 400
        
        result = ai.intelligent_lead_score(
            data['budget'],
            data['timeline'],
            data['urgency'],
            data.get('additional_context', '')
        )
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== NEW ENDPOINTS: NODE.JS PATTERN (MarketMind AI Hub) ====================

@app.route('/api/generate-campaign', methods=['POST'])
def generate_campaign():
    """
    Marketing Strategy Endpoint (Node.js Pattern)
    Generates comprehensive campaign strategy using system prompt + user prompt.
    
    Request body:
    {
        "productDetails": "Your product description",
        "audience": "Target audience description"
    }
    """
    try:
        data = request.get_json()
        if not data or 'productDetails' not in data or 'audience' not in data:
            return jsonify({'error': 'Missing required fields: productDetails, audience'}), 400
        
        product_details = data['productDetails']
        audience = data['audience']
        
        # System prompt (role-based)
        system_prompt = "Act as a LinkedIn Marketing Expert and Strategic Campaign Designer."
        
        # User prompt (user request)
        user_prompt = f"""Create a comprehensive marketing campaign strategy in VALID JSON format.

Product: {product_details}
Target Audience: {audience}

Return ONLY valid JSON with this exact structure (no markdown wrapping, no extra text):
{{
    "campaign_objectives": ["objective 1", "objective 2", "objective 3"],
    "content_ideas": [
        {{"title": "idea title", "format": "article/video/webinar", "key_message": "main point", "engagement_angle": "how to engage"}},
        ...5 ideas total...
    ],
    "ad_copy_variations": [
        {{"variation": 1, "headline": "headline", "body": "body copy", "tone": "professional/casual/urgent"}},
        ...3 variations total...
    ],
    "platform_specific_ctas": {{"linkedin": "CTA text", "email": "CTA text", "web": "CTA text"}},
    "campaign_timeline": "timeline description",
    "expected_kpis": {{"ctr": "expected CTR", "conversion": "expected conversion rate", "lead_quality": "quality assessment"}}
}}"""
        
        # Call centralized LLM handler
        result = ai.call_llm_with_system_prompt(system_prompt, user_prompt)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/generate-pitch', methods=['POST'])
def generate_pitch():
    """
    Sales Pitch Endpoint (Node.js Pattern)
    Generates personalized B2B sales pitch using system prompt + user prompt.
    
    Request body:
    {
        "title": "Prospect job title",
        "companyTier": "Fortune 500 / Large Enterprise / Mid-Market / Small Business / Startup"
    }
    """
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'companyTier' not in data:
            return jsonify({'error': 'Missing required fields: title, companyTier'}), 400
        
        title = data['title']
        company_tier = data['companyTier']
        
        # System prompt (role-based)
        system_prompt = "Act as an Elite B2B Sales Architect and Sales Strategy Expert."
        
        # User prompt (user request)
        user_prompt = f"""Create a tailored B2B sales pitch in VALID JSON format.

Prospect Title: {title}
Company Tier: {company_tier}

Return ONLY valid JSON with this exact structure (no markdown wrapping, no extra text):
{{
    "elevator_pitch_30sec": "30-second pitch",
    "pain_point_analysis": {{
        "primary_pain": "main pain point",
        "secondary_pains": ["pain 1", "pain 2"]
    }},
    "differentiators": [
        {{"differentiator": "what we offer", "benefits_for_role": "how it helps them", "impact": "concrete results"}},
        ...3 total...
    ],
    "strategic_cta": {{
        "immediate_next_step": "action to take",
        "suggested_angle": "positioning approach",
        "objection_handler": "response to common objection"
    }},
    "discovery_questions": ["question 1", "question 2", "question 3"],
    "social_proof_angles": ["proof angle 1", "proof angle 2"]
}}"""
        
        # Call centralized LLM handler
        result = ai.call_llm_with_system_prompt(system_prompt, user_prompt)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/score-lead', methods=['POST'])
def score_lead():
    """
    Lead Scorer Endpoint (Node.js Pattern)
    Hybrid scoring: Deterministic algorithm + AI reasoning.
    
    Request body:
    {
        "budget": "Budget amount (e.g., '$50000', '1.5M')",
        "timeline": "Immediate / This Month / This Quarter / This Year / Next Year",
        "urgency": "High / Medium / Low"
    }
    """
    try:
        data = request.get_json()
        if not data or 'budget' not in data or 'timeline' not in data or 'urgency' not in data:
            return jsonify({'error': 'Missing required fields: budget, timeline, urgency'}), 400
        
        budget = data['budget']
        timeline = data['timeline']
        urgency = data['urgency']
        
        # DETERMINISTIC SCORING (Hard-coded logic matching Node.js pattern)
        score = 0
        
        # Budget scoring (simplified vs detailed in Python version)
        try:
            # Extract numeric value from budget string
            budget_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', budget.replace(',', ''))))
            if budget_value >= 50000:
                score += 40
            elif budget_value >= 10000:
                score += 25
            else:
                score += 10
        except:
            score += 15  # Default if parsing fails
        
        # Timeline scoring
        timeline_lower = timeline.lower()
        if "immediate" in timeline_lower or "this week" in timeline_lower:
            score += 30
        elif "this month" in timeline_lower:
            score += 25
        elif "this quarter" in timeline_lower:
            score += 15
        elif "this year" in timeline_lower:
            score += 10
        else:
            score += 5
        
        # Urgency scoring
        urgency_lower = urgency.lower()
        if "high" in urgency_lower:
            score += 30
        elif "medium" in urgency_lower:
            score += 15
        else:
            score += 5
        
        # Cap score at 100
        score = min(score, 100)
        
        # Calculate conversion probability (matching Node.js pattern)
        conversion_probability = f"{int(score * 0.9)}%"
        
        # AI REASONING (LLM explains the score)
        system_prompt = "Act as a Sales Analyst and Lead Qualification Expert."
        reasoning_prompt = f"""Explain this lead score in VALID JSON format.

Lead Attributes:
- Budget: {budget}
- Timeline: {timeline}
- Urgency: {urgency}
- Calculated Score: {score}/100

Return ONLY valid JSON with this exact structure (no markdown wrapping, no extra text):
{{
    "lead_score": {score},
    "conversion_probability": "{conversion_probability}",
    "reasoning": "1-2 sentence explanation of why this score",
    "key_strengths": ["strength 1", "strength 2"],
    "risk_factors": ["risk 1", "risk 2"],
    "recommended_action": "specific next step to take",
    "sales_strategy": "how to approach this lead"
}}"""
        
        # Get AI reasoning
        ai_response = ai.call_llm_with_system_prompt(system_prompt, reasoning_prompt)
        
        # Return combined response
        return jsonify({
            'status': 'success',
            'data': ai_response.get('data', {
                'lead_score': score,
                'conversion_probability': conversion_probability,
                'reasoning': 'Lead scored based on budget, timeline, and urgency',
                'recommended_action': 'Schedule discovery call'
            })
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== SERVER STARTUP ====================

print("------------------------------------------------")
print(" SYSTEM CHECK: AI Business Growth Platform")
print("------------------------------------------------")

if __name__ == '__main__':
    print("1. Initializing AI Service...")
    print("2. Registering 6 AI Modules:")
    print("   ✓ Market Intelligence")
    print("   ✓ Smart Pricing Engine")
    print("   ✓ Compliance & Risk Monitoring")
    print("   ✓ 24/7 AI Chatbot")
    print("   ✓ Predictive Analytics")
    print("   ✓ Personalization Engine")
    print("3. Starting Flask server...")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    print("4. Server has stopped.")

    print("WARNING: app.py was imported, not run directly.")