import os
import boto3
import json
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
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
    
    def enhance_analysis(self, analysis: Dict) -> Dict:
        try:
            enhanced_functions = []
            for func_name, func_summary in analysis['functions']:
                if func_summary.startswith("Function with"):
                    enhanced_summary = self._generate_function_summary(func_name)
                    enhanced_functions.append((func_name, enhanced_summary))
                else:
                    enhanced_functions.append((func_name, func_summary))
            
            analysis['functions'] = enhanced_functions
            return analysis
        except Exception:
            return analysis
    
    def _generate_function_summary(self, func_name: str) -> str:
        try:
            prompt = f"Describe what a function named '{func_name}' likely does in 1 sentence."
            
            response = self.bedrock_runtime.invoke_model(
                modelId='amazon.titan-text-lite-v1',
                body=json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {"maxTokenCount": 50}
                }),
                contentType='application/json'
            )
            
            result = json.loads(response['body'].read())
            return result['results'][0]['outputText'].strip()
        except Exception:
            return f"Function with name '{func_name}'"
