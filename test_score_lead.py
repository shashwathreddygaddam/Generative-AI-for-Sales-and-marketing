import requests
import json

print("Testing /api/score-lead endpoint...")
payload = {'budget': '$250000', 'timeline': 'This Quarter', 'urgency': 'High'}

try:
    response = requests.post('http://localhost:5000/api/score-lead', json=payload, timeout=60)
    result = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Response:\n{json.dumps(result, indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")
