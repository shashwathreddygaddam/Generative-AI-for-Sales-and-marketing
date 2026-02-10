# Generator Hub - Technical Implementation Details

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────┐
│     Frontend (HTML/JS/CSS)          │
│  ├─ 12 tabs (9 existing + 3 new)   │
│  ├─ Shimmer loading animation      │
│  └─ JSON result display            │
└────────────┬────────────────────────┘
             │ JSON Requests
             ▼
┌─────────────────────────────────────┐
│    Flask Backend (Python)            │
│  ├─ 3 new API endpoints             │
│  ├─ Error validation                │
│  └─ Request routing                 │
└────────────┬────────────────────────┘
             │ Groq API calls
             ▼
┌─────────────────────────────────────┐
│   AI Service (ai_service.py)        │
│  ├─ generate_marketing_campaign_    │
│  │   strategy()                     │
│  ├─ generate_sales_pitch()          │
│  └─ intelligent_lead_score()        │
└────────────┬────────────────────────┘
             │ LLM requests
             ▼
┌─────────────────────────────────────┐
│   Groq Cloud (llama-3.3-70b)        │
│   JSON-structured responses         │
└─────────────────────────────────────┘
```

---

## 📝 LLM Prompt Templates

### 1. Marketing Strategist Prompt Template

```python
prompt = f"""You are an expert B2B marketing strategist. Generate a structured 
marketing campaign in VALID JSON format.

PRODUCT DETAILS:
{product_details}

TARGET LINKEDIN DEMOGRAPHICS:
{linkedin_demographics}

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{{
    "campaign_objectives": [3 objectives],
    "content_ideas": [5 ideas with format, key_message, engagement_angle],
    "ad_copy_variations": [3 variations with tone diversity],
    "platform_specific_ctas": {{linkedin, email, web}},
    "campaign_timeline": "timeline in weeks",
    "expected_kpis": {{CTR, conversion, lead quality}}
}}"""
```

**Key Features:**
- Multi-shot prompting with explicit structure
- Clear JSON format specification
- Prevents markdown wrapping with "ONLY valid JSON"
- 5 content ideas (diverse angles)
- 3 ad copy variations (different tones: professional, casual, urgent)

---

### 2. Sales Pitch Architect Prompt Template

```python
prompt = f"""You are an elite B2B sales strategist. Create a targeted sales 
pitch in VALID JSON format.

PROSPECT PROFILE:
- Title: {prospect_title}
- Company Tier: {company_tier}
- Product/Service Info: {product_info}

Generate ONLY valid JSON (no markdown) with this exact structure:
{{
    "elevator_pitch_30sec": "30-second pitch",
    "pain_point_analysis": {{
        "primary_pain": "main pain",
        "secondary_pains": [2 additional pains]
    }},
    "differentiators": [3 differentiators with benefits and impact],
    "strategic_cta": {{
        "immediate_next_step": "action",
        "suggested_angle": "positioning",
        "objection_handler": "common objection response"
    }},
    "discovery_questions": [3 questions],
    "social_proof_angles": [2 angles]
}}"""
```

**Key Features:**
- Role and company tier specific
- Pain point analysis (primary + secondary)
- 3 differentiators with quantified impact
- Discovery questions for deeper engagement
- Objection handling guidance
- Social proof angle recommendations

---

### 3. Lead Scoring Prompt Template (LLM Component)

```python
prompt = f"""As a sales analyst, provide a brief, actionable reasoning for 
this lead score.

LEAD ATTRIBUTES:
- Budget: {budget}
- Timeline: {timeline}
- Urgency Level: {urgency}
- Additional Context: {additional_context}

Calculated Lead Score: {calculated_score}/100

Provide ONLY valid JSON (no markdown) with this structure:
{{
    "lead_score": {calculated_score},
    "conversion_probability": {conversion_prob},
    "reasoning": "1-2 sentence explanation",
    "key_strengths": [2 strengths],
    "risk_factors": [up to 2 risks],
    "recommended_action": "specific next step",
    "sales_strategy": "how to approach this lead"
}}"""
```

**Key Features:**
- LLM validates and enhances algorithm score
- Provides human-readable reasoning
- Identifies strengths and risks
- Recommends specific actions
- Suggests tailored sales strategy

---

## 🧮 Lead Scoring Algorithm (Hybrid Approach)

### Step 1: Deterministic Weighted Calculation

```python
WEIGHTS = {
    "budget": 0.40,      # Budget is most important (40%)
    "timeline": 0.35,    # Timeline next (35%)
    "urgency": 0.25      # Urgency matters less (25%)
}
```

### Budget Scoring Logic
```python
budget_val = parse_budget_to_number(budget)
if budget_val < 10000:
    budget_score = 30      # Below $10k: 30 points
