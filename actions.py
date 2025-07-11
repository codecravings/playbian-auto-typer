"""
Action classes and automation logic for Playbian Auto Typer & Clicker
Handles all automation actions including typing, clicking, delays, and hotkeys
"""

import time
import pyautogui
import logging
from typing import List, Dict, Any, Optional
from config import SPECIAL_KEYS, EMOJI

# Configure PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# Setup logging
logger = logging.getLogger(__name__)

class ActionError(Exception):
    """Custom exception for action-related errors"""
    pass

class Action:
    """Base class for all automation actions"""
    
    def __init__(self, delay: float = 0):
        self.delay = delay  # Delay before executing this action
        self.id = None  # Unique identifier for the action
        self.name = ""  # Human-readable name
        self.description = ""  # Detailed description
        self.enabled = True  # Whether this action is enabled
        self.created_at = time.time()  # When the action was created
    
    def execute(self) -> bool:
        """Execute the action. Returns True if successful, False otherwise."""
        try:
            if not self.enabled:
                logger.info(f"Skipping disabled action: {self}")
                return True
                
            if self.delay > 0:
                logger.debug(f"Waiting {self.delay}s before executing {self}")
                time.sleep(self.delay)
            
            return self._execute_impl()
        except Exception as e:
            logger.error(f"Error executing action {self}: {e}")
            raise ActionError(f"Failed to execute {self.__class__.__name__}: {str(e)}")
    
    def _execute_impl(self) -> bool:
        """Subclasses should implement this method"""
        raise NotImplementedError("Subclasses must implement _execute_impl")
    
    def validate(self) -> bool:
        """Validate the action configuration. Returns True if valid."""
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary for serialization"""
        return {
            "type": self.__class__.__name__,
            "delay": self.delay,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "created_at": self.created_at
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load action from dictionary"""
        self.delay = data.get("delay", 0)
        self.id = data.get("id")
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.enabled = data.get("enabled", True)
        self.created_at = data.get("created_at", time.time())
    
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> 'Action':
        """Create action instance from dictionary"""
        action_type = data.get("type")
        
        if action_type == "TypeAction":
            action = TypeAction(data.get("text", ""))
        elif action_type == "ClickAction":
            action = ClickAction(
                data.get("x", 0), 
                data.get("y", 0), 
                data.get("button", "left")
            )
        elif action_type == "DelayAction":
            action = DelayAction(data.get("wait_time", 1.0))
        elif action_type == "HotkeyAction":
            action = HotkeyAction(data.get("keys", []))
        elif action_type == "SpecialKeyAction":
            action = SpecialKeyAction(data.get("key", "enter"))
        elif action_type == "ScrollAction":
            action = ScrollAction(
                data.get("x", 0),
                data.get("y", 0),
                data.get("clicks", 3),
                data.get("direction", "up")
            )
        elif action_type == "DragAction":
            action = DragAction(
                data.get("start_x", 0),
                data.get("start_y", 0),
                data.get("end_x", 0),
                data.get("end_y", 0),
                data.get("duration", 1.0)
            )
        else:
            raise ValueError(f"Unknown action type: {action_type}")
        
        action.from_dict(data)
        return action
    
    def clone(self) -> 'Action':
        """Create a copy of this action"""
        return self.create_from_dict(self.to_dict())

