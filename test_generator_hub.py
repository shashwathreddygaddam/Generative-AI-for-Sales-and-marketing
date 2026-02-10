import requests
import json

print("Testing Generator Hub Endpoints...")
print("=" * 70)

# Test 1: Marketing Campaign
print("\n[TEST 1] /api/generator/marketing-campaign")
payload1 = {
    "product_details": "AI email marketing platform with subject line optimization and 40% better open rates. Price: $99-$499/month for B2B SaaS teams.",
    "linkedin_demographics": "Marketing directors at B2B SaaS (250-1000 employees), budget approval authority, focus on ROI"
}

try:
    resp = requests.post("http://localhost:5000/api/generator/marketing-campaign", json=payload1, timeout=60)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
    elif 'result' in data:
        result = data['result']
        if isinstance(result, dict):
            print(f"✓ Campaign objectives: {len(result.get('campaign_objectives', []))} items")
            print(f"✓ Content ideas: {len(result.get('content_ideas', []))} items")
            print(f"✓ Ad variations: {len(result.get('ad_copy_variations', []))} items")
        else:
            print(f"✓ Raw response: {str(result)[:100]}...")
except Exception as e:
    print(f"❌ Connection Error: {e}")

# Test 2: Sales Pitch
print("\n[TEST 2] /api/generator/sales-pitch")
payload2 = {
    "prospect_title": "VP of Sales",
    "company_tier": "Mid-Market (250-1000 employees)",
    "product_info": "Sales intelligence platform"
}

try:
    resp = requests.post("http://localhost:5000/api/generator/sales-pitch", json=payload2, timeout=60)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
    elif 'result' in data:
        result = data['result']
        if isinstance(result, dict):
            print(f"✓ Elevator pitch: {bool(result.get('elevator_pitch_30sec'))}")
            print(f"✓ Differentiators: {len(result.get('differentiators', []))} items")
            print(f"✓ Discovery questions: {len(result.get('discovery_questions', []))} items")
        else:
            print(f"✓ Raw response: {str(result)[:100]}...")
except Exception as e:
    print(f"❌ Connection Error: {e}")

# Test 3: Lead Score
print("\n[TEST 3] /api/generator/lead-score")
payload3 = {
    "budget": "$250000",
    "timeline": "This Quarter",
    "urgency": "Critical/High",
    "additional_context": "Series B funded startup"
}

try:
    resp = requests.post("http://localhost:5000/api/generator/lead-score", json=payload3, timeout=60)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
    elif 'result' in data:
        result = data['result']
        if isinstance(result, dict):
            print(f"✓ Lead score: {result.get('lead_score', 'N/A')}/100")
            print(f"✓ Conversion probability: {result.get('conversion_probability', 'N/A')}")
            print(f"✓ Reasoning: {str(result.get('reasoning', 'N/A'))[:60]}...")
        else:
            print(f"✓ Raw response: {str(result)[:100]}...")
except Exception as e:
    print(f"❌ Connection Error: {e}")

print("\n" + "=" * 70)
print("Generator Hub Backend Test Complete")
