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
                response = self.bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "inputText": prompt,
                        "textGenerationConfig": {
                            "maxTokenCount": 400,
                            "temperature": 0.7,
                            "topP": 0.9
                        }
                    }),
                    contentType='application/json'
                )
                result = json.loads(response['body'].read())
                
                # Check for errors in response (top level)
                if 'message' in result:
                    error_msg = result.get('message', 'Unknown error')
                    # Check if it's the specific "unable to respond" error
                    if 'unable to respond' in error_msg.lower():
                        return f"// Error: Model cannot process this request. Try using Titan Text Lite instead, or simplify the code."
                    return f"// Error: {error_msg}"
                
                # Check for results array
                if 'results' in result and len(result['results']) > 0:
                    first_result = result['results'][0]
                    
                    # Check for error message in result
                    if 'message' in first_result:
                        error_msg = first_result['message']
                        if 'unable to respond' in error_msg.lower():
                            return f"// Error: Model cannot process this request. Try using Titan Text Lite instead, or simplify the code."
                        return f"// Error: {error_msg}"
                    
                    # Get output text
                    output_text = first_result.get('outputText', '')
                    if output_text and output_text.strip():
                        # Clean up the output - remove any explanatory text
                        output = output_text.strip()
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
                
        except Exception as e:
            error_msg = str(e)
            # Extract more detailed error if available
            if hasattr(e, 'response'):
                try:
                    error_detail = json.loads(e.response['Error'].get('Message', ''))
                    error_msg = error_detail.get('message', error_msg)
                except:
                    pass
            return f"// Error converting to {target_language}: {error_msg}"
    
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
                        "textGenerationConfig": {
                            "maxTokenCount": 100,
                            "temperature": 0.7,
                            "topP": 0.9
                        }
                    }),
                    contentType='application/json'
                )
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
