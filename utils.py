"""
Utility functions for Playbian Auto Typer & Clicker
Contains helper functions, validators, and common utilities
"""

import os
import sys
import json
import time
import hashlib
import platform
import subprocess
import logging
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading

from config import COLORS, FONTS, EMOJI

logger = logging.getLogger(__name__)

# System Information
def get_system_info() -> Dict[str, str]:
    """Get system information for debugging and compatibility"""
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'platform_release': platform.release(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'screen_size': f"{pyautogui.size().width}x{pyautogui.size().height}",
        'python_executable': sys.executable,
        'current_directory': os.getcwd()
    }

def is_windows() -> bool:
    """Check if running on Windows"""
    return platform.system().lower() == 'windows'

def is_mac() -> bool:
    """Check if running on macOS"""
    return platform.system().lower() == 'darwin'

def is_linux() -> bool:
    """Check if running on Linux"""
    return platform.system().lower() == 'linux'

# File Operations
def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if not"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_read_file(filepath: Union[str, Path], default: Any = None) -> Any:
    """Safely read and parse JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        logger.warning(f"Failed to read file {filepath}: {e}")
        return default

def safe_write_file(filepath: Union[str, Path], data: Any) -> bool:
    """Safely write data to JSON file"""
    try:
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (PermissionError, OSError) as e:
        logger.error(f"Failed to write file {filepath}: {e}")
        return False

def get_file_hash(filepath: Union[str, Path]) -> str:
    """Get MD5 hash of file for integrity checking"""
    try:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"Failed to get hash for {filepath}: {e}")
        return ""

def backup_file(filepath: Union[str, Path]) -> bool:
    """Create backup of file with timestamp"""
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            return False
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = filepath.with_suffix(f'.backup_{timestamp}{filepath.suffix}')
        
        import shutil
        shutil.copy2(filepath, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to backup file {filepath}: {e}")
        return False

# Data Validation
def validate_coordinates(x: int, y: int) -> Tuple[bool, str]:
    """Validate screen coordinates"""
    try:
        screen_width, screen_height = pyautogui.size()
        
        if not isinstance(x, int) or not isinstance(y, int):
            return False, "Coordinates must be integers"
        
        if x < 0 or y < 0:
            return False, "Coordinates cannot be negative"
        
        if x >= screen_width or y >= screen_height:
            return False, f"Coordinates exceed screen size ({screen_width}x{screen_height})"
        
        return True, "Valid coordinates"
    except Exception as e:
        return False, f"Error validating coordinates: {e}"

def validate_delay(delay: float) -> Tuple[bool, str]:
    """Validate delay value"""
    try:
        if not isinstance(delay, (int, float)):
            return False, "Delay must be a number"
        
        if delay < 0:
            return False, "Delay cannot be negative"
        
        if delay > 300:  # 5 minutes max
            return False, "Delay too long (max 300 seconds)"
        
        return True, "Valid delay"
    except Exception as e:
        return False, f"Error validating delay: {e}"

def validate_hotkey_keys(keys: List[str]) -> Tuple[bool, str]:
    """Validate hotkey key combination"""
    try:
        if not isinstance(keys, list) or not keys:
            return False, "Keys must be a non-empty list"
        
        valid_keys = {
            'ctrl', 'control', 'alt', 'shift', 'win', 'windows', 'cmd', 'command',
            'tab', 'enter', 'escape', 'space', 'backspace', 'delete', 'home', 'end',
            'pageup', 'pagedown', 'up', 'down', 'left', 'right', 'insert',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
        }
        
        # Add letters and numbers
        valid_keys.update(set('abcdefghijklmnopqrstuvwxyz'))
        valid_keys.update(set('0123456789'))
        
        for key in keys:
            if not isinstance(key, str):
                return False, f"Key '{key}' must be a string"
            
            if key.lower() not in valid_keys:
                return False, f"Invalid key: '{key}'"
        
        return True, "Valid hotkey combination"
    except Exception as e:
        return False, f"Error validating keys: {e}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for cross-platform compatibility"""
    # Remove/replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    # Ensure it's not empty
    if not filename:
        filename = "untitled"
    
    return filename

