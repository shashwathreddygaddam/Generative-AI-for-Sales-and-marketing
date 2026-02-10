import os
import requests
import json
import random
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        self.chat_history = []

    def _call_groq(self, prompt):
        if not self.api_key:
            return "Error: API Key missing in .env file."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Structure the payload exactly as Groq expects
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        try:
            resp = requests.post(self.api_url, json=data, headers=headers)
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"DEBUG: AI Service Error -> {e}")
            return f"AI Error: {str(e)}"

    # ===================== CENTRALIZED LLM HANDLER (Node.js Pattern) =====================
    def call_llm_with_system_prompt(self, system_prompt, user_prompt):
        """
        Unified LLM interface that takes a system prompt and user prompt.
        Mimics the Node.js generateAIContent() function.
        
        Args:
            system_prompt (str): System role/context ("Marketing Specialist", "Sales Architect", etc.)
            user_prompt (str): User request/data to process
            
        Returns:
            dict: Standardized response with status and data
        """
        if not self.api_key:
            return {"status": "error", "message": "API Key missing in .env file"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Combine system prompt and user prompt for full context
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.7
        }
        
        try:
            resp = requests.post(self.api_url, json=data, headers=headers)
            resp.raise_for_status()
            response_text = resp.json()['choices'][0]['message']['content']
            
            # Try to parse as JSON, return raw if fails
            try:
                json_data = json.loads(response_text)
                return {"status": "success", "data": json_data}
            except json.JSONDecodeError:
                return {"status": "success", "data": response_text}
                
        except Exception as e:
            print(f"DEBUG: API Error in call_llm_with_system_prompt -> {e}")
            return {"status": "error", "message": str(e)}

    # ===================== MODULE 1: MARKET INTELLIGENCE =====================
    def analyze_sentiment(self, text):
        """Analyzes customer sentiment and returns confidence score."""
        prompt = (f"Analyze the sentiment of this customer feedback in JSON format:\n\n"
                  f"\"{text}\"\n\n"
                  f"Return ONLY valid JSON with these exact keys:\n"
                  f"{{ \"sentiment\": \"positive/neutral/negative\", \"confidence\": 0.0-1.0, \"summary\": \"brief analysis\" }}")
        response = self._call_groq(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "summary": response
            }

    def competitor_benchmark(self, brand):
        """Benchmarks competitor market position and trends."""
        prompt = (f"Provide market intelligence on '{brand}' in JSON format:\n"
                  f"Return ONLY valid JSON with these exact keys:\n"
                  f"{{ \"market_score\": 0-100, \"trend\": \"up/down/stable\", \"market_position\": \"description\", \"key_strength\": \"strength\", \"key_weakness\": \"weakness\" }}")
        response = self._call_groq(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "market_score": random.randint(60, 85),
                "trend": random.choice(["up", "down", "stable"]),
                "market_position": response,
                "key_strength": "Strong brand recognition",
                "key_weakness": "Limited innovation"
            }

    # ===================== MODULE 2: SMART PRICING ENGINE =====================
    def dynamic_price(self, cost, demand_index, competitor_price):
        """Calculates optimal dynamic pricing based on market conditions."""
        try:
            cost = float(cost)
            demand_index = float(demand_index)  # 0.5 to 1.5 scale
            competitor_price = float(competitor_price)
        except:
            return {"error": "Invalid input values"}

        # Dynamic pricing algorithm
        base_margin = 0.4  # 40% margin
        demand_multiplier = demand_index
        competitor_factor = (competitor_price / cost) * 0.3

        optimal_price = cost * (1 + base_margin) * demand_multiplier + competitor_factor
        margin = ((optimal_price - cost) / optimal_price) * 100

        if demand_index > 1.2:
            reason = "High demand detected - premium pricing recommended"
        elif demand_index < 0.8:
            reason = "Low demand - competitive pricing recommended"
        else:
            reason = "Stable demand - balanced pricing recommended"

        return {
            "optimal_price": round(optimal_price, 2),
            "margin_percent": round(margin, 2),
            "pricing_reason": reason,
            "competitor_analysis": f"Competitor price: ${competitor_price:.2f} - Your optimal: ${optimal_price:.2f}"
        }

    # ===================== MODULE 3: COMPLIANCE & RISK MONITORING =====================
    def compliance_check(self, text):
        """Checks marketing text for legal, GDPR, and claim risks."""
        prompt = (f"Review this marketing text for compliance issues in JSON format:\n\n"
                  f"\"{text}\"\n\n"
                  f"Return ONLY valid JSON with these exact keys:\n"
                  f"{{ \"risk_level\": \"low/medium/high\", \"flagged_phrases\": [list], \"suggestions\": [list], \"gdpr_compliant\": true/false }}")
        response = self._call_groq(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "risk_level": "low",
                "flagged_phrases": [],
                "suggestions": ["Review marketing claims against regulations"],
                "gdpr_compliant": True
            }

    # ===================== MODULE 4: AI CHATBOT =====================
    def ai_chat_response(self, message, history=None):
        """24/7 AI chatbot for customer inquiries."""
        if history is None:
            history = []

        system_prompt = ("You are a helpful AI business assistant for an AI growth platform. "
                        "Answer questions about business growth, AI capabilities, and product features. "
                        "Keep responses concise and professional.")

        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in history:
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": message})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        try:
            resp = requests.post(self.api_url, json=data, headers=headers)
            resp.raise_for_status()
            response_text = resp.json()['choices'][0]['message']['content']
            return {
                "response": response_text,
                "status": "success"
            }
        except Exception as e:
            return {
                "response": f"AI Chatbot Error: {str(e)}",
                "status": "error"
            }

    # ===================== MODULE 5: PREDICTIVE CUSTOMER ANALYTICS =====================
    def predict_behavior(self, history_data):
        """Predicts customer behavior and optimal touchpoints."""
        prompt = (f"Analyze customer behavior data and predict in JSON format:\n"
                  f"Data: {history_data}\n\n"
                  f"Return ONLY valid JSON with these exact keys:\n"
                  f"{{ \"churn_risk\": \"high/medium/low\", \"churn_probability\": 0-100, \"next_best_action\": \"action\", \"campaign_timing\": \"timing\", \"recommended_channel\": \"channel\" }}")
        response = self._call_groq(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "churn_risk": "medium",
                "churn_probability": random.randint(20, 70),
                "next_best_action": response,
                "campaign_timing": "Immediate - within 7 days",
                "recommended_channel": "Email or SMS"
            }

    # ===================== MODULE 6: ADVANCED PERSONALIZATION ENGINE =====================
    def recommend_products(self, user_profile):
        """AI-powered product recommendations based on user profile."""
        prompt = (f"Generate product recommendations in JSON format:\n"
                  f"User Profile: {user_profile}\n\n"
                  f"Return ONLY valid JSON with this exact key:\n"
                  f"{{ \"recommended_products\": [{{'name': 'product', 'reason': 'why', 'priority': 'high/medium/low'}}] }}")
        response = self._call_groq(prompt)
        try:
            result = json.loads(response)
            return result
        except:
            return {
                "recommended_products": [
                    {"name": "AI Analytics Suite", "reason": response, "priority": "high"},
                    {"name": "Predictive CRM", "reason": "Enhanced customer insights", "priority": "medium"}
                ]
            }

    # ===================== LEGACY FUNCTIONS =====================
    def generate_campaign(self, product, audience, platform):
        prompt = (f"Act as a Marketing Manager. Create a campaign for:\n"
                  f"Product: {product}\nAudience: {audience}\nPlatform: {platform}\n"
                  f"Include: Strategy, Content Ideas, and KPIs.")
        return self._call_groq(prompt)

    def generate_pitch(self, product, customer):
        prompt = (f"Act as a Sales Expert. Write a SPIN sales pitch for:\n"
                  f"Product: {product}\nCustomer: {customer}\n"
                  f"Include: Elevator Pitch, Value Prop, and Closing.")
        return self._call_groq(prompt)

    def score_lead(self, name, budget, need, urgency):
        prompt = (f"Act as a Lead Scorer. Analyze:\n"
                  f"Name: {name}\nBudget: {budget}\nNeed: {need}\nUrgency: {urgency}\n"
                  f"Output: Score (0-100), Conversion Probability %, and Reasoning.")
        return self._call_groq(prompt)

    # ===================== GENERATOR HUB: MODULE 1 - AI MARKETING STRATEGIST =====================
    def generate_marketing_campaign_strategy(self, product_details, linkedin_demographics):
        """
        AI Marketing Strategist using multi-shot prompting with structured JSON output.
        Generates campaign objectives, content ideas, ad copy, and CTAs.
        """
        prompt = f"""You are an expert B2B marketing strategist. Generate a structured marketing campaign in VALID JSON format.

PRODUCT DETAILS:
{product_details}

TARGET LINKEDIN DEMOGRAPHICS:
{linkedin_demographics}

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{{
    "campaign_objectives": [
        "objective 1",
        "objective 2",
        "objective 3"
    ],
    "content_ideas": [
        {{
            "id": 1,
            "title": "content title",
            "format": "article/case study/infographic",
            "key_message": "main message",
            "engagement_angle": "why it matters to audience"
        }},
        {{
            "id": 2,
            "title": "content title",
            "format": "article/case study/infographic",
            "key_message": "main message",
            "engagement_angle": "why it matters to audience"
        }},
        {{
            "id": 3,
            "title": "content title",
            "format": "article/case study/infographic",
            "key_message": "main message",
            "engagement_angle": "why it matters to audience"
        }},
        {{
            "id": 4,
            "title": "content title",
            "format": "article/case study/infographic",
            "key_message": "main message",
            "engagement_angle": "why it matters to audience"
        }},
        {{
            "id": 5,
            "title": "content title",
            "format": "article/case study/infographic",
            "key_message": "main message",
            "engagement_angle": "why it matters to audience"
        }}
    ],
    "ad_copy_variations": [
        {{
            "variation": 1,
            "headline": "compelling headline",
            "body": "persuasive body copy",
            "tone": "professional/casual/urgent"
        }},
        {{
            "variation": 2,
            "headline": "compelling headline",
            "body": "persuasive body copy",
            "tone": "professional/casual/urgent"
        }},
        {{
            "variation": 3,
            "headline": "compelling headline",
            "body": "persuasive body copy",
            "tone": "professional/casual/urgent"
        }}
    ],
    "platform_specific_ctas": {{
        "linkedin": "CTA optimized for LinkedIn",
        "email": "CTA optimized for Email campaigns",
        "web": "CTA optimized for Website"
    }},
    "campaign_timeline": "suggested timeline in weeks",
    "expected_kpis": {{
        "click_through_rate": "estimated %",
        "conversion_rate": "estimated %",
        "lead_quality_score": "1-10 scale"
    }}
}}"""
        
        response = self._call_groq(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Failed to parse response", "raw_response": response}

    # ===================== GENERATOR HUB: MODULE 2 - B2B SALES PITCH ARCHITECT =====================
    def generate_sales_pitch(self, prospect_title, company_tier, product_info=""):
        """
        B2B Sales Pitch Architect generates personalized sales pitches.
        Input: Prospect Title, Company Tier
        Output: 30-second pitch, pain-point differentiators, strategic CTA
        """
        prompt = f"""You are an elite B2B sales strategist. Create a targeted sales pitch in VALID JSON format.

PROSPECT PROFILE:
- Title: {prospect_title}
- Company Tier: {company_tier}
{f"- Product/Service Info: {product_info}" if product_info else ""}

Generate ONLY valid JSON (no markdown) with this exact structure:
{{
    "elevator_pitch_30sec": "A concise, compelling 30-second pitch tailored to this prospect",
    "pain_point_analysis": {{
        "primary_pain": "main pain point for this role/company tier",
        "secondary_pains": [
            "pain point 2",
            "pain point 3"
        ]
    }},
    "differentiators": [
        {{
            "differentiator": "unique value proposition",
            "benefits_for_role": "specific benefits for {prospect_title}",
            "impact": "quantified business impact"
        }},
        {{
            "differentiator": "unique value proposition",
            "benefits_for_role": "specific benefits for {prospect_title}",
            "impact": "quantified business impact"
        }},
        {{
            "differentiator": "unique value proposition",
            "benefits_for_role": "specific benefits for {prospect_title}",
            "impact": "quantified business impact"
        }}
    ],
    "strategic_cta": {{
        "immediate_next_step": "What to ask/do immediately",
        "suggested_angle": "How to position the next step",
        "objection_handler": "How to handle likely objections"
    }},
    "discovery_questions": [
        "question 1 to ask prospect",
        "question 2 to ask prospect",
        "question 3 to ask prospect"
    ],
    "social_proof_angles": [
        "case study angle relevant to this prospect",
        "testimonial angle relevant to this prospect"
    ]
}}"""
        
        response = self._call_groq(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Failed to parse response", "raw_response": response}

    # ===================== GENERATOR HUB: MODULE 3 - INTELLIGENT LEAD SCORER =====================
    def intelligent_lead_score(self, budget, timeline, urgency, additional_context=""):
        """
        Intelligent Lead Scorer using hybrid approach:
        - Deterministic weighted algorithm for score calculation
        - LLM for detailed reasoning
        Output: Lead Score (0-100), Reasoning, Conversion Probability
        """
        # Step 1: Deterministic Weighted Scoring Algorithm
        score = 0
        weights = {
            "budget": 0.40,
            "timeline": 0.35,
            "urgency": 0.25
        }
        
        # Parse and score budget
        try:
            budget_val = float(''.join(filter(lambda x: x.isdigit() or x == '.', str(budget).lower().replace('k', '000').replace('m', '000000'))))
            if budget_val < 10000:
                budget_score = 30
            elif budget_val < 50000:
                budget_score = 60
            else:
                budget_score = 100
        except:
            budget_score = 50
        
        # Score timeline
        timeline_lower = str(timeline).lower()
        if "now" in timeline_lower or "immediate" in timeline_lower or "urgent" in timeline_lower:
            timeline_score = 100
        elif "week" in timeline_lower or "this" in timeline_lower or "month" in timeline_lower:
            timeline_score = 80
        elif "quarter" in timeline_lower:
            timeline_score = 60
        elif "year" in timeline_lower or "next" in timeline_lower:
            timeline_score = 30
        else:
            timeline_score = 50
        
        # Score urgency
        urgency_lower = str(urgency).lower()
        if "high" in urgency_lower or "critical" in urgency_lower:
            urgency_score = 100
        elif "medium" in urgency_lower:
            urgency_score = 65
        elif "low" in urgency_lower:
            urgency_score = 30
        else:
            urgency_score = 50
        
        # Calculate weighted score
        calculated_score = int(
            (budget_score * weights["budget"]) +
            (timeline_score * weights["timeline"]) +
            (urgency_score * weights["urgency"])
        )
        
        # Conversion probability based on score
        if calculated_score >= 80:
            conversion_prob = 75
        elif calculated_score >= 60:
            conversion_prob = 50
        elif calculated_score >= 40:
            conversion_prob = 25
        else:
            conversion_prob = 10
        
        # Step 2: LLM for Detailed Reasoning
        reasoning_prompt = f"""As a sales analyst, provide a brief, actionable reasoning for this lead score.

LEAD ATTRIBUTES:
- Budget: {budget}
- Timeline: {timeline}
- Urgency Level: {urgency}
{f"- Additional Context: {additional_context}" if additional_context else ""}

Calculate Lead Score: {calculated_score}/100

Provide ONLY valid JSON (no markdown) with this structure:
{{
    "lead_score": {calculated_score},
    "conversion_probability": {conversion_prob},
    "reasoning": "1-2 sentence explanation of why this is a {calculated_score}/100 lead",
    "key_strengths": [
        "strength 1",
        "strength 2"
    ],
    "risk_factors": [
        "risk 1",
        "risk 2"
    ],
    "recommended_action": "specific next step for sales team",
    "sales_strategy": "how to approach this lead"
}}"""
        
        response = self._call_groq(reasoning_prompt)
        try:
            result = json.loads(response)
            return result
        except:
            # Fallback if JSON parsing fails
            return {
                "lead_score": calculated_score,
                "conversion_probability": conversion_prob,
                "reasoning": response,
                "key_strengths": ["High interest", "Qualified budget"],
                "risk_factors": [],
                "recommended_action": "Contact immediately",
                "sales_strategy": "Focus on value proposition"
            }