class TypeAction(Action):
    """Action for typing text with support for special keys"""
    
    def __init__(self, text: str, delay: float = 0):
        super().__init__(delay)
        self.text = text
        self.name = f"Type Text"
        self.description = f"Type: {text[:50]}{'...' if len(text) > 50 else ''}"
    
    def _execute_impl(self) -> bool:
        """Execute the typing action"""
        if not self.text:
            return True
        
        logger.info(f"Typing text: {self.text[:100]}{'...' if len(self.text) > 100 else ''}")
        
        # Parse text for special keys
        parts = self._parse_text_with_special_keys(self.text)
        
        # Type each part
        for part_type, part_value in parts:
            if part_type == "text":
                pyautogui.typewrite(part_value)
            else:  # It's a special key
                pyautogui.press(part_value)
        
        return True
    
    def _parse_text_with_special_keys(self, text: str) -> List[tuple]:
        """Parse text and extract special keys"""
        parts = []
        current_text = ""
        i = 0
        
        while i < len(text):
            if text[i] == "<":
                # Find the closing bracket
                closing_idx = text.find(">", i)
                if closing_idx != -1:
                    possible_key = text[i:closing_idx+1].lower()
                    if possible_key in SPECIAL_KEYS:
                        # We found a special key
                        if current_text:
                            parts.append(("text", current_text))
                            current_text = ""
                        parts.append(("key", SPECIAL_KEYS[possible_key]))
                        i = closing_idx + 1
                        continue
            
            current_text += text[i]
            i += 1
        
        # Add any remaining text
        if current_text:
            parts.append(("text", current_text))
        
        return parts
    
    def validate(self) -> bool:
        """Validate the typing action"""
        return isinstance(self.text, str)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["text"] = self.text
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.text = data.get("text", "")
        self.description = f"Type: {self.text[:50]}{'...' if len(self.text) > 50 else ''}"
    
    def __str__(self):
        return f"Type '{self.text}' (delay: {self.delay}s)"

class ClickAction(Action):
    """Action for mouse clicking"""
    
    def __init__(self, x: int, y: int, button: str = "left", delay: float = 0):
        super().__init__(delay)
        self.x = x
        self.y = y
        self.button = button
        self.name = f"{button.title()} Click"
        self.description = f"Click {button} at ({x}, {y})"
    
    def _execute_impl(self) -> bool:
        """Execute the click action"""
        logger.info(f"Clicking {self.button} at ({self.x}, {self.y})")
        pyautogui.click(x=self.x, y=self.y, button=self.button)
        return True
    
    def validate(self) -> bool:
        """Validate the click action"""
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            return False
        if self.button not in ["left", "right", "middle"]:
            return False
        if self.x < 0 or self.y < 0:
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "x": self.x,
            "y": self.y,
            "button": self.button
        })
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.button = data.get("button", "left")
        self.description = f"Click {self.button} at ({self.x}, {self.y})"
    
    def __str__(self):
        return f"Click {self.button} at ({self.x}, {self.y}) (delay: {self.delay}s)"

class DelayAction(Action):
    """Action for waiting/delays"""
    
    def __init__(self, wait_time: float):
        super().__init__(0)  # DelayAction doesn't use the base delay
        self.wait_time = wait_time
        self.name = "Delay"
        self.description = f"Wait for {wait_time} seconds"
    
    def _execute_impl(self) -> bool:
        """Execute the delay action"""
        logger.info(f"Waiting for {self.wait_time} seconds")
        time.sleep(self.wait_time)
        return True
    
    def validate(self) -> bool:
        """Validate the delay action"""
        return isinstance(self.wait_time, (int, float)) and self.wait_time >= 0
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["wait_time"] = self.wait_time
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.wait_time = data.get("wait_time", 1.0)
        self.description = f"Wait for {self.wait_time} seconds"
    
    def __str__(self):
        return f"Wait for {self.wait_time}s"

class HotkeyAction(Action):
    """Action for keyboard hotkey combinations"""
    
    def __init__(self, keys: List[str], delay: float = 0):
        super().__init__(delay)
        self.keys = keys if isinstance(keys, list) else [keys]
        self.name = "Hotkey"
        self.description = f"Press {'+'.join(self.keys)}"
    
    def _execute_impl(self) -> bool:
        """Execute the hotkey action"""
        logger.info(f"Pressing hotkey: {'+'.join(self.keys)}")
        pyautogui.hotkey(*self.keys)
        return True
    
    def validate(self) -> bool:
        """Validate the hotkey action"""
        if not isinstance(self.keys, list) or not self.keys:
            return False
        return all(isinstance(key, str) for key in self.keys)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["keys"] = self.keys
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.keys = data.get("keys", [])
        self.description = f"Press {'+'.join(self.keys)}"
    
    def __str__(self):
        return f"Press hotkey {'+'.join(self.keys)} (delay: {self.delay}s)"

