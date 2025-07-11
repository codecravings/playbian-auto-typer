"""
Main application file for Playbian Auto Typer & Clicker
Enhanced version with dark mode, better organization, and modern UI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
import threading
import time
import json
import os
import sys
import logging
import pyautogui
import keyboard
from typing import Optional, List, Dict, Any

# Import our modules
from config import *
from actions import *
from ui_components import *

# Setup logging
def setup_logging():
    """Setup application logging"""
    ensure_config_dir()
    
    # Configure basic logging with UTF-8 encoding
    import logging.handlers
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler (compatible with older Python versions)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with UTF-8 encoding and rotation
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            LOGGING_CONFIG['file'],
            maxBytes=LOGGING_CONFIG['max_size'],
            backupCount=LOGGING_CONFIG['backup_count'],
            encoding='utf-8'
        )
        
        file_formatter = logging.Formatter(LOGGING_CONFIG['format'])
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")
    
    # Set encoding for stdout to handle Unicode (Python 3.7+)
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        elif hasattr(sys.stdout, 'buffer'):
            # For older Python versions, try to set environment variable
            os.environ['PYTHONIOENCODING'] = 'utf-8'
    except Exception:
        # Fallback: just set environment variable
        os.environ['PYTHONIOENCODING'] = 'utf-8'

setup_logging()
logger = logging.getLogger(__name__)

class PlaybianAutoTyper:
    """Main application class with modern dark UI and enhanced features"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Application state
        self.action_sequence = ActionSequence("New Sequence")
        self.is_running = False
        self.run_thread = None
        self.position_tracking = False
        self.current_file = None
        self.settings = load_settings()
        self.recent_files = load_recent_files()
        
        # UI state variables
        self.setup_variables()
        
        # Setup UI
        self.setup_styles()
        self.setup_menu()
        self.setup_ui()
        self.setup_shortcuts()
        
        # Start mouse position tracking
        self.start_position_tracking()
        
        # Load settings
        self.apply_settings()
        
        logger.info(f"{APP_NAME} v{APP_VERSION} started")
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Try to set window icon
        try:
            if sys.platform.startswith('win'):
                self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_variables(self):
        """Setup tkinter variables"""
        self.loop_var = tk.BooleanVar(value=self.settings.get('loop_enabled', False))
        self.loop_count_var = tk.IntVar(value=self.settings.get('loop_count', 1))
        self.repeat_interval_var = tk.DoubleVar(value=self.settings.get('repeat_interval', 0.0))
        self.countdown_var = tk.BooleanVar(value=self.settings.get('countdown_enabled', True))
        self.auto_save_var = tk.BooleanVar(value=self.settings.get('auto_save', False))
        
        # Input variables
        self.type_text_var = tk.StringVar()
        self.type_delay_var = tk.DoubleVar(value=0.0)
        self.click_x_var = tk.IntVar(value=0)
        self.click_y_var = tk.IntVar(value=0)
        self.click_button_var = tk.StringVar(value="left")
        self.click_delay_var = tk.DoubleVar(value=0.0)
        self.wait_time_var = tk.DoubleVar(value=1.0)
        self.hotkey_keys_var = tk.StringVar(value="ctrl,c")
        self.hotkey_delay_var = tk.DoubleVar(value=0.0)
        self.special_key_delay_var = tk.DoubleVar(value=0.0)
    
    def setup_styles(self):
        """Setup application styles"""
        ModernStyle.setup_styles()
    
    def setup_menu(self):
        """Setup application menu bar"""
        menubar = Menu(self.root)
        menubar.configure(
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['accent'],
            activeforeground='white',
            font=FONTS['default']
        )
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        self._configure_menu(file_menu)
        
        file_menu.add_command(label=f"{EMOJI['new']} New", 
                            command=self.new_sequence, 
                            accelerator=SHORTCUTS['new_sequence'])
        file_menu.add_command(label=f"{EMOJI['load']} Open...", 
                            command=self.load_sequence, 
                            accelerator=SHORTCUTS['load_sequence'])
        
        # Recent files submenu
        self.recent_menu = Menu(file_menu, tearoff=0)
        self._configure_menu(self.recent_menu)
        self._update_recent_menu()
        file_menu.add_cascade(label=f"{EMOJI['folder']} Recent Files", menu=self.recent_menu)
        
        file_menu.add_separator()
        file_menu.add_command(label=f"{EMOJI['save']} Save", 
                            command=self.save_sequence, 
                            accelerator=SHORTCUTS['save_sequence'])
        file_menu.add_command(label=f"{EMOJI['export']} Save As...", 
                            command=self.save_sequence_as)
        file_menu.add_separator()
        file_menu.add_command(label=f"{EMOJI['settings']} Settings", 
                            command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = Menu(menubar, tearoff=0)
        self._configure_menu(edit_menu)
        
        edit_menu.add_command(label=f"{EMOJI['delete']} Delete Selected", 
                            command=self.delete_selected_action,
                            accelerator=SHORTCUTS['delete_action'])
        edit_menu.add_command(label=f"{EMOJI['edit']} Edit Selected", 
                            command=self.edit_selected_action,
                            accelerator=SHORTCUTS['edit_action'])
        edit_menu.add_command(label=f"{EMOJI['copy']} Duplicate Selected", 
                            command=self.duplicate_selected_action,
                            accelerator="Ctrl+D")
        edit_menu.add_separator()
        edit_menu.add_command(label=f"{EMOJI['clear']} Clear All", 
                            command=self.clear_all_actions)
        
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Automation menu
        automation_menu = Menu(menubar, tearoff=0)
        self._configure_menu(automation_menu)
        
        automation_menu.add_command(label=f"{EMOJI['play']} Start Automation", 
                                  command=self.start_automation,
                                  accelerator=SHORTCUTS['start_automation'])
        automation_menu.add_command(label=f"{EMOJI['stop']} Stop Automation", 
                                  command=self.stop_automation,
                                  accelerator=SHORTCUTS['stop_automation'])
        automation_menu.add_separator()
        automation_menu.add_checkbutton(label=f"{EMOJI['mouse']} Track Mouse Position", 
                                      command=self.toggle_mouse_tracking,
                                      variable=self.position_tracking,
                                      accelerator=SHORTCUTS['track_mouse'])
        
        menubar.add_cascade(label="Automation", menu=automation_menu)
        
        # View menu
        view_menu = Menu(menubar, tearoff=0)
        self._configure_menu(view_menu)
        
        view_menu.add_command(label=f"{EMOJI['theme']} Toggle Theme", 
                            command=self.toggle_theme,
                            accelerator=SHORTCUTS['toggle_theme'])
        view_menu.add_command(label=f"{EMOJI['refresh']} Refresh UI", 
                            command=self.refresh_ui)
        
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        self._configure_menu(help_menu)
        
        help_menu.add_command(label=f"{EMOJI['help']} Special Keys Help", 
                            command=self.show_special_keys_help,
                            accelerator=SHORTCUTS['show_help'])
        help_menu.add_command(label=f"{EMOJI['keyboard']} Keyboard Shortcuts", 
                            command=self.show_shortcuts_help)
        help_menu.add_separator()
        help_menu.add_command(label=f"{EMOJI['info']} About", 
                            command=self.show_about)
        
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _configure_menu(self, menu):
        """Configure menu styling"""
        menu.configure(
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['accent'],
            activeforeground='white',
            font=FONTS['default'],
            bd=0
        )
    
    def _update_recent_menu(self):
        """Update recent files menu"""
        self.recent_menu.delete(0, 'end')
        
        if not self.recent_files:
            self.recent_menu.add_command(label="No recent files", state='disabled')
            return
        
        for file_path in self.recent_files:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                self.recent_menu.add_command(
                    label=filename,
                    command=lambda path=file_path: self.load_file(path)
                )
        
        if self.recent_files:
            self.recent_menu.add_separator()
            self.recent_menu.add_command(
                label="Clear Recent Files",
                command=self.clear_recent_files
            )
    
    def setup_ui(self):
        """Setup main user interface"""
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.setup_header()
        
        # Toolbar
        self.setup_toolbar()
        
        # Content area (notebook with action inputs and list)
        self.setup_content_area()
        
        # Status bar
        self.status_bar = StatusBar(self.main_container)
        self.status_bar.pack(side='bottom', fill='x', pady=(5, 0))
    
    def setup_header(self):
        """Setup application header"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Title and version
        title_label = ttk.Label(header_frame, text=APP_NAME, style='Title.TLabel')
        title_label.pack(side='left')
        
        version_label = ttk.Label(header_frame, text=f"v{APP_VERSION}", style='Secondary.TLabel')
        version_label.pack(side='left', padx=(10, 0))
        
        # File info
        self.file_label = ttk.Label(header_frame, text="Untitled", style='Secondary.TLabel')
        self.file_label.pack(side='right')
    
    def setup_toolbar(self):
        """Setup main toolbar"""
        toolbar = ttk.Frame(self.main_container, style='Card.TFrame')
        toolbar.pack(fill='x', pady=(0, 10))
        
        # Create inner frame for better padding
        toolbar_inner = ttk.Frame(toolbar)
        toolbar_inner.pack(fill='x', padx=10, pady=8)
        
        # Automation controls
        self.start_btn = ttk.Button(toolbar_inner, 
                                   text=f"{EMOJI['play']} Start",
                                   command=self.start_automation,
                                   style='Success.TButton')
        self.start_btn.pack(side='left', padx=(0, 5))
        ToolTip(self.start_btn, f"Start automation ({SHORTCUTS['start_automation']})")
        
        self.stop_btn = ttk.Button(toolbar_inner,
                                  text=f"{EMOJI['stop']} Stop",
                                  command=self.stop_automation,
                                  style='Danger.TButton')
        self.stop_btn.pack(side='left', padx=5)
        self.stop_btn.state(['disabled'])
        ToolTip(self.stop_btn, f"Stop automation ({SHORTCUTS['stop_automation']})")
        
        ttk.Separator(toolbar_inner, orient='vertical').pack(side='left', fill='y', padx=10)
        
        # File controls
        ttk.Button(toolbar_inner,
                  text=f"{EMOJI['new']}",
                  command=self.new_sequence,
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Button(toolbar_inner,
                  text=f"{EMOJI['load']}",
                  command=self.load_sequence,
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Button(toolbar_inner,
                  text=f"{EMOJI['save']}",
                  command=self.save_sequence,
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Separator(toolbar_inner, orient='vertical').pack(side='left', fill='y', padx=10)
        
        # Loop controls
        loop_frame = ttk.Frame(toolbar_inner)
        loop_frame.pack(side='left', padx=5)
        
        ttk.Checkbutton(loop_frame, text="Loop", variable=self.loop_var).pack(side='left')
        
        ttk.Label(loop_frame, text="Count:", style='Card.TLabel').pack(side='left', padx=(10, 5))
        count_spin = ttk.Spinbox(loop_frame, from_=1, to=999, width=5, 
                               textvariable=self.loop_count_var)
        count_spin.pack(side='left', padx=2)
        
        ttk.Label(loop_frame, text="Interval:", style='Card.TLabel').pack(side='left', padx=(10, 5))
        interval_spin = ttk.Spinbox(loop_frame, from_=0, to=60, width=6, 
                                  increment=0.5, textvariable=self.repeat_interval_var)
        interval_spin.pack(side='left', padx=2)
        
        # Track position button
        self.track_btn = ttk.Button(toolbar_inner,
                                   text=f"{EMOJI['mouse']} Track",
                                   command=self.toggle_mouse_tracking,
                                   style='Primary.TButton')
        self.track_btn.pack(side='right', padx=5)
        ToolTip(self.track_btn, f"Toggle mouse tracking ({SHORTCUTS['track_mouse']})")
    
    def setup_content_area(self):
        """Setup main content area with notebook"""
        # Create paned window for resizable layout
        paned = ttk.PanedWindow(self.main_container, orient='horizontal')
        paned.pack(fill='both', expand=True)
        
        # Left side - Action inputs
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        self.setup_action_inputs(left_frame)
        
        # Right side - Action list
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        self.setup_action_list(right_frame)
    
    def setup_action_inputs(self, parent):
        """Setup action input controls"""
        # Action input notebook
        input_frame = ttk.LabelFrame(parent, text="Add Actions", style='Card.TLabelframe')
        input_frame.pack(fill='both', expand=True, padx=(0, 5))
        
        self.input_notebook = ttk.Notebook(input_frame)
        self.input_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Type action tab
        self.setup_type_tab()
        
        # Click action tab
        self.setup_click_tab()
        
        # Delay action tab
        self.setup_delay_tab()
        
        # Hotkey action tab
        self.setup_hotkey_tab()
        
        # Special keys tab
        self.setup_special_keys_tab()
    
    def setup_type_tab(self):
        """Setup typing action tab"""
        type_frame = ttk.Frame(self.input_notebook)
        self.input_notebook.add(type_frame, text=f"{EMOJI['keyboard']} Type")
        
        container = ttk.Frame(type_frame)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text input
        ttk.Label(container, text="Text to type:").grid(row=0, column=0, sticky='w', pady=5)
        
        text_frame = ttk.Frame(container)
        text_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=5)
        
        self.type_entry = tk.Text(text_frame, height=4, font=FONTS['default'],
                                 bg=COLORS['input_bg'], fg=COLORS['text_primary'],
                                 insertbackground=COLORS['text_primary'],
                                 wrap='word', relief='solid', bd=1)
        self.type_entry.pack(side='left', fill='both', expand=True)
        
        type_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', 
                                     command=self.type_entry.yview)
        type_scrollbar.pack(side='right', fill='y')
        self.type_entry.configure(yscrollcommand=type_scrollbar.set)
        
        # Delay input
        ttk.Label(container, text="Delay (seconds):").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Spinbox(container, from_=0, to=60, width=10, increment=0.1,
                   textvariable=self.type_delay_var).grid(row=2, column=1, sticky='w', pady=5)
        
        # Help button
        ttk.Button(container, text="?", width=3,
                  command=self.show_special_keys_help,
                  style='Small.TButton').grid(row=2, column=2, sticky='e', padx=10, pady=5)
        
        # Add button
        ttk.Button(container, text=f"{EMOJI['keyboard']} Add Typing Action",
                  command=self.add_type_action,
                  style='Primary.TButton').grid(row=3, column=0, columnspan=3, pady=10)
        
        container.columnconfigure(1, weight=1)
    
    def setup_click_tab(self):
        """Setup click action tab"""
        click_frame = ttk.Frame(self.input_notebook)
        self.input_notebook.add(click_frame, text=f"{EMOJI['mouse']} Click")
        
        container = ttk.Frame(click_frame)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Position inputs
        pos_frame = ttk.Frame(container)
        pos_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=5)
        
        ttk.Label(pos_frame, text="X:").grid(row=0, column=0, sticky='w', padx=5)
        ttk.Entry(pos_frame, width=8, textvariable=self.click_x_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(pos_frame, text="Y:").grid(row=0, column=2, sticky='w', padx=5)
        ttk.Entry(pos_frame, width=8, textvariable=self.click_y_var).grid(row=0, column=3, padx=5)
        
        # Button selection
        ttk.Label(container, text="Button:").grid(row=1, column=0, sticky='w', pady=5)
        button_combo = ttk.Combobox(container, values=["left", "right", "middle"],
                                   textvariable=self.click_button_var, width=10)
        button_combo.grid(row=1, column=1, sticky='w', pady=5)
        button_combo.current(0)
        
        # Delay input
        ttk.Label(container, text="Delay (seconds):").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Spinbox(container, from_=0, to=60, width=10, increment=0.1,
                   textvariable=self.click_delay_var).grid(row=2, column=1, sticky='w', pady=5)
        
        # Add button
        ttk.Button(container, text=f"{EMOJI['mouse']} Add Click Action",
                  command=self.add_click_action,
                  style='Primary.TButton').grid(row=3, column=0, columnspan=3, pady=10)
        
        container.columnconfigure(1, weight=1)
    
    def setup_delay_tab(self):
        """Setup delay action tab"""
        delay_frame = ttk.Frame(self.input_notebook)
        self.input_notebook.add(delay_frame, text=f"{EMOJI['delay']} Delay")
        
        container = ttk.Frame(delay_frame)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Center the controls
        center_frame = ttk.Frame(container)
        center_frame.pack(expand=True)
        
        ttk.Label(center_frame, text="Wait time (seconds):").grid(row=0, column=0, padx=5, pady=20)
        ttk.Spinbox(center_frame, from_=0.1, to=300, width=10, increment=0.5,
                   textvariable=self.wait_time_var).grid(row=0, column=1, padx=5, pady=20)
        
        ttk.Button(center_frame, text=f"{EMOJI['delay']} Add Delay",
                  command=self.add_delay_action,
                  style='Primary.TButton').grid(row=1, column=0, columnspan=2, pady=10)
    
    def setup_hotkey_tab(self):
        """Setup hotkey action tab"""
        hotkey_frame = ttk.Frame(self.input_notebook)
        self.input_notebook.add(hotkey_frame, text=f"{EMOJI['hotkey']} Hotkey")
        
        container = ttk.Frame(hotkey_frame)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Keys input
        ttk.Label(container, text="Keys (comma separated):").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(container, width=30, textvariable=self.hotkey_keys_var).grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Examples
        examples = "Examples: ctrl,c | alt,tab | win,r | ctrl,shift,esc"
        ttk.Label(container, text=examples, style='Secondary.TLabel').grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        # Delay input
        ttk.Label(container, text="Delay (seconds):").grid(row=3, column=0, sticky='w', pady=5)
        ttk.Spinbox(container, from_=0, to=60, width=10, increment=0.1,
                   textvariable=self.hotkey_delay_var).grid(row=3, column=1, sticky='w', pady=5)
        
        # Add button
        ttk.Button(container, text=f"{EMOJI['hotkey']} Add Hotkey",
                  command=self.add_hotkey_action,
                  style='Primary.TButton').grid(row=4, column=0, columnspan=2, pady=15)
        
        container.columnconfigure(0, weight=1)
    
    def setup_special_keys_tab(self):
        """Setup special keys tab"""
        special_frame = ttk.Frame(self.input_notebook)
        self.input_notebook.add(special_frame, text=f"{EMOJI['keyboard']} Special")
        
        # Create scrollable frame for special keys
        canvas = tk.Canvas(special_frame, bg=COLORS['bg_secondary'], 
                          highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(special_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Create special key buttons
        self.create_special_key_buttons(scrollable_frame)
        
        # Delay control at bottom
        delay_frame = ttk.Frame(special_frame)
        delay_frame.pack(side='bottom', fill='x', padx=10, pady=5)
        
        ttk.Label(delay_frame, text="Delay (seconds):").pack(side='left')
        ttk.Spinbox(delay_frame, from_=0, to=60, width=8, increment=0.1,
                   textvariable=self.special_key_delay_var).pack(side='left', padx=10)
    
    def create_special_key_buttons(self, parent):
        """Create buttons for special keys"""
        # Group special keys by category
        key_categories = {
            "Navigation": ["enter", "tab", "escape", "up", "down", "left", "right", 
                          "home", "end", "page_up", "page_down"],
            "Editing": ["backspace", "delete", "space", "insert"],
            "Modifiers": ["shift", "ctrl", "alt", "caps_lock"],
            "Function Keys": [f"f{i}" for i in range(1, 13)]
        }
        
        row = 0
        for category, keys in key_categories.items():
            # Category header
            ttk.Label(parent, text=category, style='Heading.TLabel').grid(
                row=row, column=0, columnspan=4, sticky='w', padx=5, pady=(10, 5))
            row += 1
            
            # Create buttons for keys in this category
            col = 0
            for key_name in keys:
                display_name = key_name.replace('_', ' ').title()
                
                btn = ttk.Button(parent, text=display_name,
                               command=lambda k=key_name: self.add_special_key_action(k),
                               style='Small.TButton')
                btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
                
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
            
            if col > 0:  # If we didn't fill the last row
                row += 1
        
        # Make columns expandable
        for i in range(4):
            parent.columnconfigure(i, weight=1)
    
    def setup_action_list(self, parent):
        """Setup action list display"""
        list_frame = ttk.LabelFrame(parent, text="Action Sequence", style='Card.TLabelframe')
        list_frame.pack(fill='both', expand=True, padx=(5, 0))
        
        # Action list
        self.action_list = ActionListView(list_frame, self.handle_action_list_event)
        self.action_list.pack(fill='both', expand=True, padx=10, pady=10)
        
        # List control buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(side='bottom', fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text=f"{EMOJI['up']} Up",
                  command=lambda: self.handle_action_list_event("moveup"),
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Button(btn_frame, text=f"{EMOJI['down']} Down",
                  command=lambda: self.handle_action_list_event("movedown"),
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Button(btn_frame, text=f"{EMOJI['edit']} Edit",
                  command=lambda: self.handle_action_list_event("edit"),
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Button(btn_frame, text=f"{EMOJI['copy']} Duplicate",
                  command=lambda: self.handle_action_list_event("duplicate"),
                  style='Small.TButton').pack(side='left', padx=2)
        
        ttk.Button(btn_frame, text=f"{EMOJI['delete']} Delete",
                  command=lambda: self.handle_action_list_event("delete"),
                  style='Danger.TButton').pack(side='right', padx=2)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Bind shortcuts to root window
        shortcuts_map = {
            f"<{SHORTCUTS['start_automation']}>": lambda e: self.start_automation(),
            f"<{SHORTCUTS['stop_automation']}>": lambda e: self.stop_automation(),
            f"<{SHORTCUTS['track_mouse']}>": lambda e: self.toggle_mouse_tracking(),
            f"<{SHORTCUTS['save_sequence']}>": lambda e: self.save_sequence(),
            f"<{SHORTCUTS['load_sequence']}>": lambda e: self.load_sequence(),
            f"<{SHORTCUTS['new_sequence']}>": lambda e: self.new_sequence(),
            f"<{SHORTCUTS['delete_action']}>": lambda e: self.delete_selected_action(),
            f"<{SHORTCUTS['edit_action']}>": lambda e: self.edit_selected_action(),
            f"<{SHORTCUTS['toggle_theme']}>": lambda e: self.toggle_theme(),
            f"<{SHORTCUTS['show_help']}>": lambda e: self.show_special_keys_help(),
            "<Control-d>": lambda e: self.duplicate_selected_action(),
        }
        
        for shortcut, handler in shortcuts_map.items():
            self.root.bind(shortcut, handler)
        
        # Setup global hotkeys using keyboard library (with error handling)
        try:
            # Only set up hotkeys if keyboard library is available and working
            # Use suppress=False to avoid conflicts with GUI events
            keyboard.add_hotkey('f5', self.start_automation, suppress=False)  
            keyboard.add_hotkey('esc', self.stop_automation, suppress=False)
            logger.info("Global hotkeys configured successfully")
            
            # Don't set up global Ctrl+T to avoid conflicts with button
            # User can use the button or menu instead
        except Exception as e:
            logger.warning(f"Could not setup global hotkeys: {e}")
            logger.info("Global hotkeys disabled, but keyboard shortcuts within the app will still work")
    
    def start_position_tracking(self):
        """Start tracking mouse position"""
        self._last_position = (0, 0)
        
        def update_position():
            try:
                x, y = pyautogui.position()
                
                # Only update if position changed significantly (reduce spam)
                if abs(x - self._last_position[0]) > 5 or abs(y - self._last_position[1]) > 5:
                    self.status_bar.set_position(x, y)
                    self._last_position = (x, y)
                
                if self.position_tracking:
                    self.click_x_var.set(x)
                    self.click_y_var.set(y)
                    
            except Exception as e:
                logger.error(f"Error tracking mouse position: {e}")
            
            self.root.after(200, update_position)  # Reduced frequency from 100ms to 200ms
        
        update_position()
    
    def apply_settings(self):
        """Apply loaded settings to UI"""
        self.loop_var.set(self.settings.get('loop_enabled', False))
        self.loop_count_var.set(self.settings.get('loop_count', 1))
        self.repeat_interval_var.set(self.settings.get('repeat_interval', 0.0))
        self.countdown_var.set(self.settings.get('countdown_enabled', True))
        self.auto_save_var.set(self.settings.get('auto_save', False))
    
    def save_settings(self):
        """Save current settings"""
        self.settings.update({
            'loop_enabled': self.loop_var.get(),
            'loop_count': self.loop_count_var.get(),
            'repeat_interval': self.repeat_interval_var.get(),
            'countdown_enabled': self.countdown_var.get(),
            'auto_save': self.auto_save_var.get(),
            'position_tracking': self.position_tracking
        })
        save_settings(self.settings)
    
    # Action methods
    def add_type_action(self):
        """Add typing action"""
        text = self.type_entry.get('1.0', 'end-1c').strip()
        if not text:
            show_error_dialog(self.root, "Invalid Input", "Please enter text to type")
            return
        
        delay = self.type_delay_var.get()
        action = TypeAction(text, delay)
        self.action_sequence.add_action(action)
        self.update_action_list()
        self.status_bar.set_status(f"Added typing action", "success")
        
        # Clear input
        self.type_entry.delete('1.0', 'end')
        self.type_delay_var.set(0.0)
    
    def add_click_action(self):
        """Add click action"""
        try:
            x = self.click_x_var.get()
            y = self.click_y_var.get()
            button = self.click_button_var.get()
            delay = self.click_delay_var.get()
            
            action = ClickAction(x, y, button, delay)
            self.action_sequence.add_action(action)
            self.update_action_list()
            self.status_bar.set_status(f"Added {button} click at ({x}, {y})", "success")
        except tk.TclError:
            show_error_dialog(self.root, "Invalid Input", "Please enter valid coordinates")
    
    def add_delay_action(self):
        """Add delay action"""
        wait_time = self.wait_time_var.get()
        action = DelayAction(wait_time)
        self.action_sequence.add_action(action)
        self.update_action_list()
        self.status_bar.set_status(f"Added delay of {wait_time} seconds", "success")
    
    def add_hotkey_action(self):
        """Add hotkey action"""
        keys_text = self.hotkey_keys_var.get().strip()
        if not keys_text:
            show_error_dialog(self.root, "Invalid Input", "Please enter hotkey combination")
            return
        
        keys = [k.strip() for k in keys_text.split(",")]
        delay = self.hotkey_delay_var.get()
        
        action = HotkeyAction(keys, delay)
        self.action_sequence.add_action(action)
        self.update_action_list()
        self.status_bar.set_status(f"Added hotkey: {'+'.join(keys)}", "success")
    
    def add_special_key_action(self, key: str):
        """Add special key action"""
        delay = self.special_key_delay_var.get()
        action = SpecialKeyAction(key, delay)
        self.action_sequence.add_action(action)
        self.update_action_list()
        self.status_bar.set_status(f"Added special key: {key}", "success")
    
    def update_action_list(self):
        """Update the action list display"""
        self.action_list.update_actions(self.action_sequence.actions)
        
        # Update file label to show unsaved changes
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.file_label.config(text=f"{filename} *")
        else:
            self.file_label.config(text="Untitled *")
    
    def handle_action_list_event(self, event_type: str, *args):
        """Handle events from action list"""
        if event_type == "edit":
            self.edit_selected_action()
        elif event_type == "delete":
            self.delete_selected_action()
        elif event_type == "duplicate":
            self.duplicate_selected_action()
        elif event_type == "moveup":
            self.move_action_up()
        elif event_type == "movedown":
            self.move_action_down()
        elif event_type == "move" and len(args) >= 2:
            from_index, to_index = args[0], args[1]
            self.action_sequence.move_action(from_index, to_index)
            self.update_action_list()
    
    def edit_selected_action(self):
        """Edit selected action"""
        index = self.action_list.get_selected_index()
        if index is None:
            show_info_dialog(self.root, "No Selection", "Please select an action to edit")
            return
        
        action = self.action_sequence.actions[index]
        # Create edit dialog (implementation would be similar to original but with new styling)
        self.show_edit_dialog(action, index)
    
    def show_edit_dialog(self, action, index: int):
        """Show edit dialog for action"""
        # This would create a modern styled edit dialog
        # Implementation similar to original but with new styling
        pass
    
    def delete_selected_action(self):
        """Delete selected action"""
        index = self.action_list.get_selected_index()
        if index is None:
            return
        
        if show_confirm_dialog(self.root, "Delete Action", 
                             "Are you sure you want to delete this action?"):
            self.action_sequence.remove_action(index)
            self.update_action_list()
            self.status_bar.set_status("Action deleted", "success")
    
    def duplicate_selected_action(self):
        """Duplicate selected action"""
        index = self.action_list.get_selected_index()
        if index is None:
            return
        
        action = self.action_sequence.actions[index]
        duplicate = action.clone()
        self.action_sequence.actions.insert(index + 1, duplicate)
        self.update_action_list()
        self.status_bar.set_status("Action duplicated", "success")
    
    def move_action_up(self):
        """Move selected action up"""
        index = self.action_list.get_selected_index()
        if index is None or index == 0:
            return
        
        self.action_sequence.move_action(index, index - 1)
        self.update_action_list()
        self.action_list.select_item(index - 1)
    
    def move_action_down(self):
        """Move selected action down"""
        index = self.action_list.get_selected_index()
        if index is None or index >= len(self.action_sequence.actions) - 1:
            return
        
        self.action_sequence.move_action(index, index + 1)
        self.update_action_list()
        self.action_list.select_item(index + 1)
    
    def clear_all_actions(self):
        """Clear all actions"""
        if not self.action_sequence.actions:
            return
        
        if show_confirm_dialog(self.root, "Clear All Actions", 
                             "Are you sure you want to clear all actions?"):
            self.action_sequence.clear()
            self.update_action_list()
            self.status_bar.set_status("All actions cleared", "success")
    
    # Automation methods
    def start_automation(self):
        """Start automation sequence"""
        if self.is_running:
            return
        
        if not self.action_sequence.actions:
            show_error_dialog(self.root, "No Actions", "Please add some actions before starting automation")
            return
        
        # Validate sequence
        errors = self.action_sequence.validate()
        if errors:
            error_msg = "\\n".join(errors)
            show_error_dialog(self.root, "Invalid Sequence", f"Please fix these errors:\\n{error_msg}")
            return
        
        self.is_running = True
        self.start_btn.state(['disabled'])
        self.stop_btn.state(['!disabled'])
        
        # Update sequence settings
        self.action_sequence.loop_enabled = self.loop_var.get()
        self.action_sequence.loop_count = self.loop_count_var.get()
        self.action_sequence.repeat_interval = self.repeat_interval_var.get()
        
        # Start automation in separate thread
        self.run_thread = threading.Thread(target=self._run_automation, daemon=True)
        self.run_thread.start()
        
        logger.info("Automation started")
    
    def _run_automation(self):
        """Run automation in separate thread"""
        try:
            # Countdown if enabled
            if self.countdown_var.get():
                for i in range(3, 0, -1):
                    if not self.is_running:
                        return
                    self.root.after(0, lambda i=i: self.status_bar.set_status(f"Starting in {i}...", "running"))
                    time.sleep(1)
            
            # Progress callback
            def progress_callback(loop_idx, loop_count, action_idx, action_count, action):
                if action_idx == -1:  # Between loops
                    msg = f"Loop {loop_idx + 1}/{loop_count} complete. Waiting..."
                else:
                    msg = f"Loop {loop_idx + 1}/{loop_count}, Action {action_idx + 1}/{action_count}"
                self.root.after(0, lambda: self.status_bar.set_status(msg, "running"))
            
            # Stop check
            def stop_check():
                return not self.is_running
            
            # Execute sequence
            success = self.action_sequence.execute(progress_callback, stop_check)
            
            if success and self.is_running:
                self.root.after(0, lambda: self.status_bar.set_status("Automation completed successfully", "success"))
            elif not self.is_running:
                self.root.after(0, lambda: self.status_bar.set_status("Automation stopped by user", "warning"))
            else:
                self.root.after(0, lambda: self.status_bar.set_status("Automation failed", "error"))
        
        except Exception as e:
            logger.error(f"Automation error: {e}")
            self.root.after(0, lambda: self.status_bar.set_status(f"Error: {str(e)}", "error"))
        
        finally:
            self.root.after(0, self._automation_finished)
    
    def _automation_finished(self):
        """Called when automation finishes"""
        self.is_running = False
        self.start_btn.state(['!disabled'])
        self.stop_btn.state(['disabled'])
    
    def stop_automation(self):
        """Stop automation"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.status_bar.set_status("Stopping automation...", "warning")
        logger.info("Automation stopped by user")
    
    # File operations
    def new_sequence(self):
        """Create new sequence"""
        if self.action_sequence.actions and self.file_label.cget('text').endswith(' *'):
            if show_confirm_dialog(self.root, "Unsaved Changes", 
                                 "You have unsaved changes. Continue anyway?"):
                pass
            else:
                return
        
        self.action_sequence = ActionSequence("New Sequence")
        self.current_file = None
        self.file_label.config(text="Untitled")
        self.update_action_list()
        self.status_bar.set_status("New sequence created", "success")
    
    def load_sequence(self):
        """Load sequence from file"""
        filename = filedialog.askopenfilename(
            title="Load Sequence",
            filetypes=SUPPORTED_FILE_EXTENSIONS,
            defaultextension=".json"
        )
        
        if filename:
            self.load_file(filename)
    
    def load_file(self, filename: str):
        """Load sequence from specific file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Create new sequence and load data
            self.action_sequence = ActionSequence()
            
            if "actions" in data:
                # New format
                self.action_sequence.from_dict(data)
            else:
                # Legacy format
                for action_data in data:
                    action = Action.create_from_dict(action_data)
                    self.action_sequence.add_action(action)
            
            self.current_file = filename
            self.file_label.config(text=os.path.basename(filename))
            self.update_action_list()
            
            # Update recent files
            if filename in self.recent_files:
                self.recent_files.remove(filename)
            self.recent_files.insert(0, filename)
            self.recent_files = self.recent_files[:MAX_RECENT_FILES]
            save_recent_files(self.recent_files)
            self._update_recent_menu()
            
            self.status_bar.set_status(f"Loaded {len(self.action_sequence.actions)} actions", "success")
            logger.info(f"Loaded sequence from {filename}")
        
        except Exception as e:
            logger.error(f"Failed to load file {filename}: {e}")
            show_error_dialog(self.root, "Load Error", f"Failed to load file:\\n{str(e)}")
    
    def save_sequence(self):
        """Save current sequence"""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_sequence_as()
    
    def save_sequence_as(self):
        """Save sequence with new filename"""
        if not self.action_sequence.actions:
            show_error_dialog(self.root, "No Actions", "No actions to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Sequence As",
            filetypes=SUPPORTED_FILE_EXTENSIONS,
            defaultextension=".json"
        )
        
        if filename:
            self._save_to_file(filename)
            self.current_file = filename
            self.file_label.config(text=os.path.basename(filename))
    
    def _save_to_file(self, filename: str):
        """Save sequence to specific file"""
        try:
            # Update sequence metadata
            self.action_sequence.modified_at = time.time()
            
            with open(filename, 'w') as f:
                json.dump(self.action_sequence.to_dict(), f, indent=2)
            
            # Remove asterisk from file label
            self.file_label.config(text=os.path.basename(filename))
            self.status_bar.set_status("Sequence saved", "success")
            logger.info(f"Saved sequence to {filename}")
        
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {e}")
            show_error_dialog(self.root, "Save Error", f"Failed to save file:\\n{str(e)}")
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.recent_files.clear()
        save_recent_files(self.recent_files)
        self._update_recent_menu()
        self.status_bar.set_status("Recent files cleared", "success")
    
    # UI methods
    def toggle_mouse_tracking(self):
        """Toggle mouse position tracking"""
        self.position_tracking = not self.position_tracking
        
        if self.position_tracking:
            self.track_btn.config(text=f"{EMOJI['stop']} Stop Track")
            self.status_bar.set_status("Mouse tracking enabled - Move mouse to update coordinates", "info")
            logger.info("Mouse tracking enabled")
        else:
            self.track_btn.config(text=f"{EMOJI['mouse']} Track")
            self.status_bar.set_status("Mouse tracking disabled", "info")
            logger.info("Mouse tracking disabled")
        
        # Save setting
        self.settings['position_tracking'] = self.position_tracking
        logger.info("Mouse tracking disabled")
        
        # Save setting
        self.settings['position_tracking'] = self.position_tracking
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current = CURRENT_THEME
        new_theme = 'light' if current == 'dark' else 'dark'
        
        switch_theme(new_theme)
        self.setup_styles()
        self.refresh_ui()
        
        self.status_bar.set_status(f"Switched to {new_theme} theme", "success")
        logger.info(f"Theme changed to {new_theme}")
    
    def refresh_ui(self):
        """Refresh UI styling"""
        self.setup_styles()
        self.update_action_list()
        self.status_bar.set_status("UI refreshed", "success")
    
    def show_settings(self):
        """Show settings dialog"""
        # This would create a comprehensive settings dialog
        show_info_dialog(self.root, "Settings", "Settings dialog would be implemented here")
    
    def show_special_keys_help(self):
        """Show special keys help dialog"""
        dialog, main_frame = create_modern_dialog(self.root, "Special Keys Help", 600, 500)
        
        # Title
        ttk.Label(main_frame, text="Special Keys Reference", style='Title.TLabel').pack(pady=10)
        
        # Create text widget for help content
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap='word', font=FONTS['default'],
                             bg=COLORS['input_bg'], fg=COLORS['text_primary'],
                             relief='solid', bd=1, padx=10, pady=10)
        text_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Insert help text
        text_widget.insert('1.0', SPECIAL_KEYS_HELP)
        text_widget.config(state='disabled')
        
        # Close button
        ttk.Button(main_frame, text="Close", command=dialog.destroy,
                  style='Primary.TButton').pack(pady=10)
    
    def show_shortcuts_help(self):
        """Show keyboard shortcuts help"""
        dialog, main_frame = create_modern_dialog(self.root, "Keyboard Shortcuts", 500, 400)
        
        # Title
        ttk.Label(main_frame, text="Keyboard Shortcuts", style='Title.TLabel').pack(pady=10)
        
        # Shortcuts list
        shortcuts_text = "\\n".join([
            f"{desc}: {key}" for key, desc in {
                SHORTCUTS['start_automation']: "Start Automation",
                SHORTCUTS['stop_automation']: "Stop Automation", 
                SHORTCUTS['track_mouse']: "Toggle Mouse Tracking",
                SHORTCUTS['save_sequence']: "Save Sequence",
                SHORTCUTS['load_sequence']: "Load Sequence",
                SHORTCUTS['new_sequence']: "New Sequence",
                SHORTCUTS['delete_action']: "Delete Selected Action",
                SHORTCUTS['edit_action']: "Edit Selected Action",
                SHORTCUTS['toggle_theme']: "Toggle Theme",
                SHORTCUTS['show_help']: "Show Help",
                "Ctrl+D": "Duplicate Selected Action"
            }.items()
        ])
        
        text_widget = tk.Text(main_frame, wrap='word', font=FONTS['default'],
                             bg=COLORS['input_bg'], fg=COLORS['text_primary'],
                             relief='solid', bd=1, padx=10, pady=10, height=15)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget.insert('1.0', shortcuts_text)
        text_widget.config(state='disabled')
        
        # Close button
        ttk.Button(main_frame, text="Close", command=dialog.destroy,
                  style='Primary.TButton').pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        dialog, main_frame = create_modern_dialog(self.root, "About", 400, 350)
        
        # App icon
        ttk.Label(main_frame, text="🖱️⌨️", font=FONTS['large']).pack(pady=10)
        
        # App info
        ttk.Label(main_frame, text=APP_NAME, style='Title.TLabel').pack(pady=5)
        ttk.Label(main_frame, text=f"Version {APP_VERSION}", style='Secondary.TLabel').pack()
        ttk.Label(main_frame, text=f"by {APP_AUTHOR}", style='Secondary.TLabel').pack(pady=5)
        
        # Description
        desc = ("A modern automation tool for keyboard and mouse actions\\n"
                "with a beautiful dark mode interface and enhanced features.")
        ttk.Label(main_frame, text=desc, style='Card.TLabel',
                 wraplength=350, justify='center').pack(pady=15)
        
        # Credits
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)
        ttk.Label(main_frame, text="Built with Python & Tkinter", style='Secondary.TLabel').pack()
        ttk.Label(main_frame, text="Uses PyAutoGUI for automation", style='Secondary.TLabel').pack()
        
        # Close button
        ttk.Button(main_frame, text="Close", command=dialog.destroy,
                  style='Primary.TButton').pack(pady=20)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            if show_confirm_dialog(self.root, "Automation Running", 
                                 "Automation is currently running. Stop and exit?"):
                self.stop_automation()
                time.sleep(0.5)  # Give time for automation to stop
            else:
                return
        
        # Check for unsaved changes
        if self.action_sequence.actions and self.file_label.cget('text').endswith(' *'):
            if show_confirm_dialog(self.root, "Unsaved Changes", 
                                 "You have unsaved changes. Exit anyway?"):
                pass
            else:
                return
        
        # Save settings
        self.save_settings()
        
        # Clean up global hotkeys
        try:
            keyboard.unhook_all()
        except:
            pass
        
        logger.info("Application closed")
        self.root.destroy()

def main():
    """Main application entry point"""
    # Check for required modules
    missing_modules = []
    
    try:
        import pyautogui
    except ImportError:
        missing_modules.append("pyautogui")
    
    try:
        import keyboard
    except ImportError:
        missing_modules.append("keyboard")
    
    if missing_modules:
        import tkinter.messagebox as mb
        modules_str = ", ".join(missing_modules)
        mb.showerror(
            "Missing Dependencies",
            f"The following modules are required but missing:\\n{modules_str}\\n\\n"
            f"Please install them using:\\npip install {' '.join(missing_modules)}"
        )
        return
    
    # Set up exception handling
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        
        try:
            import tkinter.messagebox as mb
            error_msg = f"An unexpected error occurred:\\n{exc_type.__name__}: {exc_value}"
            mb.showerror("Error", error_msg)
        except:
            pass
    
    sys.excepthook = handle_exception
    
    # Create and run application
    root = tk.Tk()
    app = PlaybianAutoTyper(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        # Clean up
        try:
            keyboard.unhook_all()
        except:
            pass

if __name__ == "__main__":
    main()