"""
AI API Integration module for Playbian Auto Typer & Clicker
Supports integration with various AI APIs like Gemini, OpenAI for intelligent automation
"""

import logging
import json
import requests
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

from config import API_CONFIG, EMOJI
from actions import Action, TypeAction, ClickAction, DelayAction, HotkeyAction

logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """Response from AI API"""
    success: bool
    content: str
    actions: List[Action] = None
    error: str = None
    metadata: Dict[str, Any] = None

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.api_key = api_key
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Playbian-AutoTyper/2.1',
            'Content-Type': 'application/json'
        })
    
    @abstractmethod
    def generate_actions(self, prompt: str) -> AIResponse:
        """Generate automation actions from natural language prompt"""
        pass
    
    @abstractmethod
    def explain_actions(self, actions: List[Action]) -> AIResponse:
        """Explain what a sequence of actions will do"""
        pass
    
    @abstractmethod
    def optimize_sequence(self, actions: List[Action]) -> AIResponse:
        """Suggest optimizations for an action sequence"""
        pass
    
    def is_configured(self) -> bool:
        """Check if provider is properly configured"""
        return bool(self.api_key and self.api_key.strip())

class GeminiProvider(AIProvider):
    """Google Gemini AI provider"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = config.get('model', 'gemini-pro')
        
        # Update session headers for Gemini
        self.session.headers.update({
            'x-goog-api-key': self.api_key
        })
    
    def generate_actions(self, prompt: str) -> AIResponse:
        """Generate automation actions from natural language using Gemini"""
        try:
            # Construct the system prompt for action generation
            system_prompt = self._get_action_generation_prompt()
            
            # Prepare the request
            request_data = {
                "contents": [{
                    "parts": [{
                        "text": f"{system_prompt}\n\nUser Request: {prompt}"
                    }]
                }],
                "generationConfig": {
                    "temperature": self.config.get('temperature', 0.3),
                    "maxOutputTokens": self.config.get('max_tokens', 1000),
                    "topP": 0.8,
                    "topK": 10
                }
            }
            
            # Make API call
            url = f"{self.base_url}/models/{self.model}:generateContent"
            response = self.session.post(url, json=request_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['candidates'][0]['content']['parts'][0]['text']
                
                # Parse the response to extract actions
                actions = self._parse_action_response(content)
                
                return AIResponse(
                    success=True,
                    content=content,
                    actions=actions,
                    metadata={'model': self.model, 'provider': 'gemini'}
                )
            else:
                error_msg = f"Gemini API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return AIResponse(success=False, content="", error=error_msg)
        
        except Exception as e:
            error_msg = f"Failed to generate actions with Gemini: {str(e)}"
            logger.error(error_msg)
            return AIResponse(success=False, content="", error=error_msg)
    
    def explain_actions(self, actions: List[Action]) -> AIResponse:
        """Explain what a sequence of actions will do using Gemini"""
        try:
            # Convert actions to readable format
            actions_text = self._actions_to_text(actions)
            
            prompt = f"""
            Please explain what this automation sequence will do in simple, user-friendly terms:
            
            Actions:
            {actions_text}
            
            Provide a clear, step-by-step explanation of what will happen when this automation runs.
            """
            
            request_data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 500
                }
            }
            
            url = f"{self.base_url}/models/{self.model}:generateContent"
            response = self.session.post(url, json=request_data, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                content = result['candidates'][0]['content']['parts'][0]['text']
                
                return AIResponse(
                    success=True,
                    content=content,
                    metadata={'model': self.model, 'provider': 'gemini'}
                )
            else:
                error_msg = f"Gemini API error: {response.status_code}"
                return AIResponse(success=False, content="", error=error_msg)
        
        except Exception as e:
            error_msg = f"Failed to explain actions with Gemini: {str(e)}"
            logger.error(error_msg)
            return AIResponse(success=False, content="", error=error_msg)
    
    def optimize_sequence(self, actions: List[Action]) -> AIResponse:
        """Suggest optimizations for an action sequence using Gemini"""
        try:
            actions_text = self._actions_to_text(actions)
            
            prompt = f"""
            Analyze this automation sequence and suggest optimizations:
            
            Current Actions:
            {actions_text}
            
            Please suggest:
            1. Ways to make it more efficient
            2. Potential timing improvements
            3. Any redundant actions that could be removed
            4. Better approaches for the same outcome
            
            Provide specific, actionable recommendations.
            """
            
            request_data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 800
                }
            }
            
            url = f"{self.base_url}/models/{self.model}:generateContent"
            response = self.session.post(url, json=request_data, timeout=25)
            
            if response.status_code == 200:
                result = response.json()
                content = result['candidates'][0]['content']['parts'][0]['text']
                
                return AIResponse(
                    success=True,
                    content=content,
                    metadata={'model': self.model, 'provider': 'gemini'}
                )
            else:
                error_msg = f"Gemini API error: {response.status_code}"
                return AIResponse(success=False, content="", error=error_msg)
        
        except Exception as e:
            error_msg = f"Failed to optimize sequence with Gemini: {str(e)}"
            logger.error(error_msg)
            return AIResponse(success=False, content="", error=error_msg)
    
    def _get_action_generation_prompt(self) -> str:
        """Get the system prompt for action generation"""
        return """