class SpecialKeyAction(Action):
    """Action for pressing special keys"""
    
    def __init__(self, key: str, delay: float = 0):
        super().__init__(delay)
        self.key = key
        self.name = f"Special Key"
        self.description = f"Press {key} key"
    
    def _execute_impl(self) -> bool:
        """Execute the special key action"""
        logger.info(f"Pressing special key: {self.key}")
        pyautogui.press(self.key)
        return True
    
    def validate(self) -> bool:
        """Validate the special key action"""
        return isinstance(self.key, str) and self.key.strip() != ""
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["key"] = self.key
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.key = data.get("key", "enter")
        self.description = f"Press {self.key} key"
    
    def __str__(self):
        return f"Press {self.key} key (delay: {self.delay}s)"

class ScrollAction(Action):
    """Action for mouse scrolling"""
    
    def __init__(self, x: int, y: int, clicks: int = 3, direction: str = "up", delay: float = 0):
        super().__init__(delay)
        self.x = x
        self.y = y
        self.clicks = clicks
        self.direction = direction
        self.name = f"Scroll {direction.title()}"
        self.description = f"Scroll {direction} {clicks} clicks at ({x}, {y})"
    
    def _execute_impl(self) -> bool:
        """Execute the scroll action"""
        logger.info(f"Scrolling {self.direction} {self.clicks} clicks at ({self.x}, {self.y})")
        
        # Move to position first
        pyautogui.moveTo(self.x, self.y)
        
        # Scroll based on direction
        scroll_amount = self.clicks if self.direction == "up" else -self.clicks
        pyautogui.scroll(scroll_amount, x=self.x, y=self.y)
        
        return True
    
    def validate(self) -> bool:
        """Validate the scroll action"""
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            return False
        if not isinstance(self.clicks, int) or self.clicks <= 0:
            return False
        if self.direction not in ["up", "down"]:
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "x": self.x,
            "y": self.y,
            "clicks": self.clicks,
            "direction": self.direction
        })
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.clicks = data.get("clicks", 3)
        self.direction = data.get("direction", "up")
        self.description = f"Scroll {self.direction} {self.clicks} clicks at ({self.x}, {self.y})"
    
    def __str__(self):
        return f"Scroll {self.direction} {self.clicks} clicks at ({self.x}, {self.y}) (delay: {self.delay}s)"

class DragAction(Action):
    """Action for mouse dragging"""
    
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                 duration: float = 1.0, button: str = "left", delay: float = 0):
        super().__init__(delay)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.duration = duration
        self.button = button
        self.name = f"Drag {button.title()}"
        self.description = f"Drag from ({start_x}, {start_y}) to ({end_x}, {end_y})"
    
    def _execute_impl(self) -> bool:
        """Execute the drag action"""
        logger.info(f"Dragging from ({self.start_x}, {self.start_y}) to ({self.end_x}, {self.end_y})")
        pyautogui.drag(
            self.end_x - self.start_x, 
            self.end_y - self.start_y, 
            duration=self.duration,
            button=self.button
        )
        return True
    
    def validate(self) -> bool:
        """Validate the drag action"""
        coords = [self.start_x, self.start_y, self.end_x, self.end_y]
        if not all(isinstance(coord, int) for coord in coords):
            return False
        if not isinstance(self.duration, (int, float)) or self.duration <= 0:
            return False
        if self.button not in ["left", "right", "middle"]:
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "start_x": self.start_x,
            "start_y": self.start_y,
            "end_x": self.end_x,
            "end_y": self.end_y,
            "duration": self.duration,
            "button": self.button
        })
        return data
    
    def from_dict(self, data: Dict[str, Any]):
        super().from_dict(data)
        self.start_x = data.get("start_x", 0)
        self.start_y = data.get("start_y", 0)
        self.end_x = data.get("end_x", 0)
        self.end_y = data.get("end_y", 0)
        self.duration = data.get("duration", 1.0)
        self.button = data.get("button", "left")
        self.description = f"Drag from ({self.start_x}, {self.start_y}) to ({self.end_x}, {self.end_y})"
    
    def __str__(self):
        return f"Drag from ({self.start_x}, {self.start_y}) to ({self.end_x}, {self.end_y}) (delay: {self.delay}s)"

