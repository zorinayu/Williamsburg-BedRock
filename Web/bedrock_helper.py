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
    
    def get_available_models(self):
        """Get list of available Bedrock foundation models"""
        # Return a conservative list of well-tested models
        # Default model (amazon.titan-text-lite-v1) is first
        return [
            {'modelId': 'amazon.titan-text-lite-v1', 'modelName': 'Amazon Titan Text Lite', 'providerName': 'Amazon'},
            {'modelId': 'amazon.titan-text-express-v1', 'modelName': 'Amazon Titan Text Express', 'providerName': 'Amazon'},
            {'modelId': 'anthropic.claude-3-haiku-20240307-v1:0', 'modelName': 'Claude 3 Haiku', 'providerName': 'Anthropic'},
            {'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0', 'modelName': 'Claude 3 Sonnet', 'providerName': 'Anthropic'},
        ]
    
    def enhance_analysis(self, analysis: Dict, model_id: str = 'amazon.titan-text-lite-v1') -> Dict:
        try:
            language = analysis.get('language', 'Unknown')
            enhanced_functions = []
            for func_data in analysis['functions']:
                if len(func_data) == 3:
                    func_name, func_summary, func_code = func_data
                    # Enhance summary for any language
                    if func_summary.startswith("Function:") or func_summary.startswith("Function with"):
                        enhanced_summary = self._generate_function_summary(func_name, func_code, language, model_id)
                        enhanced_functions.append((func_name, enhanced_summary, func_code))
                    else:
                        enhanced_functions.append((func_name, func_summary, func_code))
                else:
                    # Backward compatibility
                    enhanced_functions.append(func_data)
            
            analysis['functions'] = enhanced_functions
            return analysis
        except Exception:
            return analysis
    
    def convert_function_to_language(self, func_code: str, target_language: str, source_language: str = "Python", model_id: str = 'amazon.titan-text-lite-v1') -> str:
        """Convert function from source language to target language using Bedrock"""
        try:
            prompt = f"""Convert this {source_language} function to {target_language}. Keep the same logic and functionality:

{func_code}

Provide only the converted code without explanations."""
            
            # Check if it's a Claude model (different API format)
            if 'claude' in model_id.lower():
                return self._invoke_claude_model(model_id, prompt, max_tokens=400)
            else:
                # Titan and other models
                response = self.bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "inputText": prompt,
                        "textGenerationConfig": {"maxTokenCount": 400}
                    }),
                    contentType='application/json'
                )
                result = json.loads(response['body'].read())
                return result['results'][0]['outputText'].strip()
        except Exception as e:
            return f"// Error converting to {target_language}: {str(e)}"
    
    def _invoke_claude_model(self, model_id: str, prompt: str, max_tokens: int = 400) -> str:
        """Invoke Claude model with proper API format"""
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }),
                contentType='application/json'
            )
            result = json.loads(response['body'].read())
            return result['content'][0]['text'].strip()
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def _generate_function_summary(self, func_name: str, func_code: str = "", language: str = "Python", model_id: str = 'amazon.titan-text-lite-v1') -> str:
        try:
            if func_code:
                prompt = f"""Analyze this {language} function and provide a concise one-sentence description of what it does:

{func_code[:500]}

Provide only a brief description in one sentence."""
            else:
                prompt = f"Describe what a {language} function named '{func_name}' likely does in 1 sentence."
            
            # Check if it's a Claude model (different API format)
            if 'claude' in model_id.lower():
                return self._invoke_claude_model(model_id, prompt, max_tokens=100)
            else:
                # Titan and other models
                response = self.bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "inputText": prompt,
                        "textGenerationConfig": {"maxTokenCount": 100}
                    }),
                    contentType='application/json'
                )
                result = json.loads(response['body'].read())
                return result['results'][0]['outputText'].strip()
        except Exception as e:
            return f"Function: {func_name} (Error: {str(e)})"
