import requests
import json

print("=" * 70)
print("DETAILED GENERATOR HUB ENDPOINT TEST")
print("=" * 70)

# Test 1: Marketing Campaign  
print("\n[TEST 1] /api/generator/marketing-campaign")
payload1 = {
    "product_details": "AI email marketing platform with subject line optimization and 40% better open rates. Price: $99-$499/month.",
    "linkedin_demographics": "Marketing directors at B2B SaaS"
}

try:
    resp = requests.post("http://localhost:5000/api/generator/marketing-campaign", json=payload1, timeout=60)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Full Response:\n{json.dumps(data, indent=2)}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "-" * 70)

# Test 2: Sales Pitch
print("\n[TEST 2] /api/generator/sales-pitch")
payload2 = {
    "prospect_title": "VP of Sales",
    "company_tier": "Mid-Market (250-1000 employees)"
}

try:
    resp = requests.post("http://localhost:5000/api/generator/sales-pitch", json=payload2, timeout=60)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Full Response:\n{json.dumps(data, indent=2)[:500]}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "-" * 70)

# Test 3: Lead Score
print("\n[TEST 3] /api/generator/lead-score")
payload3 = {
    "budget": "$250000",
    "timeline": "This Quarter",
    "urgency": "Critical/High"
}

try:
    resp = requests.post("http://localhost:5000/api/generator/lead-score", json=payload3, timeout=60)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Full Response:\n{json.dumps(data, indent=2)[:500]}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