class ActionSequence:
    """Manages a sequence of actions for automation"""
    
    def __init__(self, name: str = "Untitled Sequence"):
        self.name = name
        self.actions: List[Action] = []
        self.created_at = time.time()
        self.modified_at = time.time()
        self.description = ""
        
        # Execution settings
        self.loop_enabled = False
        self.loop_count = 1
        self.repeat_interval = 0.0
        self.stop_on_error = True
        
        # Runtime state
        self.is_running = False
        self.current_action_index = 0
        self.current_loop = 0
    
    def add_action(self, action: Action) -> None:
        """Add an action to the sequence"""
        self.actions.append(action)
        self.modified_at = time.time()
        logger.info(f"Added action to sequence: {action}")
    
    def remove_action(self, index: int) -> bool:
        """Remove an action from the sequence"""
        if 0 <= index < len(self.actions):
            removed = self.actions.pop(index)
            self.modified_at = time.time()
            logger.info(f"Removed action from sequence: {removed}")
            return True
        return False
    
    def move_action(self, from_index: int, to_index: int) -> bool:
        """Move an action within the sequence"""
        if 0 <= from_index < len(self.actions) and 0 <= to_index < len(self.actions):
            action = self.actions.pop(from_index)
            self.actions.insert(to_index, action)
            self.modified_at = time.time()
            logger.info(f"Moved action from {from_index} to {to_index}")
            return True
        return False
    
    def clear(self) -> None:
        """Clear all actions from the sequence"""
        self.actions.clear()
        self.modified_at = time.time()
        logger.info("Cleared all actions from sequence")
    
    def validate(self) -> List[str]:
        """Validate the sequence and return any error messages"""
        errors = []
        
        if not self.actions:
            errors.append("Sequence is empty")
        
        for i, action in enumerate(self.actions):
            if not action.validate():
                errors.append(f"Action {i+1} is invalid: {action}")
        
        return errors
    
    def execute(self, progress_callback=None, stop_check=None) -> bool:
        """Execute the sequence"""
        self.is_running = True
        total_actions = len(self.actions)
        
        try:
            loop_count = self.loop_count if self.loop_enabled else 1
            
            for loop_index in range(loop_count):
                self.current_loop = loop_index + 1
                
                if stop_check and stop_check():
                    break
                
                for action_index, action in enumerate(self.actions):
                    self.current_action_index = action_index
                    
                    if stop_check and stop_check():
                        break
                    
                    if progress_callback:
                        progress_callback(loop_index, loop_count, action_index, total_actions, action)
                    
                    try:
                        success = action.execute()
                        if not success and self.stop_on_error:
                            logger.error(f"Action failed, stopping sequence: {action}")
                            return False
                    except ActionError as e:
                        logger.error(f"Action error: {e}")
                        if self.stop_on_error:
                            return False
                
                # Wait between loops if needed
                if self.loop_enabled and loop_index < loop_count - 1 and self.repeat_interval > 0:
                    if progress_callback:
                        progress_callback(loop_index, loop_count, -1, total_actions, None)
                    time.sleep(self.repeat_interval)
            
            return True
        finally:
            self.is_running = False
            self.current_action_index = 0
            self.current_loop = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sequence to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "loop_enabled": self.loop_enabled,
            "loop_count": self.loop_count,
            "repeat_interval": self.repeat_interval,
            "stop_on_error": self.stop_on_error,
            "actions": [action.to_dict() for action in self.actions]
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load sequence from dictionary"""
        self.name = data.get("name", "Untitled Sequence")
        self.description = data.get("description", "")
        self.created_at = data.get("created_at", time.time())
        self.modified_at = data.get("modified_at", time.time())
        self.loop_enabled = data.get("loop_enabled", False)
        self.loop_count = data.get("loop_count", 1)
        self.repeat_interval = data.get("repeat_interval", 0.0)
        self.stop_on_error = data.get("stop_on_error", True)
        
        self.actions = []
        for action_data in data.get("actions", []):
            try:
                action = Action.create_from_dict(action_data)
                self.actions.append(action)
            except Exception as e:
                logger.error(f"Failed to load action: {e}")
    
    def __str__(self):
        return f"ActionSequence '{self.name}' with {len(self.actions)} actions"