# Screen and Display Utilities
def get_screen_info() -> Dict[str, Any]:
    """Get detailed screen information"""
    try:
        size = pyautogui.size()
        return {
            'width': size.width,
            'height': size.height,
            'center_x': size.width // 2,
            'center_y': size.height // 2,
            'aspect_ratio': round(size.width / size.height, 2)
        }
    except Exception as e:
        logger.error(f"Failed to get screen info: {e}")
        return {'width': 1920, 'height': 1080, 'center_x': 960, 'center_y': 540, 'aspect_ratio': 1.78}

def capture_screenshot(save_path: Optional[str] = None) -> Optional[str]:
    """Capture screenshot and optionally save to file"""
    try:
        import tempfile
        
        if save_path is None:
            # Generate temporary filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            temp_dir = tempfile.gettempdir()
            save_path = os.path.join(temp_dir, f"playbian_screenshot_{timestamp}.png")
        
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        logger.info(f"Screenshot saved to {save_path}")
        return save_path
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return None

def find_image_on_screen(image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """Find image on screen and return center coordinates"""
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            return (center.x, center.y)
        return None
    except Exception as e:
        logger.warning(f"Failed to find image {image_path}: {e}")
        return None

# Performance and Monitoring
def measure_execution_time(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper

def get_memory_usage() -> Dict[str, float]:
    """Get current memory usage information"""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size in MB
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size in MB
            'percent': process.memory_percent()
        }
    except ImportError:
        logger.warning("psutil not available for memory monitoring")
        return {'rss_mb': 0, 'vms_mb': 0, 'percent': 0}

def monitor_system_resources() -> Dict[str, Any]:
    """Monitor system resources"""
    try:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / 1024 / 1024 / 1024,
            'disk_percent': disk.percent,
            'disk_free_gb': disk.free / 1024 / 1024 / 1024
        }
    except ImportError:
        logger.warning("psutil not available for system monitoring")
        return {}

# Threading Utilities
class SafeThread(threading.Thread):
    """Thread class with exception handling"""
    
    def __init__(self, target=None, name=None, args=(), kwargs=None):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs or {})
        self.exception = None
        self.result = None
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}
    
    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exception = e
            logger.error(f"Thread {self.name} failed: {e}")
    
    def join(self, timeout=None):
        super().join(timeout)
        if self.exception:
            raise self.exception
        return self.result

def run_in_thread(func, *args, **kwargs):
    """Run function in a separate thread"""
    thread = SafeThread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread

# UI Utilities
def center_window(window, width: int, height: int):
    """Center a tkinter window on screen"""
    window.update_idletasks()
    
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_gradient_frame(parent, color1: str, color2: str, width: int, height: int):
    """Create a frame with gradient background (using Canvas)"""
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    
    # Create gradient effect by drawing multiple rectangles
    steps = 50
    for i in range(steps):
        # Interpolate between colors
        ratio = i / steps
        r1, g1, b1 = parent.winfo_rgb(color1)
        r2, g2, b2 = parent.winfo_rgb(color2)
        
        r = int(r1 + (r2 - r1) * ratio) // 256
        g = int(g1 + (g2 - g1) * ratio) // 256
        b = int(b1 + (b2 - b1) * ratio) // 256
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        
        y1 = int(height * i / steps)
        y2 = int(height * (i + 1) / steps)
        
        canvas.create_rectangle(0, y1, width, y2, fill=color, outline=color)
    
    return canvas

def show_notification(title: str, message: str, duration: int = 3000):
    """Show a temporary notification window"""
    notification = tk.Toplevel()
    notification.title(title)
    notification.configure(bg=COLORS['bg_secondary'])
    notification.overrideredirect(True)  # Remove window decorations
    
    # Create content
    frame = tk.Frame(notification, bg=COLORS['bg_secondary'], padx=20, pady=10)
    frame.pack()
    
    title_label = tk.Label(frame, text=title, font=FONTS['heading'],
                          bg=COLORS['bg_secondary'], fg=COLORS['text_primary'])
    title_label.pack()
    
    msg_label = tk.Label(frame, text=message, font=FONTS['default'],
                        bg=COLORS['bg_secondary'], fg=COLORS['text_secondary'],
                        wraplength=300)
    msg_label.pack(pady=(5, 0))
    
    # Position notification
    notification.update_idletasks()
    width = notification.winfo_reqwidth()
    height = notification.winfo_reqheight()
    
    screen_width = notification.winfo_screenwidth()
    screen_height = notification.winfo_screenheight()
    
    x = screen_width - width - 20
    y = screen_height - height - 50
    
    notification.geometry(f"+{x}+{y}")
    
    # Auto-close after duration
    notification.after(duration, notification.destroy)
    
    return notification

