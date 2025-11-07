"""
AWS Bedrock API Configuration
"""
import os

# API Key configuration
API_KEY_NAME = "BedrockAPIKey-xpfn-at-911541042551"
API_KEY = "ABSKQmVkcm9ja0FQSUtleS14cGZuLWF0LTkxMTU0MTA0MjU1MTo5SFVEVlZDc0QzKzVLb0JabGJ3UWlnUE91aUJ6MnlvQ0YxbHVlaFE4WHkwc1dMdUxUUGdsR2plNEEzcz0="

# Set environment variable
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = API_KEY

def get_bedrock_token():
    """Get the Bedrock API bearer token from environment variable"""
    return os.getenv("AWS_BEARER_TOKEN_BEDROCK")

