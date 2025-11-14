import os
import boto3
import json
from dotenv import load_dotenv
from typing import Dict
import requests

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(parent_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()


class BedrockHelper:
    def __init__(self):
        # Check for bearer token authentication
        bearer_token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        if bearer_token:
            # Use bearer token authentication
            self.bearer_token = bearer_token
            self.use_bearer_token = True
            self.region = 'us-west-2'
            self.bedrock_runtime = None  # Will use direct HTTP requests
        else:
            # Use default AWS credentials
            self.use_bearer_token = False
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
    
    def _invoke_model_with_bearer_token(self, model_id: str, body: dict) -> dict:
        """Invoke Bedrock model using bearer token authentication"""
        url = f"https://bedrock-runtime.{self.region}.amazonaws.com/model/{model_id}/invoke"
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=body, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Re-raise HTTP errors to be handled by the caller
            raise
        except requests.exceptions.RequestException as e:
            # Handle other request errors
            raise Exception(f"Request failed: {str(e)}")
    
    def _invoke_model(self, model_id: str, body: dict, content_type: str = 'application/json'):
        """Unified method to invoke model with either bearer token or boto3"""
        if self.use_bearer_token:
            result = self._invoke_model_with_bearer_token(model_id, body)
            # Convert to boto3-like response format
            class ResponseBody:
                def __init__(self, data):
                    self.data = data
                def read(self):
                    return json.dumps(self.data).encode('utf-8')
            return {'body': ResponseBody(result)}
        else:
            return self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType=content_type
            )
    
    def get_available_models(self):
        """Get list of available Bedrock foundation models"""
        # Return a conservative list of well-tested models
        # Default model (amazon.titan-text-lite-v1) is first
        return [
            {'modelId': 'amazon.titan-text-lite-v1', 'modelName': 'Amazon Titan Text Lite', 'providerName': 'Amazon'},
            {'modelId': 'amazon.titan-text-express-v1', 'modelName': 'Amazon Titan Text Express', 'providerName': 'Amazon'},
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
            # Clean and prepare the code
            code_lines = func_code.strip().split('\n')
            # Remove empty lines at start/end
            while code_lines and not code_lines[0].strip():
                code_lines.pop(0)
            while code_lines and not code_lines[-1].strip():
                code_lines.pop()
            clean_code = '\n'.join(code_lines)
            
            prompt = f"""You are a code translator. Convert the following {source_language} function to {target_language}. Maintain the same functionality and logic.

{source_language} code:
{clean_code}

Converted {target_language} code:"""
            
            # Check if it's a Claude model (different API format)
            if 'claude' in model_id.lower():
                return self._invoke_claude_model(model_id, prompt, max_tokens=400)
            else:
                # Titan and other models
                request_body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 400,
                        "temperature": 0.7,
                        "topP": 0.9
                    }
                }
                response = self._invoke_model(model_id, request_body)
                result = json.loads(response['body'].read())
                
                # Check for errors in response (top level)
                if 'message' in result:
                    error_msg = result.get('message', 'Unknown error')
                    # Check if it's the specific "unable to respond" error
                    if 'unable to respond' in error_msg.lower() or 'sorry' in error_msg.lower():
                        return f"MODEL_ERROR: The current model cannot process this request. Please try selecting a different model (e.g., Titan Text Lite) or simplify the code."
                    return f"MODEL_ERROR: {error_msg}"
                
                # Check for results array
                if 'results' in result and len(result['results']) > 0:
                    first_result = result['results'][0]
                    
                    # Check for error message in result
                    if 'message' in first_result:
                        error_msg = first_result['message']
                        if 'unable to respond' in error_msg.lower() or 'sorry' in error_msg.lower():
                            return f"MODEL_ERROR: The current model cannot process this request. Please try selecting a different model (e.g., Titan Text Lite) or simplify the code."
                        return f"MODEL_ERROR: {error_msg}"
                    
                    # Get output text
                    output_text = first_result.get('outputText', '')
                    if output_text and output_text.strip():
                        # Clean up the output - remove any explanatory text
                        output = output_text.strip()
                        
                        # Check if output contains error messages (non-model related errors)
                        # Only check for specific error patterns, not generic words that might appear in code
                        error_patterns = [
                            'sorry - this model',
                            'sorry, this model',
                            'unable to respond',
                            'cannot process this request',
                            'this model is unable'
                        ]
                        output_lower = output.lower()
                        # Check if the output is primarily an error message (short and contains error patterns)
                        if len(output) < 200 and any(pattern in output_lower for pattern in error_patterns):
                            # This is likely an error message from the model
                            return f"MODEL_ERROR: {output}"
                        
                        # Try to extract just the code if there's extra text
                        if '```' in output:
                            # Extract code from markdown code blocks
                            parts = output.split('```')
                            for i, part in enumerate(parts):
                                if i % 2 == 1:  # Odd indices are code blocks
                                    code = part.strip()
                                    if code.startswith(target_language.lower()) or code.startswith('python') or code.startswith('java'):
                                        code = '\n'.join(code.split('\n')[1:])  # Remove language identifier
                                    if code:
                                        return code.strip()
                        return output
                
                # If no output found, return error
                return f"// Error: Unexpected response format from model. Response: {json.dumps(result)[:200]}"
                
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (non-model related)
            error_msg = f"HTTP Error: {e.response.status_code}"
            if e.response.status_code == 401:
                error_msg = "Authentication failed. Please check your API key."
            elif e.response.status_code == 403:
                error_msg = "Access denied. Please check your API permissions."
            elif e.response.status_code == 429:
                error_msg = "Rate limit exceeded. Please try again later."
            elif e.response.status_code >= 500:
                error_msg = "Server error. Please try again later."
            try:
                error_detail = e.response.json()
                if 'message' in error_detail:
                    error_msg = error_detail['message']
            except:
                pass
            return f"HTTP_ERROR: {error_msg}"
        except Exception as e:
            error_msg = str(e)
            # Extract more detailed error if available
            if hasattr(e, 'response'):
                try:
                    error_detail = json.loads(e.response['Error'].get('Message', ''))
                    error_msg = error_detail.get('message', error_msg)
                except:
                    pass
            return f"SYSTEM_ERROR: Error converting to {target_language}: {error_msg}"
    
    def _invoke_claude_model(self, model_id: str, prompt: str, max_tokens: int = 400) -> str:
        """Invoke Claude model with proper API format"""
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            response = self._invoke_model(model_id, request_body)
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
                request_body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 100,
                        "temperature": 0.7,
                        "topP": 0.9
                    }
                }
                response = self._invoke_model(model_id, request_body)
                result = json.loads(response['body'].read())
                
                # Check for errors in response
                if 'message' in result:
                    return f"Function: {func_name} (Model error: {result['message']})"
                
                # Check for results array
                if 'results' in result and len(result['results']) > 0:
                    output_text = result['results'][0].get('outputText', '')
                    if output_text:
                        return output_text.strip()
                    # Check for error in result
                    if 'message' in result['results'][0]:
                        return f"Function: {func_name} (Error: {result['results'][0]['message']})"
                
                return f"Function: {func_name}"
                
        except Exception as e:
            error_msg = str(e)
            # Extract more detailed error if available
            if hasattr(e, 'response'):
                try:
                    error_detail = json.loads(e.response['Error'].get('Message', ''))
                    error_msg = error_detail.get('message', error_msg)
                except:
                    pass
            return f"Function: {func_name} (Error: {error_msg})"
