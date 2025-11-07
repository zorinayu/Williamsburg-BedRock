#!/usr/bin/env python3
"""
Test script to verify AWS Bedrock API connection
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('AWS_BEARER_TOKEN_BEDROCK')

if not api_key:
    print("ERROR: AWS_BEARER_TOKEN_BEDROCK not found")
    exit(1)

# Test connection to Bedrock API
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

try:
    # List foundation models endpoint
    response = requests.get(
        'https://bedrock.us-east-1.amazonaws.com/foundation-models',
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        print("SUCCESS: Connected to AWS Bedrock API")
    else:
        print(f"ERROR: API returned status code {response.status_code}")
        exit(1)
except Exception as e:
    print(f"ERROR: Connection failed - {str(e)}")
    exit(1)