You are an automation assistant that converts natural language requests into specific automation actions.

Available action types:
1. TYPE: Type text (supports special keys like <enter>, <tab>, etc.)
2. CLICK: Click at specific coordinates with left/right/middle button
3. DELAY: Wait for specified time in seconds
4. HOTKEY: Press key combinations (e.g., ctrl+c, alt+tab)
5. SPECIAL_KEY: Press individual keys (enter, escape, backspace, etc.)

Response format (JSON):
{
  "actions": [
    {"type": "TYPE", "text": "Hello World<enter>", "delay": 0.5},
    {"type": "CLICK", "x": 100, "y": 200, "button": "left", "delay": 0.2},
    {"type": "DELAY", "wait_time": 2.0},
    {"type": "HOTKEY", "keys": ["ctrl", "v"], "delay": 0.1},
    {"type": "SPECIAL_KEY", "key": "enter", "delay": 0.0}
  ],
  "explanation": "Brief explanation of what this automation does"
}

Guidelines:
- Use realistic coordinates (typical screen: 1920x1080)
- Add appropriate delays between actions (0.1-2.0 seconds)
- Use special keys in text with angle brackets: <enter>, <tab>, <backspace>
- For hotkeys, separate keys with commas: ["ctrl", "c"]
- Be specific and accurate
- Consider user workflow and timing

