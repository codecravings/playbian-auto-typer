"""
Configuration file for Playbian Auto Typer & Clicker
Contains all constants, colors, and configuration settings
"""

import os
import json

# Application Constants
APP_NAME = "Playbian Auto Typer & Clicker"
APP_VERSION = "2.1"
APP_AUTHOR = "Playbian Team"

# Default window settings
DEFAULT_WINDOW_SIZE = "900x700"
MIN_WINDOW_SIZE = (800, 600)

# Automation settings
DEFAULT_PAUSE = 0.05  # 50ms pause between actions
FAILSAFE_ENABLED = True

# File extensions
SUPPORTED_FILE_EXTENSIONS = [
    ("JSON files", "*.json"),
    ("All files", "*.*")
]

# Dark Mode Color Palette (Modern Dark Theme)
COLORS_DARK = {
    # Primary backgrounds
    'bg_primary': '#1a1a1a',          # Main background
    'bg_secondary': '#2d2d2d',        # Secondary background
    'bg_tertiary': '#404040',         # Tertiary background
    
    # Accent colors
    'accent': '#4d79ff',              # Primary accent
    'accent_hover': '#3a66ff',        # Accent hover
    'accent_light': '#6b8bff',        # Light accent
    
    # Text colors
    'text_primary': '#ffffff',        # Main text
    'text_secondary': '#b3b3b3',      # Secondary text
    'text_muted': '#808080',          # Muted text
    'text_inverse': '#1a1a1a',        # Inverse text for buttons
    
    # Status colors
    'success': '#4caf50',             # Success color
    'success_hover': '#43a047',       # Success hover
    'warning': '#ff9800',             # Warning color
    'warning_hover': '#f57c00',       # Warning hover
    'danger': '#f44336',              # Danger color
    'danger_hover': '#e53935',        # Danger hover
    'info': '#2196f3',                # Info color
    
    # Border and input colors
    'border': '#404040',              # Border color
    'border_light': '#555555',        # Light border
    'input_bg': '#2d2d2d',            # Input background
    'input_border': '#555555',        # Input border
    'input_focus': '#4d79ff',         # Input focus border
    
    # Glass effect colors (for modern look)
    'glass_bg': '#2d2d2d80',          # Semi-transparent background
    'glass_border': '#55555580',      # Semi-transparent border
    'glass_shadow': '#00000040',      # Shadow for depth
    
    # Action type colors (darker variants)
    'type_action': '#1e3a5f',         # Dark blue for typing
    'click_action': '#5f4a1e',        # Dark yellow for clicking
    'delay_action': '#1e5f2b',        # Dark green for delay
    'hotkey_action': '#5f1e5a',       # Dark purple for hotkeys
    
    # Hover states for action types
    'type_action_hover': '#2d4d73',
    'click_action_hover': '#735a2d',
    'delay_action_hover': '#2d7339',
    'hotkey_action_hover': '#732d6b',
    
    # Tree/List colors
    'tree_bg': '#2d2d2d',
    'tree_select': '#4d79ff',
    'tree_alternate': '#333333',
    
    # Tooltip colors
    'tooltip_bg': '#404040',
    'tooltip_border': '#555555',
}

# Light Mode Color Palette (for future toggle)
COLORS_LIGHT = {
    'bg_primary': '#f0f5f9',
    'bg_secondary': '#e0e8f0',
    'accent': '#4d79ff',
    'accent_hover': '#3a66ff',
    'text_primary': '#2d3e50',
    'text_secondary': '#5d738d',
    'success': '#4caf50',
    'success_hover': '#43a047',
    'warning': '#ff9800',
    'danger': '#f44336',
    'danger_hover': '#e53935',
    'border': '#c9d6e5',
    'input_bg': '#ffffff',
    'input_border': '#c9d6e5',
    'glass_bg': '#ffffff',
    'glass_border': '#ffffff80',
    'glass_shadow': '#00000015',
    'type_action': '#e3f2fd',
    'click_action': '#fff8e1',
    'delay_action': '#e8f5e9',
    'hotkey_action': '#f3e5f5',
    'type_action_hover': '#bbdefb',
    'click_action_hover': '#ffecb3',
    'delay_action_hover': '#c8e6c9',
    'hotkey_action_hover': '#e1bee7',
}

# Current theme (can be toggled)
CURRENT_THEME = 'dark'
COLORS = COLORS_DARK  # Default to dark mode

# Emoji icons for modern UI
EMOJI = {
    'play': "▶️",
    'stop': "⏹️",
    'pause': "⏸️",
    'save': "💾",
    'load': "📂",
    'clear': "🧹",
    'up': "⬆️",
    'down': "⬇️",
    'delete': "🗑️",
    'edit': "✏️",
    'mouse': "🖱️",
    'keyboard': "⌨️",
    'delay': "⏱️",
    'hotkey': "🔑",
    'settings': "⚙️",
    'info': "ℹ️",
    'help': "❓",
    'copy': "📋",
    'paste': "📥",
    'new': "📄",
    'folder': "📁",
    'export': "📤",
    'import': "📥",
    'theme': "🎨",
    'api': "🔌",
    'ai': "🤖",
    'magic': "✨",
    'record': "⏺️",
    'refresh': "🔄",
}

