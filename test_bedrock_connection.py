#!/usr/bin/env python3
"""
Test script to verify AWS Bedrock API connection
"""
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Create Bedrock Runtime client (for inference)
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
    
    # Test with a simple invoke
    response = bedrock_runtime.invoke_model(
        modelId='amazon.titan-text-lite-v1',
        body='{"inputText": "Hello", "textGenerationConfig": {"maxTokenCount": 10}}',
        contentType='application/json'
    )
    
    print("SUCCESS: Connected to AWS Bedrock Runtime API")
    print("Bedrock is working for inference")
    
except Exception as e:
    print(f"ERROR: Connection failed - {str(e)}")
    if "AccessDenied" in str(e):
        print("\nYour AWS role doesn't have Bedrock permissions.")
        print("Contact your AWS administrator to add Bedrock access.")
    exit(1)

