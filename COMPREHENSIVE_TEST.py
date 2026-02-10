"""
COMPREHENSIVE GENERATOR HUB VALIDATION TEST
Testing all three modules with detailed output verification
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_marketing_campaign():
    print_section("TEST 1: AI MARKETING STRATEGIST")
    
    payload = {
        "product_details": "AI email marketing platform with subject line optimization and 40% better open rates. Price: $99-$499/month for B2B SaaS teams.",
        "linkedin_demographics": "Marketing directors at B2B SaaS companies (250-1000 employees), budget approval authority, focus on ROI metrics"
    }
    
    print(f"Endpoint: POST {BASE_URL}/api/generator/marketing-campaign")
    print(f"Payload: {json.dumps(payload, indent=2)[:200]}...")
    print("\nWaiting for LLM response...")
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/generator/marketing-campaign",
            json=payload,
            timeout=60
        )
        elapsed = time.time() - start
        
        print(f"✓ Response received in {elapsed:.1f} seconds")
        print(f"✓ Status Code: {response.status_code}")
        
        data = response.json()
        
        if 'error' in data:
            print(f"✗ Error: {data['error']}")
            return False
        
        if 'result' not in data:
            print(f"✗ Missing 'result' key in response")
            print(f"Response keys: {list(data.keys())}")
            return False
        
        result = data['result']
        
        # Verify structure
        required_keys = ['campaign_objectives', 'content_ideas', 'ad_copy_variations', 
                         'platform_specific_ctas', 'campaign_timeline', 'expected_kpis']
        
        print("\n✓ RESPONSE STRUCTURE VERIFICATION:")
        for key in required_keys:
            if key in result:
                if isinstance(result[key], list):
                    print(f"  ✓ {key}: {len(result[key])} items")
                elif isinstance(result[key], dict):
                    print(f"  ✓ {key}: {list(result[key].keys())}")
                else:
                    print(f"  ✓ {key}: {type(result[key]).__name__}")
            else:
                print(f"  ✗ MISSING {key}")
                return False
        
        print("\n✓ MARKETING CAMPAIGN TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_sales_pitch():
    print_section("TEST 2: B2B SALES PITCH ARCHITECT")
    
    payload = {
        "prospect_title": "VP of Sales",
        "company_tier": "Mid-Market (250-1000 employees)",
        "product_info": "Sales intelligence platform with AI-powered deal insights"
    }
    
    print(f"Endpoint: POST {BASE_URL}/api/generator/sales-pitch")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("\nWaiting for LLM response...")
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/generator/sales-pitch",
            json=payload,
            timeout=60
        )
        elapsed = time.time() - start
        
        print(f"✓ Response received in {elapsed:.1f} seconds")
        print(f"✓ Status Code: {response.status_code}")
        
        data = response.json()
        
        if 'error' in data:
            print(f"✗ Error: {data['error']}")
            return False
        
        if 'result' not in data:
            print(f"✗ Missing 'result' key in response")
            return False
        
        result = data['result']
        
        # Verify structure
        required_keys = ['elevator_pitch_30sec', 'pain_point_analysis', 'differentiators',
                         'strategic_cta', 'discovery_questions', 'social_proof_angles']
        
        print("\n✓ RESPONSE STRUCTURE VERIFICATION:")
        for key in required_keys:
            if key in result:
                if isinstance(result[key], list):
                    print(f"  ✓ {key}: {len(result[key])} items")
                elif isinstance(result[key], dict):
                    print(f"  ✓ {key}: {list(result[key].keys())}")
                elif isinstance(result[key], str):
                    print(f"  ✓ {key}: {result[key][:50]}...")
                else:
                    print(f"  ✓ {key}: {type(result[key]).__name__}")
            else:
                print(f"  ✗ MISSING {key}")
                return False
        
        print("\n✓ SALES PITCH TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_lead_score():
    print_section("TEST 3: INTELLIGENT LEAD SCORER")
    
    payload = {
        "budget": "$250000",
        "timeline": "This Quarter",
        "urgency": "Critical/High",
        "additional_context": "Series B funded startup, 3x YoY growth"
    }
    
    print(f"Endpoint: POST {BASE_URL}/api/generator/lead-score")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("\nWaiting for LLM response...")
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/generator/lead-score",
            json=payload,
            timeout=60
        )
        elapsed = time.time() - start
        
        print(f"✓ Response received in {elapsed:.1f} seconds")
        print(f"✓ Status Code: {response.status_code}")
        
        data = response.json()
        
        if 'error' in data:
            print(f"✗ Error: {data['error']}")
            return False
        
        if 'result' not in data:
            print(f"✗ Missing 'result' key in response")
            return False
        
        result = data['result']
        
        # Verify structure
        required_keys = ['lead_score', 'conversion_probability', 'reasoning',
                         'key_strengths', 'risk_factors', 'recommended_action', 'sales_strategy']
        
        print("\n✓ RESPONSE STRUCTURE VERIFICATION:")
        for key in required_keys:
            if key in result:
                if isinstance(result[key], list):
                    print(f"  ✓ {key}: {len(result[key])} items")
                elif isinstance(result[key], (int, float)):
                    print(f"  ✓ {key}: {result[key]}")
                elif isinstance(result[key], str):
                    print(f"  ✓ {key}: {result[key][:50]}...")
                else:
                    print(f"  ✓ {key}: {type(result[key]).__name__}")
            else:
                print(f"  ✗ MISSING {key}")
                return False
        
        # Verify lead score is in valid range
        score = result.get('lead_score', -1)
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            print(f"  ✗ Invalid lead_score: {score} (should be 0-100)")
            return False
        
        score_category = (
            "🟢 HOT LEAD (75%+ conversion)" if score >= 80 else
            "🟡 WARM LEAD (50% conversion)" if score >= 60 else
            "🟠 COOL LEAD (25% conversion)" if score >= 40 else
            "🔴 COLD LEAD (10% conversion)"
        )
        
        print(f"\n  Score Category: {score_category}")
        
        print("\n✓ LEAD SCORE TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Run all tests
if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  GENERATOR HUB: COMPREHENSIVE VALIDATION TEST".center(78) + "║")
    print("║" + "  Testing AI Marketing Strategist, Sales Pitch Architect, Lead Scorer".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    results = {
        "Marketing Campaign": test_marketing_campaign(),
        "Sales Pitch": test_sales_pitch(),
        "Lead Score": test_lead_score()
    }
    
    print_section("FINAL TEST SUMMARY")
    print("\nTest Results:")
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 80)
    if all_passed:
        print("  🎉 ALL TESTS PASSED! Generator Hub is working perfectly!")
    else:
        print("  ⚠️  Some tests failed. Check the output above for details.")
    print("=" * 80)
    print("\n📱 Access the frontend at: http://localhost:5000")
    print("🧪 Test interface at: http://localhost:5000/generator-hub-test")
    print("\n")