Generate automation actions for the following request:
        """
    
    def _parse_action_response(self, content: str) -> List[Action]:
        """Parse AI response into Action objects"""
        actions = []
        
        try:
            # Try to extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                data = json.loads(json_str)
                
                for action_data in data.get('actions', []):
                    action = self._create_action_from_data(action_data)
                    if action:
                        actions.append(action)
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse AI response: {e}")
            # Fallback: try to extract actions from text
            actions = self._parse_text_response(content)
        
        return actions
    
    def _create_action_from_data(self, data: Dict[str, Any]) -> Optional[Action]:
        """Create Action object from parsed data"""
        try:
            action_type = data.get('type', '').upper()
            delay = data.get('delay', 0.0)
            
            if action_type == 'TYPE':
                return TypeAction(data['text'], delay)
            elif action_type == 'CLICK':
                return ClickAction(
                    data['x'], data['y'], 
                    data.get('button', 'left'), delay
                )
            elif action_type == 'DELAY':
                return DelayAction(data['wait_time'])
            elif action_type == 'HOTKEY':
                return HotkeyAction(data['keys'], delay)
            elif action_type == 'SPECIAL_KEY':
                from actions import SpecialKeyAction
                return SpecialKeyAction(data['key'], delay)
            
        except (KeyError, TypeError, ValueError) as e:
            logger.warning(f"Failed to create action from data {data}: {e}")
        
        return None
    
    def _parse_text_response(self, content: str) -> List[Action]:
        """Fallback parser for text responses"""
        actions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Simple pattern matching for common actions
            if line.lower().startswith('type:'):
                text = line[5:].strip()
                actions.append(TypeAction(text, 0.5))
            elif line.lower().startswith('click:'):
                # Extract coordinates from "click: x,y" format
                coords = line[6:].strip()
                if ',' in coords:
                    try:
                        x, y = map(int, coords.split(','))
                        actions.append(ClickAction(x, y, 'left', 0.2))
                    except ValueError:
                        pass
            elif line.lower().startswith('wait:'):
                # Extract wait time
                try:
                    wait_time = float(line[5:].strip())
                    actions.append(DelayAction(wait_time))
                except ValueError:
                    pass
        
        return actions
    
    def _actions_to_text(self, actions: List[Action]) -> str:
        """Convert actions to readable text format"""
        lines = []
        for i, action in enumerate(actions, 1):
            lines.append(f"{i}. {str(action)}")
        return '\n'.join(lines)

class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self.base_url = "https://api.openai.com/v1"
        self.model = config.get('model', 'gpt-3.5-turbo')
        
        # Update session headers for OpenAI
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}'
        })
    
    def generate_actions(self, prompt: str) -> AIResponse:
        """Generate automation actions using OpenAI GPT"""
        try:
            system_prompt = self._get_action_generation_prompt()
            
            request_data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.get('temperature', 0.3),
                "max_tokens": self.config.get('max_tokens', 1000)
            }
            
            url = f"{self.base_url}/chat/completions"
            response = self.session.post(url, json=request_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse the response similar to Gemini
                actions = self._parse_action_response(content)
                
                return AIResponse(
                    success=True,
                    content=content,
                    actions=actions,
                    metadata={'model': self.model, 'provider': 'openai'}
                )
            else:
                error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return AIResponse(success=False, content="", error=error_msg)
        
        except Exception as e:
            error_msg = f"Failed to generate actions with OpenAI: {str(e)}"
            logger.error(error_msg)
            return AIResponse(success=False, content="", error=error_msg)
    
    def explain_actions(self, actions: List[Action]) -> AIResponse:
        """Explain actions using OpenAI"""
        # Similar implementation to Gemini but using OpenAI API format
        try:
            actions_text = self._actions_to_text(actions)
            
            request_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an automation expert. Explain automation sequences in clear, simple terms."
                    },
                    {
                        "role": "user",
                        "content": f"Explain what this automation sequence does:\n\n{actions_text}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            url = f"{self.base_url}/chat/completions"
            response = self.session.post(url, json=request_data, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return AIResponse(
                    success=True,
                    content=content,
                    metadata={'model': self.model, 'provider': 'openai'}
                )
            else:
                error_msg = f"OpenAI API error: {response.status_code}"
                return AIResponse(success=False, content="", error=error_msg)
        
        except Exception as e:
            error_msg = f"Failed to explain actions with OpenAI: {str(e)}"
            logger.error(error_msg)
            return AIResponse(success=False, content="", error=error_msg)
    
    def optimize_sequence(self, actions: List[Action]) -> AIResponse:
        """Optimize sequence using OpenAI"""
        # Similar to explain_actions but with optimization prompt
        try:
            actions_text = self._actions_to_text(actions)
            
            request_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an automation optimization expert. Analyze sequences and suggest improvements."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze and suggest optimizations for this automation sequence:\n\n{actions_text}"
                    }
                ],
                "temperature": 0.4,
                "max_tokens": 800
            }
            
            url = f"{self.base_url}/chat/completions"
            response = self.session.post(url, json=request_data, timeout=25)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return AIResponse(
                    success=True,
                    content=content,
                    metadata={'model': self.model, 'provider': 'openai'}
                )
            else:
                error_msg = f"OpenAI API error: {response.status_code}"
                return AIResponse(success=False, content="", error=error_msg)
        
        except Exception as e:
            error_msg = f"Failed to optimize sequence with OpenAI: {str(e)}"
            logger.error(error_msg)
            return AIResponse(success=False, content="", error=error_msg)
    
    # Reuse parsing methods from GeminiProvider
    def _get_action_generation_prompt(self) -> str:
        return GeminiProvider._get_action_generation_prompt(self)
    
    def _parse_action_response(self, content: str) -> List[Action]:
        return GeminiProvider._parse_action_response(self, content)
    
    def _create_action_from_data(self, data: Dict[str, Any]) -> Optional[Action]:
        return GeminiProvider._create_action_from_data(self, data)
    
    def _parse_text_response(self, content: str) -> List[Action]:
        return GeminiProvider._parse_text_response(self, content)
    
    def _actions_to_text(self, actions: List[Action]) -> str:
        return GeminiProvider._actions_to_text(self, actions)

class AIManager:
    """Manager class for AI providers"""
    
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self.current_provider: Optional[str] = None
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available AI providers"""
        # Initialize Gemini provider
        gemini_config = API_CONFIG.get('gemini', {})
        if gemini_config.get('enabled', False) and gemini_config.get('api_key'):
            try:
                self.providers['gemini'] = GeminiProvider(
                    gemini_config['api_key'],
                    gemini_config
                )
                if not self.current_provider:
                    self.current_provider = 'gemini'
                logger.info("Gemini provider initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini provider: {e}")
        
        # Initialize OpenAI provider
        openai_config = API_CONFIG.get('openai', {})
        if openai_config.get('enabled', False) and openai_config.get('api_key'):
            try:
                self.providers['openai'] = OpenAIProvider(
                    openai_config['api_key'],
                    openai_config
                )
                if not self.current_provider:
                    self.current_provider = 'openai'
                logger.info("OpenAI provider initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI provider: {e}")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return list(self.providers.keys())
    
    def set_current_provider(self, provider_name: str) -> bool:
        """Set the current active provider"""
        if provider_name in self.providers:
            self.current_provider = provider_name
            logger.info(f"Switched to {provider_name} provider")
            return True
        return False
    
    def get_current_provider(self) -> Optional[AIProvider]:
        """Get the current active provider"""
        if self.current_provider and self.current_provider in self.providers:
            return self.providers[self.current_provider]
        return None
    
    def is_available(self) -> bool:
        """Check if any AI provider is available"""
        return len(self.providers) > 0 and self.current_provider is not None
    
    def generate_actions_from_text(self, prompt: str) -> AIResponse:
        """Generate actions from natural language description"""
        provider = self.get_current_provider()
        if not provider:
            return AIResponse(
                success=False,
                content="",
                error="No AI provider available. Please configure an API key."
            )
        
        logger.info(f"Generating actions from prompt: {prompt[:100]}...")
        return provider.generate_actions(prompt)
    
    def explain_action_sequence(self, actions: List[Action]) -> AIResponse:
        """Get explanation of what an action sequence will do"""
        provider = self.get_current_provider()
        if not provider:
            return AIResponse(
                success=False,
                content="",
                error="No AI provider available"
            )
        
        logger.info(f"Explaining sequence of {len(actions)} actions")
        return provider.explain_actions(actions)
    
    def suggest_optimizations(self, actions: List[Action]) -> AIResponse:
        """Get optimization suggestions for an action sequence"""
        provider = self.get_current_provider()
        if not provider:
            return AIResponse(
                success=False,
                content="",
                error="No AI provider available"
            )
        
        logger.info(f"Suggesting optimizations for {len(actions)} actions")
        return provider.optimize_sequence(actions)
    
    def test_connection(self, provider_name: str = None) -> Tuple[bool, str]:
        """Test connection to AI provider"""
        if provider_name:
            provider = self.providers.get(provider_name)
        else:
            provider = self.get_current_provider()
        
        if not provider:
            return False, "Provider not available"
        
        try:
            # Simple test request
            response = provider.generate_actions("test connection")
            if response.success:
                return True, "Connection successful"
            else:
                return False, response.error or "Unknown error"
        except Exception as e:
            return False, str(e)
    
    def update_api_key(self, provider_name: str, api_key: str) -> bool:
        """Update API key for a provider"""
        try:
            if provider_name == 'gemini':
                config = API_CONFIG.get('gemini', {})
                config['api_key'] = api_key
                config['enabled'] = bool(api_key.strip())
                self.providers['gemini'] = GeminiProvider(api_key, config)
            elif provider_name == 'openai':
                config = API_CONFIG.get('openai', {})
                config['api_key'] = api_key
                config['enabled'] = bool(api_key.strip())
                self.providers['openai'] = OpenAIProvider(api_key, config)
            else:
                return False
            
            logger.info(f"Updated API key for {provider_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to update API key for {provider_name}: {e}")
            return False

