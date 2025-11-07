import os
import requests
from dotenv import load_dotenv
from typing import Dict

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(parent_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()


class BedrockHelper:
    def __init__(self):
        self.api_key = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        self.base_url = "https://bedrock.us-east-1.amazonaws.com"
    
    def enhance_analysis(self, analysis: Dict) -> Dict:
        if not self.api_key:
            return analysis
        
        enhanced_functions = []
        for func_name, func_summary in analysis['functions']:
            if func_summary.startswith("Function with"):
                enhanced_functions.append((func_name, func_summary))
            else:
                enhanced_functions.append((func_name, func_summary))
        
        analysis['functions'] = enhanced_functions
        return analysis