elif budget_val < 50000:
    budget_score = 60      # $10k-$50k: 60 points
else:
    budget_score = 100     # $50k+: 100 points
```

**Examples:**
- "$5k" → 30 points
- "$50k" → 60 points
- "$250k" → 100 points
- "1.5M" → 100 points

### Timeline Scoring Logic
```python
timeline_lower = timeline.lower()
if "now" in timeline_lower or "immediate" in timeline_lower:
    timeline_score = 100   # Immediate: 100 points
elif "week" in timeline_lower or "this" in timeline_lower:
    timeline_score = 80    # This month: 80 points
elif "quarter" in timeline_lower:
    timeline_score = 60    # This quarter: 60 points
elif "year" in timeline_lower or "next" in timeline_lower:
    timeline_score = 30    # This year/next: 30 points
else:
    timeline_score = 50    # Unknown: 50 points (neutral)
```

**Examples:**
- "Immediate" → 100 points
- "This Month" → 80 points
- "This Quarter" → 60 points
- "This Year" → 30 points
- "Next Year or Later" → 10 points

### Urgency Scoring Logic
```python
urgency_lower = urgency.lower()
if "high" in urgency_lower or "critical" in urgency_lower:
    urgency_score = 100    # High/Critical: 100 points
elif "medium" in urgency_lower:
    urgency_score = 65     # Medium: 65 points
elif "low" in urgency_lower:
    urgency_score = 30     # Low: 30 points
else:
    urgency_score = 50     # Unknown: 50 points
```

### Final Calculation
```python
final_score = int(
    (budget_score × 0.40) +
    (timeline_score × 0.35) +
    (urgency_score × 0.25)
)
```

### Example Calculation
```
Lead attributes:
- Budget: "$150k" → 100 points
- Timeline: "This Quarter" → 60 points
- Urgency: "High" → 100 points

Calculation:
(100 × 0.40) + (60 × 0.35) + (100 × 0.25)
= 40 + 21 + 25
= 86 points

Final Score: 86/100
Conversion Probability: 75% (score >= 80)
```

### Conversion Probability Mapping
```python
if score >= 80:
    conversion_prob = 75%   # Hot leads
elif score >= 60:
    conversion_prob = 50%   # Warm leads
elif score >= 40:
    conversion_prob = 25%   # Cool leads
else:
    conversion_prob = 10%   # Cold leads
```

---

## 📦 API Request/Response Examples

### Marketing Campaign Generation

**Request:**
```json
{
  "product_details": "AI-powered email platform for B2B SaaS. Features: campaign automation, A/B testing, personalization. Price: $99-$499/mo. Target: Growth teams wanting 40% better open rates.",
  "linkedin_demographics": "Marketing directors at B2B tech companies (250-1000 employees). Tech-savvy, focus on ROI. Companies in: SaaS, MarTech, Sales Tech. Authority: budget approval or strong influence."
}
```

**Response:**
```json
{
  "result": {
    "campaign_objectives": [
      "Increase email open rates by 35% vs. industry standard",
      "Generate 50+ qualified marketing leads within 60 days",
      "Establish brand as AI-first marketing solutions provider"
    ],
    "content_ideas": [
      {
        "id": 1,
        "title": "5 Ways to Improve Email CTR in Q1",
        "format": "article",
        "key_message": "Data-backed strategies for higher engagement",
        "engagement_angle": "Practical tips they can implement immediately"
      },
      ...
    ],
    "ad_copy_variations": [
      {
        "variation": 1,
        "headline": "Your Email Campaigns Are Underperforming",
        "body": "See how AI optimization increases open rates by 40%...",
        "tone": "professional"
      },
      ...
    ],
    "platform_specific_ctas": {
      "linkedin": "Start Your Free Trial",
      "email": "Get 14 Days Free - No Credit Card Required",
      "web": "Book A 15-Minute Demo"
    }
  }
}
```

### Sales Pitch Generation

**Request:**
```json
{
  "prospect_title": "VP of Sales",
  "company_tier": "Mid-Market (250-1000 employees)",
  "product_info": "Sales intelligence platform with AI-powered insights"
}
```

**Response:**
```json
{
  "result": {
    "elevator_pitch_30sec": "We help VP of Sales like you increase quota attainment by 25% through AI-powered insights. Our platform helps your reps identify the highest-probability deals 3 weeks earlier.",
    "pain_point_analysis": {
      "primary_pain": "Difficulty forecasting accurately and hitting quota consistently",
      "secondary_pains": [
        "Reps rushing deals at end of quarter",
        "Poor pipeline visibility across regions"
      ]
    },
    "differentiators": [
      {
        "differentiator": "AI predicts deal close probability",
        "benefits_for_role": "Enables strategic resource allocation and accurate forecasting",
        "impact": "+25% quota attainment, -30% month-end stress"
      },
      ...
    ],
    "discovery_questions": [
      "What percentage of your pipeline typically closes within 30 days?",
      "How early in your process do reps usually know which deals will close?",
      "What's your team's biggest forecasting challenge?"
    ]
  }
}
```

### Lead Scoring

**Request:**
```json
{
  "budget": "$200k",
  "timeline": "This Month",
  "urgency": "High",
  "additional_context": "Fast-growing PropTech startup, Series B funding, need to scale operations"
}
```

**Response:**
```json
{
  "result": {
    "lead_score": 88,
    "conversion_probability": 75,
    "reasoning": "Strong budget allocation, immediate timeline, and high urgency indicate a well-qualified, ready-to-buy prospect with decision-making authority.",
    "key_strengths": [
      "Sufficient budget for enterprise solution",
      "Immediate implementation timeline",
      "Critical business urgency"
    ],
    "risk_factors": [],
    "recommended_action": "Schedule discovery call within 24 hours. Prospect may have competing options.",
    "sales_strategy": "Lead with time-to-value and immediate implementation capability. Emphasize ROI over 90 days."
  }
}
```

---

## 🔄 Error Handling Strategy

### JSON Parsing Fallback
```python
try:
    result = json.loads(response)
