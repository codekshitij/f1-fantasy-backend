import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
import json

# Load environment variables
load_dotenv()

def test_firebase_init():
    try:
        # Get Firebase credentials from environment
        firebase_json = os.getenv("FIREBASE_CREDENTIALS")
        if not firebase_json:
            print("❌ FIREBASE_CREDENTIALS not found in environment variables")
            return False
            
        # Parse JSON
        try:
            cred_dict = json.loads(firebase_json)
            print("✅ Successfully parsed Firebase credentials JSON")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Firebase credentials JSON: {e}")
            return False
            
        # Initialize Firebase Admin
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                print("✅ Successfully initialized Firebase Admin SDK")
                return True
            except ValueError as e:
                print(f"❌ Invalid Firebase credentials: {e}")
                return False
            except Exception as e:
                print(f"❌ Unexpected error initializing Firebase: {e}")
                return False
        else:
            print("✅ Firebase Admin SDK already initialized")
            return True
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def get_fresh_token():
    try:
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-credentials.json')
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK initialized successfully")
        
        # Create a custom token
        uid = "test_user_123"  # This is just for testing
        custom_token = auth.create_custom_token(uid)
        print(f"✅ Generated custom token: {custom_token}")
        
        return custom_token
    except Exception as e:
        print(f"❌ Error getting fresh token: {e}")
        return None

if __name__ == "__main__":
    print("Testing Firebase Admin initialization...")
    success = test_firebase_init()
    print(f"\nFinal result: {'✅ Success' if success else '❌ Failed'}")

    print("\nTesting Firebase token generation...")
    token = get_fresh_token()
    if token:
        print("\n✅ Successfully generated fresh token")
    else:
        print("\n❌ Failed to generate token") 