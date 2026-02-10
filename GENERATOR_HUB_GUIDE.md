# MarketAI Suite - Generator Hub Documentation

## 🎯 Overview

The **Generator Hub** is a new advanced section of the MarketAI Suite containing 3 powerful AI-driven tools for marketing strategy, sales pitch generation, and lead scoring.

---

## 📱 Access the Generator Hub

Navigate to: **http://localhost:5000**

Tabs available:
- Original 9 modules (Campaign, Pitch, Score, Sentiment, Pricing, Compliance, Chatbot, Predict, Personalize)
- **NEW**: Gen Campaign, Gen Pitch, Gen Score

---

## 🚀 MODULE 1: AI MARKETING STRATEGIST

### Purpose
Generate comprehensive B2B marketing campaigns with targeted content, ad copy variations, and platform-specific CTAs using multi-shot prompting and structured JSON output.

### Endpoint
```
POST /api/generator/marketing-campaign
```

### Input Fields
- **Product Details** (Required)
  - Product features, benefits, pricing, target market, USP
  
- **LinkedIn Target Demographics** (Required)
  - Job titles, industries, company sizes, seniority, pain points, decision-making authority

### Output (JSON)
```json
{
  "campaign_objectives": [
    "objective 1",
    "objective 2",
    "objective 3"
  ],
  "content_ideas": [
    {
      "id": 1,
      "title": "content title",
      "format": "article/case study/infographic",
      "key_message": "main message",
      "engagement_angle": "why it matters to audience"
    }
    // ... 5 total ideas
  ],
  "ad_copy_variations": [
    {
      "variation": 1,
      "headline": "compelling headline",
      "body": "persuasive body copy",
      "tone": "professional/casual/urgent"
    }
    // ... 3 total variations
  ],
  "platform_specific_ctas": {
    "linkedin": "CTA optimized for LinkedIn",
    "email": "CTA optimized for Email",
    "web": "CTA optimized for Website"
  },
  "campaign_timeline": "suggested timeline in weeks",
  "expected_kpis": {
    "click_through_rate": "estimated %",
    "conversion_rate": "estimated %",
    "lead_quality_score": "1-10 scale"
  }
}
```

### Example Request
```javascript
fetch('/api/generator/marketing-campaign', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    product_details: "AI-powered email marketing platform. Automates campaign optimization, personalization, and A/B testing. Pricing: $99-$499/month based on volume.",
    linkedin_demographics: "Marketing managers and directors at B2B SaaS companies with 50-500 employees. Focus on revenue operations and marketing automation decision-makers."
  })
})
```

### Features
✓ 5 targeted content ideas with engagement angles
✓ 3 ad copy variations with different tones
✓ Platform-specific CTAs (LinkedIn, Email, Web)
✓ Campaign timeline and KPI projections
✓ Copyable ad copy and CTA buttons
✓ Shimmer loading animation while generating

---

## 🎤 MODULE 2: B2B SALES PITCH ARCHITECT

### Purpose
Create personalized sales pitches tailored to specific prospect roles and company tiers with discovery questions, objection handlers, and strategic CTAs using RAG principles.

### Endpoint
```
POST /api/generator/sales-pitch
```

### Input Fields
- **Prospect Title** (Required)
  - e.g., IT Director, VP of Operations, CFO, VP of Sales
  
- **Company Tier** (Required)
  - Fortune 500
  - Large Enterprise (1000+ employees)
  - Mid-Market (250-1000 employees)
  - Small Business (50-250 employees)
  - Startup (<50 employees)

- **Product/Service Info** (Optional)
  - Brief description of your solution

### Output (JSON)
```json
{
  "elevator_pitch_30sec": "A concise, compelling 30-second pitch",
  "pain_point_analysis": {
    "primary_pain": "main pain point for this role",
    "secondary_pains": [
      "pain point 2",
      "pain point 3"
    ]
  },
  "differentiators": [
    {
      "differentiator": "unique value proposition",
      "benefits_for_role": "specific benefits for prospect",
      "impact": "quantified business impact"
    }
    // ... 3 total differentiators
  ],
  "strategic_cta": {
    "immediate_next_step": "What to ask/do immediately",
    "suggested_angle": "How to position the next step",
    "objection_handler": "How to handle likely objections"
  },
  "discovery_questions": [
    "question 1 to ask prospect",
    "question 2 to ask prospect",
    "question 3 to ask prospect"
  ],
  "social_proof_angles": [
    "case study angle relevant to this prospect",
    "testimonial angle relevant to this prospect"
  ]
}
```