# Global AI manager instance
ai_manager = AIManager()

def get_ai_manager() -> AIManager:
    """Get the global AI manager instance"""
    return ai_manager

# Example usage functions for the UI
def generate_smart_actions(description: str) -> Tuple[bool, str, List[Action]]:
    """
    Generate actions from natural language description
    Returns: (success, message, actions)
    """
    if not ai_manager.is_available():
        return False, "AI features not available. Please configure an API key in settings.", []
    
    try:
        response = ai_manager.generate_actions_from_text(description)
        if response.success:
            return True, "Actions generated successfully!", response.actions or []
        else:
            return False, response.error or "Failed to generate actions", []
    except Exception as e:
        logger.error(f"Error generating smart actions: {e}")
        return False, f"Error: {str(e)}", []

def explain_sequence_intelligently(actions: List[Action]) -> Tuple[bool, str]:
    """
    Get AI explanation of what an action sequence will do
    Returns: (success, explanation)
    """
    if not ai_manager.is_available():
        return False, "AI features not available"
    
    try:
        response = ai_manager.explain_action_sequence(actions)
        if response.success:
            return True, response.content
        else:
            return False, response.error or "Failed to explain sequence"
    except Exception as e:
        logger.error(f"Error explaining sequence: {e}")
        return False, f"Error: {str(e)}"

def get_optimization_suggestions(actions: List[Action]) -> Tuple[bool, str]:
    """
    Get AI suggestions for optimizing an action sequence
    Returns: (success, suggestions)
    """
    if not ai_manager.is_available():
        return False, "AI features not available"
    
    try:
        response = ai_manager.suggest_optimizations(actions)
        if response.success:
            return True, response.content
        else:
            return False, response.error or "Failed to get suggestions"
    except Exception as e:
        logger.error(f"Error getting optimization suggestions: {e}")
        return False, f"Error: {str(e)}"
