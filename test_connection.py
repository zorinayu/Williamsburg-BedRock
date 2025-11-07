"""
Test AWS Bedrock API connection
"""
import requests
from config import get_bedrock_token, API_KEY_NAME

def test_bedrock_connection():
    """Test connection to AWS Bedrock API"""
    # Get bearer token
    token = get_bedrock_token()
    if not token:
        print("ERROR: AWS_BEARER_TOKEN_BEDROCK not set")
        return False
    
    # AWS Bedrock endpoint
    endpoint = "https://bedrock.us-east-1.amazonaws.com"
    url = f"{endpoint}/foundation-models"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            model_count = len(data.get('modelSummaries', []))
            print(f"SUCCESS: Connected to AWS Bedrock API")
            print(f"API Key Name: {API_KEY_NAME}")
            print(f"Found {model_count} foundation models")
            return True
        else:
            print(f"ERROR: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Connection failed - {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing AWS Bedrock API connection...")
    print("-" * 50)
    success = test_bedrock_connection()
    print("-" * 50)
    if success:
        print("Connection test: PASSED")
    else:
        print("Connection test: FAILED")