### Example Request
```javascript
fetch('/api/generator/sales-pitch', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prospect_title: "IT Director",
    company_tier: "Large Enterprise (1000+ employees)",
    product_info: "Cloud infrastructure automation platform"
  })
})
```

### Features
✓ Role-specific 30-second elevator pitch
✓ Pain point analysis for the prospect's role
✓ 3 tailored differentiators with impacts
✓ Discovery questions for deeper engagement
✓ Objection handlers
✓ Social proof angles (case studies, testimonials)
✓ Copy pitch and questions buttons
✓ Save to CRM functionality

---

## 📊 MODULE 3: INTELLIGENT LEAD SCORER

### Purpose
Intelligently score leads using a hybrid approach combining deterministic weighted algorithm with LLM-powered reasoning. Provides conversion probability and actionable sales strategy.

### Endpoint
```
POST /api/generator/lead-score
```

### Input Fields
- **Budget** (Required)
  - e.g., $50k, $250k, 1.5M
  
- **Timeline** (Required)
  - Immediate (This week)
  - This Month
  - This Quarter
  - This Year
  - Next Year or Later

- **Urgency Level** (Required)
  - Critical/High
  - Medium
  - Low

- **Additional Context** (Optional)
  - Industry, company growth, initiatives, etc.

### Scoring Algorithm
```
Lead Score = 
  (Budget Score × 0.40) + 
  (Timeline Score × 0.35) + 
  (Urgency Score × 0.25)

Budget Scoring:
  < $10k:   30 points
  $10k-$50k: 60 points
  > $50k:  100 points

Timeline Scoring:
  Immediate: 100 points
  This Month: 80 points
  This Quarter: 60 points
  This Year: 30 points
  Next Year+: 10 points

Urgency Scoring:
  Critical/High: 100 points
  Medium: 65 points
  Low: 30 points

Conversion Probability:
  80-100: 75% probability
  60-79: 50% probability
  40-59: 25% probability
  0-39: 10% probability
```

### Output (JSON)
```json
{
  "lead_score": 75,
  "conversion_probability": 50,
  "reasoning": "Strong budget and immediate timeline with medium urgency indicates qualified lead",
  "key_strengths": [
    "Adequate budget allocated",
    "Quick decision timeline"
  ],
  "risk_factors": [
    "Not highest urgency",
    "Need to confirm authority"
  ],
  "recommended_action": "Schedule discovery call within 48 hours",
  "sales_strategy": "Focus on ROI and implementation speed"
}
```

### Example Request
```javascript
fetch('/api/generator/lead-score', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    budget: "$150k",
    timeline: "This Quarter",
    urgency: "High",
    additional_context: "VP of Operations at fast-growing fintech startup, seeking operational efficiency"
  })
})
```

### Features
✓ Hybrid scoring algorithm (deterministic + LLM)
✓ Lead score display with color coding (Red/Yellow/Green)
✓ Conversion probability percentage
✓ Key strengths and risk factors
✓ Recommended next steps
✓ Sales strategy recommendations
✓ Copy next step and strategy buttons
✓ Add to pipeline functionality

---

## 🎨 UI/UX Features

### Consistent Design
✓ Dark SaaS theme matching existing platform
✓ Gradient buttons with hover effects
✓ Professional color scheme
✓ Responsive layout

### Loading Experience
✓ **Shimmer Loading Animation**: Custom CSS shimmer effect during AI generation
✓ Button text changes to "✨ Generating with AI..."
✓ Multiple shimmer lines show multiple outputs being generated
✓ Smooth transition from loading to results

