import requests
import json

def test_google_login():
    # Test endpoint
    url = "http://localhost:8000/auth/google-login"
    
    # Test data (this is a dummy token, you'll need to replace it with a real one from your frontend)
    test_data = {
        "idToken": "dummy_token"  # Replace this with a real token from your frontend
    }
    
    try:
        print("Testing Google login endpoint...")
        response = requests.post(url, json=test_data)
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_google_login() 