def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Required to make the clipboard copy work
        root.destroy()
        return True
    except Exception as e:
        logger.error(f"Failed to copy to clipboard: {e}")
        return False

def get_clipboard_text() -> str:
    """Get text from system clipboard"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        return text
    except Exception as e:
        logger.error(f"Failed to get clipboard text: {e}")
        return ""

# Format and Display Utilities
def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs:.1f}s"

def format_file_size(bytes_size: int) -> str:
    """Format file size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def escape_special_chars(text: str) -> str:
    """Escape special characters for safe display"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# Error Handling and Logging Utilities
def setup_error_logging(log_file: str = None):
    """Setup comprehensive error logging"""
    if log_file is None:
        from config import LOGGING_CONFIG
        log_file = LOGGING_CONFIG['file']
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir:
        ensure_directory(log_dir)
    
    # Configure logging with rotation
    try:
        from logging.handlers import RotatingFileHandler
        
        handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
    except Exception as e:
        print(f"Failed to setup rotating log handler: {e}")

def log_system_info():
    """Log system information for debugging"""
    info = get_system_info()
    logger.info("=== System Information ===")
    for key, value in info.items():
        logger.info(f"{key}: {value}")
    logger.info("=" * 30)

def handle_unexpected_error(error: Exception, context: str = ""):
    """Handle unexpected errors with proper logging and user notification"""
    error_msg = f"Unexpected error in {context}: {str(error)}"
    logger.error(error_msg, exc_info=True)
    
    # Show user-friendly error message
    try:
        messagebox.showerror(
            "Unexpected Error",
            f"An unexpected error occurred:\n\n{str(error)}\n\n"
            "Please check the logs for more details."
        )
    except:
        # If GUI is not available, print to console
        print(f"ERROR: {error_msg}")

# Development and Debug Utilities
def debug_print(message: str, level: str = "DEBUG"):
    """Print debug message with timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def profile_function(func):
    """Decorator to profile function performance"""
    def wrapper(*args, **kwargs):
        import cProfile
        import pstats
        import io
        
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        
        # Print stats
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats(10)  # Top 10 functions
        
        logger.debug(f"Profile for {func.__name__}:\n{s.getvalue()}")
        
        return result
    return wrapper

def check_dependencies() -> Dict[str, bool]:
    """Check if all required dependencies are available"""
    dependencies = {
        'tkinter': True,  # Built-in
        'pyautogui': False,
        'keyboard': False,
        'requests': False,  # For API integration
        'psutil': False,    # Optional, for system monitoring
        'pillow': False     # For image operations
    }
    
    for module in dependencies.keys():
        try:
            __import__(module)
            dependencies[module] = True
        except ImportError:
            dependencies[module] = False
    
    return dependencies

def generate_error_report() -> str:
    """Generate comprehensive error report for troubleshooting"""
    report = []
    report.append("=== PLAYBIAN AUTO TYPER ERROR REPORT ===")
    report.append(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # System info
    report.append("System Information:")
    for key, value in get_system_info().items():
        report.append(f"  {key}: {value}")
    report.append("")
    
    # Dependencies
    report.append("Dependencies:")
    deps = check_dependencies()
    for module, available in deps.items():
        status = "✓" if available else "✗"
        report.append(f"  {status} {module}")
    report.append("")
    
    # Memory usage
    memory = get_memory_usage()
    if memory:
        report.append("Memory Usage:")
        for key, value in memory.items():
            report.append(f"  {key}: {value}")
        report.append("")
    
    # Recent log entries (if available)
    try:
        from config import LOGGING_CONFIG
        log_file = LOGGING_CONFIG['file']
        if os.path.exists(log_file):
            report.append("Recent Log Entries (last 20 lines):")
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    report.append(f"  {line.strip()}")
    except:
        report.append("Could not read log file")
    
    report.append("")
    report.append("=== END OF REPORT ===")
    
    return "\n".join(report)