### Result Display
✓ **Syntax-highlighted JSON**: Code block display with proper formatting
✓ **Action Buttons**: Context-specific buttons below results
  - Copy to clipboard
  - Export/Save functionality
  - CRM integration buttons
✓ **Responsive Output**: Scrollable containers for large responses

---

## 🔧 Technical Implementation

### Backend Stack
- **Framework**: Flask (Python)
- **AI/LLM**: Groq API (llama-3.3-70b-versatile)
- **Data Format**: JSON request/response

### Frontend Stack
- **HTML5**: Semantic form elements
- **CSS3**: Shimmer animations, gradients, responsive design
- **JavaScript**: Async/await, fetch API, clipboard integration

### API Response Handling
```javascript
// JSON parsing with error handling
try {
  const result = JSON.parse(response);
} catch (e) {
  // Fallback to raw response if JSON parsing fails
}

// Syntax highlighting with HTML escaping
const jsonString = JSON.stringify(data, null, 2);
output.innerHTML = `<pre>${escapeHtml(jsonString)}</pre>`;
```

---

## 📈 Use Cases

### Marketing Team
- **Scenario**: "Plan Q2 campaign for new AI product"
- **Action**: Use Marketing Strategist → Get 5 content ideas + 3 ad variations
- **Output**: Immediate campaign framework ready for execution

### Sales Development
- **Scenario**: "Qualify incoming leads from LinkedIn campaign"
- **Action**: Use Lead Scorer → Input lead attributes
- **Output**: Prioritized lead list with conversion probability

### Sales Executives
- **Scenario**: "Preparing for call with CTO at mid-market company"
- **Action**: Use Sales Pitch Architect → Input prospect details
- **Output**: Tailored pitch with discovery questions and objection handlers

---

## 🚀 Best Practices

### Marketing Strategist
1. Be specific about product USP
2. Detail actual target titles and pain points
3. Review generated content ideas for relevance
4. Use provided timeline as starting point (adjust as needed)

### Sales Pitch Architect
1. Select accurate prospect title and company tier
2. Include relevant product context if available
3. Customize the 30-sec pitch before using in call
4. Use discovery questions to open conversations
5. Reference objection handlers when needed

### Lead Scorer
1. Ensure budget information is accurate
2. Choose realistic timeline for prospect
3. Add context about company if available
4. Use "Recommended Action" as guidance
5. Monitor conversion rates (validate accuracy)

---

## 📊 API Reference

### Health Check
```
GET /api/health
Returns: { "status": "healthy", "message": "..." }
```

### Marketing Campaign Generator
```
POST /api/generator/marketing-campaign
Required: product_details, linkedin_demographics
Returns: Structured campaign with objectives, content, ad copy, CTAs
```

### Sales Pitch Generator
```
POST /api/generator/sales-pitch
Required: prospect_title, company_tier
Optional: product_info
Returns: Personalized pitch with discovery questions and objection handlers
```

### Lead Scorer
```
POST /api/generator/lead-score
Required: budget, timeline, urgency
Optional: additional_context
Returns: Lead score (0-100), conversion probability, reasoning, strategy
```

---

## ✅ Quality Assurance Checklist

- ✓ All endpoints properly validated
- ✓ Error handling on all inputs
- ✓ JSON parsing with fallbacks
- ✓ Responsive design on mobile/tablet
- ✓ Shimmer loading smooth and performant
- ✓ Clipboard copy functionality tested
- ✓ No hardcoded values in prompts (all parameterized)
- ✓ Output formatting consistent across all modules
- ✓ Button labels clear and actionable
- ✓ Loading states provide feedback

---

## 🔐 Security Notes

- All user input validated server-side
- XSS protection via HTML escaping
- CORS enabled appropriately
- API key protected in .env
- No sensitive data logged
- JSON parsing errors handled gracefully

---

## 📝 Future Enhancements

- Multi-language support
- A/B testing integration
- CRM API connections (Salesforce, HubSpot)
- Historical lead scoring comparison
- Campaign performance tracking dashboard
- Advanced analytics and reporting
- Export to CSV/PDF formats
- Collaborative campaign planning

---

Generated: February 10, 2026
Version: MarketAI Suite 3.0 with Generator Hub