# Special keys mapping
SPECIAL_KEYS = {
    "<enter>": "enter",
    "<tab>": "tab",
    "<space>": "space",
    "<backspace>": "backspace",
    "<delete>": "delete",
    "<escape>": "escape",
    "<shift>": "shift",
    "<ctrl>": "ctrl",
    "<alt>": "alt",
    "<caps_lock>": "capslock",
    "<page_up>": "pageup",
    "<page_down>": "pagedown",
    "<home>": "home",
    "<end>": "end",
    "<insert>": "insert",
    "<up>": "up",
    "<down>": "down",
    "<left>": "left",
    "<right>": "right",
    "<f1>": "f1", "<f2>": "f2", "<f3>": "f3", "<f4>": "f4",
    "<f5>": "f5", "<f6>": "f6", "<f7>": "f7", "<f8>": "f8",
    "<f9>": "f9", "<f10>": "f10", "<f11>": "f11", "<f12>": "f12",
}

# Keyboard shortcuts
SHORTCUTS = {
    'start_automation': 'F5',
    'stop_automation': 'Escape',
    'track_mouse': 'Control-t',  # Changed from F2 to Ctrl+T
    'save_sequence': 'Control-s',
    'load_sequence': 'Control-o',
    'new_sequence': 'Control-n',
    'delete_action': 'Delete',
    'edit_action': 'Return',
    'toggle_theme': 'Control-Shift-t',
    'show_help': 'F1',
}

# Font configuration
FONTS = {
    'default': ('Segoe UI', 9),
    'heading': ('Segoe UI', 14, 'bold'),
    'title': ('Segoe UI', 16, 'bold'),
    'small': ('Segoe UI', 8),
    'code': ('Consolas', 9),
    'large': ('Segoe UI', 12),
}

# Animation settings
ANIMATION = {
    'fade_steps': 10,
    'fade_delay': 20,
    'tooltip_delay': 500,
    'status_timeout': 3000,
}

# Default automation settings
DEFAULT_SETTINGS = {
    'loop_enabled': False,
    'loop_count': 1,
    'repeat_interval': 0.0,
    'countdown_enabled': True,
    'countdown_duration': 3,
    'auto_save': False,
    'confirm_clear': True,
    'position_tracking': False,
}

# Configuration file settings
CONFIG_DIR = os.path.expanduser("~/.playbian_auto_typer")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")
RECENT_FILES_FILE = os.path.join(CONFIG_DIR, "recent_files.json")
MAX_RECENT_FILES = 10

def ensure_config_dir():
    """Ensure the configuration directory exists"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

def load_settings():
    """Load settings from configuration file"""
    ensure_config_dir()
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to configuration file"""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")

def load_recent_files():
    """Load recent files list"""
    ensure_config_dir()
    try:
        if os.path.exists(RECENT_FILES_FILE):
            with open(RECENT_FILES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading recent files: {e}")
    return []

def save_recent_files(files):
    """Save recent files list"""
    ensure_config_dir()
    try:
        # Keep only the most recent files
        recent = files[:MAX_RECENT_FILES]
        with open(RECENT_FILES_FILE, 'w') as f:
            json.dump(recent, f, indent=2)
    except Exception as e:
        print(f"Error saving recent files: {e}")

def switch_theme(theme_name='dark'):
    """Switch between light and dark themes"""
    global COLORS, CURRENT_THEME
    CURRENT_THEME = theme_name
    if theme_name == 'dark':
        COLORS = COLORS_DARK
    else:
        COLORS = COLORS_LIGHT

# API Configuration (for future Gemini integration)
API_CONFIG = {
    'gemini': {
        'enabled': False,
        'api_key': '',
        'model': 'gemini-pro',
        'max_tokens': 1000,
        'temperature': 0.7,
    },
    'openai': {
        'enabled': False,
        'api_key': '',
        'model': 'gpt-3.5-turbo',
        'max_tokens': 1000,
        'temperature': 0.7,
    }
}

# Help text for special keys
SPECIAL_KEYS_HELP = """Special Keys Help:

You can use these special keys in your typing actions by enclosing them in angle brackets:

Navigation Keys:
• <enter> - Enter/Return key
• <tab> - Tab key
• <up>, <down>, <left>, <right> - Arrow keys
• <home>, <end> - Home and End keys
• <page_up>, <page_down> - Page navigation

Editing Keys:
• <space> - Space bar
• <backspace> - Backspace key
• <delete> - Delete key
• <insert> - Insert key

Modifier Keys:
• <shift> - Shift key
• <ctrl> - Control key
• <alt> - Alt key
• <caps_lock> - Caps Lock key

Function Keys:
• <f1> through <f12> - Function keys

System Keys:
• <escape> - Escape key

Example Usage:
"Hello<enter>World" → Types 'Hello', presses Enter, then types 'World'
"<ctrl>c" → Use this in hotkey actions, not typing actions
"Name:<tab>John Doe" → Types 'Name:', presses Tab, then types 'John Doe'
"""

# Logging configuration
LOGGING_CONFIG = {
    'enabled': True,
    'level': 'INFO',
    'file': os.path.join(CONFIG_DIR, 'app.log'),
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 3,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'encoding': 'utf-8'  # Fix for Unicode encoding issues
}