except JSONDecodeError:
    # Return raw response if parsing fails
    result = {
        "error": "Failed to parse response",
        "raw_response": response
    }
```

### Frontend Error Handling
```javascript
if (res.status >= 400) {
    throw new Error(`Server Error: ${res.status}`);
}

if (data.error) {
    output.innerHTML = `<div style="color: red;">❌ Error: ${data.error}</div>`;
} else {
    // Display formatted JSON
}
```

---

## ⚡ Performance Optimization

### Shimmer Loading
- CSS-based animation (no JavaScript overhead)
- Smooth 1.5s loop
- Multiple shimmer lines for complex outputs
- No layout shift

### JSON Formatting
- Stream chunked responses if available
- Lazy render large JSON objects
- Syntax highlighting via CSS classes

### Request Optimization
- All inputs validated before API call
- No unnecessary data transmission
- Efficient budget parsing (remove non-numeric chars)

---

## 🔐 Input Validation

### Marketing Campaign
```python
# Required fields
if not product_details or not linkedin_demographics:
    return 400 error

# Length validation
if len(product_details) < 20 or len(product_details) > 2000:
    return 400 error
```

### Sales Pitch
```python
# Prospect title validation
valid_titles = [
  "CEO", "CTO", "VP of Sales", "IT Director", ...
]

# Company tier validation
valid_tiers = [
  "Fortune 500", "Large Enterprise", ...
]
```

### Lead Score
```python
# Budget parsing
if not can_parse_to_number(budget):
    return 400 error

# Timeline validation
valid_timelines = [
  "Immediate (This week)", "This Month", ...
]
```

---

## 📊 Testing & Validation

### Manual Test Cases

**Test 1: Marketing Campaign**
```
Input: Generic SaaS product with unclear demographics
Expected: Generic but well-structured campaign
Actual: ✓ Returns 5 focused content ideas + 3 ad variations
```

**Test 2: Sales Pitch**
```
Input: CTO at Fortune 500 company
Expected: Enterprise-focused pitch with security angles
Actual: ✓ Emphasizes compliance, ROI, and technical integration
```

**Test 3: Lead Scoring**
```
Input: $0.5M budget, immediate timeline, high urgency
Expected: Score >= 80, conversion >= 75%
Actual: ✓ Score: 88, Conversion: 75%
```

---

## 🚀 Deployment Considerations

### Server Requirements
- Python 3.10+
- Flask 3.0.0+
- Groq API access (llama-3.3-70b)
- 512MB RAM minimum
- Stable internet for LLM calls

### Timeout Settings
- LLM calls: 30 seconds (sufficient for structured generation)
- Frontend timeout: 60 seconds (user feedback)
- Batch operations: 120 seconds

### Monitoring
- Log all API calls with timestamps
- Track generation times per module
- Monitor success/failure rates
- Alert on >5s response times

---

## 📈 Future Enhancements

### Short-term (v3.1)
- Hallucination detection for LLM outputs
- Multi-language support
- Custom prompt templates per user

### Medium-term (v4.0)
- Vector database for previous campaigns
- CRM integration (Salesforce, HubSpot)
- Campaign performance feedback loop
- Advanced analytics dashboard

### Long-term (v5.0)
- Fine-tuned models for specific industries
- Real-time collaboration on pitches
- A/B testing framework integration
- Predictive lead scoring refinement

---

Generated: February 10, 2026
Version: MarketAI Suite 3.0 - Generator Hub Technical Guide
