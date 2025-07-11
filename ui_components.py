"""
UI components and styling for Playbian Auto Typer & Clicker
Contains all custom UI widgets, styling, and helper classes
"""

import tkinter as tk
from tkinter import ttk, Menu, messagebox
import time
import logging
from typing import Callable, Optional, List, Dict, Any
from config import COLORS, EMOJI, FONTS, ANIMATION, SPECIAL_KEYS

logger = logging.getLogger(__name__)

class ModernStyle:
    """Modern dark theme styling for the application"""
    
    @staticmethod
    def setup_styles():
        """Setup modern dark theme styles"""
        style = ttk.Style()
        
        # Use the most modern theme available
        available_themes = style.theme_names()
        preferred_themes = ['clam', 'vista', 'winnative', 'default']
        
        for theme in preferred_themes:
            if theme in available_themes:
                style.theme_use(theme)
                break
        
        # Configure main frames
        style.configure('TFrame', 
                      background=COLORS['bg_primary'],
                      borderwidth=0)
        
        style.configure('Card.TFrame', 
                      background=COLORS['bg_secondary'],
                      borderwidth=1,
                      relief='solid',
                      bordercolor=COLORS['border'])
        
        style.configure('Glass.TFrame', 
                      background=COLORS['glass_bg'],
                      borderwidth=1,
                      relief='solid',
                      bordercolor=COLORS['glass_border'])
        
        # Configure labelframes
        style.configure('TLabelframe', 
                      background=COLORS['bg_primary'],
                      bordercolor=COLORS['border'],
                      borderwidth=2,
                      relief='solid')
        
        style.configure('TLabelframe.Label', 
                      font=FONTS['default'],
                      foreground=COLORS['text_primary'],
                      background=COLORS['bg_primary'])
        
        style.configure('Card.TLabelframe', 
                      background=COLORS['bg_secondary'],
                      bordercolor=COLORS['border_light'],
                      borderwidth=1,
                      relief='solid')
        
        style.configure('Card.TLabelframe.Label', 
                      font=FONTS['default'],
                      foreground=COLORS['text_primary'],
                      background=COLORS['bg_secondary'])
        
        # Configure labels
        style.configure('TLabel', 
                      font=FONTS['default'],
                      background=COLORS['bg_primary'],
                      foreground=COLORS['text_primary'])
        
        style.configure('Heading.TLabel', 
                      font=FONTS['heading'],
                      background=COLORS['bg_primary'],
                      foreground=COLORS['text_primary'])
        
        style.configure('Title.TLabel', 
                      font=FONTS['title'],
                      background=COLORS['bg_primary'],
                      foreground=COLORS['accent'])
        
        style.configure('Secondary.TLabel', 
                      font=FONTS['default'],
                      background=COLORS['bg_primary'],
                      foreground=COLORS['text_secondary'])
        
        style.configure('Card.TLabel', 
                      font=FONTS['default'],
                      background=COLORS['bg_secondary'],
                      foreground=COLORS['text_primary'])
        
        # Configure buttons
        ModernStyle._configure_buttons(style)
        
        # Configure inputs
        ModernStyle._configure_inputs(style)
        
        # Configure treeview
        ModernStyle._configure_treeview(style)
        
        # Configure notebook
        ModernStyle._configure_notebook(style)
        
        # Configure other widgets
        ModernStyle._configure_misc_widgets(style)
    
    @staticmethod
    def _configure_buttons(style):
        """Configure button styles"""
        # Base button
        style.configure('TButton', 
                      font=FONTS['default'],
                      background=COLORS['bg_secondary'],
                      foreground=COLORS['text_primary'],
                      bordercolor=COLORS['border'],
                      focuscolor=COLORS['accent'],
                      relief='solid',
                      borderwidth=1,
                      padding=(12, 8))
        
        style.map('TButton',
                background=[('pressed', COLORS['border']), 
                          ('active', COLORS['bg_tertiary'])],
                foreground=[('pressed', COLORS['text_primary']), 
                          ('active', COLORS['text_primary'])],
                bordercolor=[('active', COLORS['accent'])])
        
        # Primary button
        style.configure('Primary.TButton', 
                      font=FONTS['default'],
                      background=COLORS['accent'],
                      foreground='white',
                      bordercolor=COLORS['accent_hover'],
                      relief='solid',
                      borderwidth=1,
                      padding=(12, 8))
        
        style.map('Primary.TButton',
                background=[('pressed', COLORS['accent_hover']), 
                          ('active', COLORS['accent_light'])],
                foreground=[('pressed', 'white'), ('active', 'white')])
        
        # Success button
        style.configure('Success.TButton', 
                      font=FONTS['default'],
                      background=COLORS['success'],
                      foreground='white',
                      bordercolor=COLORS['success_hover'],
                      relief='solid',
                      borderwidth=1,
                      padding=(12, 8))
        
        style.map('Success.TButton',
                background=[('pressed', COLORS['success_hover']), 
                          ('active', COLORS['success_hover'])],
                foreground=[('pressed', 'white'), ('active', 'white')])
        
        # Danger button
        style.configure('Danger.TButton', 
                      font=FONTS['default'],
                      background=COLORS['danger'],
                      foreground='white',
                      bordercolor=COLORS['danger_hover'],
                      relief='solid',
                      borderwidth=1,
                      padding=(12, 8))
        
        style.map('Danger.TButton',
                background=[('pressed', COLORS['danger_hover']), 
                          ('active', COLORS['danger_hover'])],
                foreground=[('pressed', 'white'), ('active', 'white')])
        
        # Small button
        style.configure('Small.TButton', 
                      font=FONTS['small'],
                      background=COLORS['bg_secondary'],
                      foreground=COLORS['text_primary'],
                      bordercolor=COLORS['border'],
                      relief='solid',
                      borderwidth=1,
                      padding=(8, 4))
        
        style.map('Small.TButton',
                background=[('pressed', COLORS['border']), 
                          ('active', COLORS['bg_tertiary'])],
                bordercolor=[('active', COLORS['accent'])])
    
    @staticmethod
    def _configure_inputs(style):
        """Configure input widget styles"""
        # Entry
        style.configure('TEntry', 
                      font=FONTS['default'],
                      fieldbackground=COLORS['input_bg'],
                      foreground=COLORS['text_primary'],
                      bordercolor=COLORS['input_border'],
                      insertcolor=COLORS['text_primary'],
                      relief='solid',
                      borderwidth=1,
                      padding=8)
        
        style.map('TEntry',
                bordercolor=[('focus', COLORS['input_focus'])])
        
        # Spinbox
        style.configure('TSpinbox', 
                      font=FONTS['default'],
                      fieldbackground=COLORS['input_bg'],
                      foreground=COLORS['text_primary'],
                      bordercolor=COLORS['input_border'],
                      arrowcolor=COLORS['text_primary'],
                      insertcolor=COLORS['text_primary'],
                      relief='solid',
                      borderwidth=1,
                      padding=8)
        
        style.map('TSpinbox',
                bordercolor=[('focus', COLORS['input_focus'])])
        
        # Combobox
        style.configure('TCombobox', 
                      font=FONTS['default'],
                      fieldbackground=COLORS['input_bg'],
                      foreground=COLORS['text_primary'],
                      bordercolor=COLORS['input_border'],
                      arrowcolor=COLORS['text_primary'],
                      insertcolor=COLORS['text_primary'],
                      relief='solid',
                      borderwidth=1,
                      padding=8)
        
        style.map('TCombobox',
                bordercolor=[('focus', COLORS['input_focus'])])
        
        # Checkbutton
        style.configure('TCheckbutton', 
                      font=FONTS['default'],
                      background=COLORS['bg_primary'],
                      foreground=COLORS['text_primary'],
                      focuscolor=COLORS['accent'])
        
        # Radiobutton
        style.configure('TRadiobutton', 
                      font=FONTS['default'],
                      background=COLORS['bg_primary'],
                      foreground=COLORS['text_primary'],
                      focuscolor=COLORS['accent'])
    
    @staticmethod
    def _configure_treeview(style):
        """Configure treeview styles"""
        style.configure('Treeview', 
                      font=FONTS['default'],
                      background=COLORS['tree_bg'],
                      foreground=COLORS['text_primary'],
                      fieldbackground=COLORS['tree_bg'],
                      bordercolor=COLORS['border'],
                      borderwidth=1,
                      relief='solid',
                      rowheight=32)
        
        style.configure('Treeview.Heading', 
                      font=FONTS['default'],
                      background=COLORS['bg_tertiary'],
                      foreground=COLORS['text_primary'],
                      borderwidth=1,
                      relief='solid',
                      padding=(8, 6))
        
        style.map('Treeview',
                background=[('selected', COLORS['tree_select'])],
                foreground=[('selected', 'white')])
        
        style.map('Treeview.Heading',
                background=[('active', COLORS['accent']),
                          ('pressed', COLORS['accent_hover'])],
                foreground=[('active', 'white'),
                          ('pressed', 'white')])
        
        # Action-specific treeview styles
        for action_type in ['type', 'click', 'delay', 'hotkey']:
            style.map(f'{action_type}_action.Treeview',
                    background=[('selected', COLORS['tree_select']), 
                              ('', COLORS[f'{action_type}_action'])],
                    foreground=[('selected', 'white'), 
                              ('', COLORS['text_primary'])])
    
    @staticmethod
    def _configure_notebook(style):
        """Configure notebook styles"""
        style.configure('TNotebook', 
                      background=COLORS['bg_primary'],
                      bordercolor=COLORS['border'],
                      tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab', 
                      font=FONTS['default'],
                      background=COLORS['bg_secondary'],
                      foreground=COLORS['text_primary'],
                      bordercolor=COLORS['border'],
                      padding=[12, 8],
                      focuscolor=COLORS['accent'])
        
        style.map('TNotebook.Tab',
                background=[('selected', COLORS['bg_primary']), 
                          ('active', COLORS['bg_tertiary'])],
                foreground=[('selected', COLORS['accent']), 
                          ('active', COLORS['text_primary'])],
                bordercolor=[('selected', COLORS['accent'])])
    
    @staticmethod
    def _configure_misc_widgets(style):
        """Configure miscellaneous widget styles"""
        # Separator
        style.configure('TSeparator', 
                      background=COLORS['border'])
        
        # Progressbar
        style.configure('TProgressbar',
                      background=COLORS['accent'],
                      troughcolor=COLORS['bg_secondary'],
                      bordercolor=COLORS['border'],
                      lightcolor=COLORS['accent'],
                      darkcolor=COLORS['accent'])
        
        # Scale
        style.configure('TScale',
                      background=COLORS['bg_primary'],
                      troughcolor=COLORS['bg_secondary'],
                      bordercolor=COLORS['border'],
                      slidercolor=COLORS['accent'])

class ToolTip:
    """Enhanced tooltip with animation and modern styling"""
    
    def __init__(self, widget, text: str, delay: int = ANIMATION['tooltip_delay']):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip = None
        self.after_id = None
        
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<Motion>", self._on_motion)
    
    def _on_enter(self, event=None):
        """Handle mouse enter event"""
        self._schedule_tooltip()
    
    def _on_leave(self, event=None):
        """Handle mouse leave event"""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _on_motion(self, event=None):
        """Handle mouse motion event"""
        if self.tooltip:
            self._update_position(event)
    
    def _schedule_tooltip(self):
        """Schedule tooltip to show after delay"""
        self._cancel_tooltip()
        self.after_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _cancel_tooltip(self):
        """Cancel scheduled tooltip"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
    
    def _show_tooltip(self, event=None):
        """Show the tooltip"""
        if self.tooltip:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.configure(bg=COLORS['tooltip_bg'])
        
        # Create tooltip content
        frame = tk.Frame(self.tooltip, 
                        bg=COLORS['tooltip_bg'],
                        bd=1,
                        relief='solid',
                        highlightbackground=COLORS['tooltip_border'],
                        highlightcolor=COLORS['tooltip_border'],
                        highlightthickness=1)
        frame.pack()
        
        label = tk.Label(frame,
                        text=self.text,
                        font=FONTS['small'],
                        bg=COLORS['tooltip_bg'],
                        fg=COLORS['text_primary'],
                        padx=8,
                        pady=4)
        label.pack()
        
        # Animate tooltip appearance
        self.tooltip.attributes('-alpha', 0.0)
        self._fade_in()
    
    def _fade_in(self, alpha: float = 0.0):
        """Fade in animation for tooltip"""
        alpha += 0.1
        if alpha <= 1.0 and self.tooltip:
            try:
                self.tooltip.attributes('-alpha', alpha)
                self.tooltip.after(ANIMATION['fade_delay'], 
                                 lambda: self._fade_in(alpha))
            except tk.TclError:
                pass
    
    def _hide_tooltip(self):
        """Hide the tooltip"""
        if self.tooltip:
            try:
                self.tooltip.destroy()
            except tk.TclError:
                pass
            self.tooltip = None
    
    def _update_position(self, event):
        """Update tooltip position based on mouse movement"""
        if self.tooltip:
            x = event.x_root + 20
            y = event.y_root + 5
            try:
                self.tooltip.wm_geometry(f"+{x}+{y}")
            except tk.TclError:
                pass

class StatusBar(ttk.Frame):
    """Enhanced status bar with icons and animations"""
    
    def __init__(self, parent):
        super().__init__(parent, style='Card.TFrame')
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.last_update = time.time()
        
        # Status icon and text
        self.icon_label = ttk.Label(self, text="✓", 
                                   foreground=COLORS['success'],
                                   background=COLORS['bg_secondary'],
                                   font=FONTS['default'])
        self.icon_label.pack(side='left', padx=(8, 4), pady=4)
        
        self.status_label = ttk.Label(self, 
                                    textvariable=self.status_var,
                                    style='Card.TLabel',
                                    anchor='w')
        self.status_label.pack(side='left', fill='x', expand=True, padx=4, pady=4)
        
        # Mouse position display
        self.position_var = tk.StringVar()
        self.position_var.set("Mouse: (0, 0)")
        self.position_label = ttk.Label(self, 
                                      textvariable=self.position_var,
                                      style='Card.TLabel')
        self.position_label.pack(side='right', padx=4, pady=4)
        
        # Time display
        self.time_var = tk.StringVar()
        self.time_label = ttk.Label(self, 
                                  textvariable=self.time_var,
                                  style='Card.TLabel')
        self.time_label.pack(side='right', padx=4, pady=4)
        
        self._update_time()
    
    def set_status(self, text: str, status_type: str = "info"):
        """Set status with icon based on type"""
        icons = {
            "info": ("ℹ️", COLORS['info']),
            "success": ("✓", COLORS['success']),
            "warning": ("⚠️", COLORS['warning']),
            "error": ("✗", COLORS['danger']),
            "running": ("▶️", COLORS['accent'])
        }
        
        icon, color = icons.get(status_type, ("ℹ️", COLORS['info']))
        
        self.icon_label.config(text=icon, foreground=color)
        self.status_var.set(text)
        self.last_update = time.time()
        self.update_idletasks()
        
        # Auto-clear status after timeout (except for running status)
        if status_type != "running":
            self.after(ANIMATION['status_timeout'], self._auto_clear_status)
        
        logger.info(f"Status updated: {text} ({status_type})")
    
    def _auto_clear_status(self):
        """Auto-clear status if it hasn't been updated recently"""
        if time.time() - self.last_update >= ANIMATION['status_timeout'] / 1000:
            self.set_status("Ready", "success")
    
    def set_position(self, x: int, y: int):
        """Update mouse position display"""
        self.position_var.set(f"Mouse: ({x}, {y})")
    
    def _update_time(self):
        """Update time display"""
        current_time = time.strftime("%H:%M:%S")
        self.time_var.set(current_time)
        self.after(1000, self._update_time)

class ActionListView(ttk.Frame):
    """Enhanced action list with drag-drop and context menu"""
    
    def __init__(self, parent, callback: Callable):
        super().__init__(parent, style='Card.TFrame')
        self.callback = callback
        self.actions = []
        self.configured_tags = set()  # Track configured tags
        
        # Create treeview with columns
        columns = ('Icon', 'Action', 'Details', 'Delay')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.tree.heading('Icon', text='')
        self.tree.heading('Action', text='Action Type')
        self.tree.heading('Details', text='Details')
        self.tree.heading('Delay', text='Delay (s)')
        
        self.tree.column('Icon', width=40, minwidth=40, anchor='center')
        self.tree.column('Action', width=120, minwidth=100)
        self.tree.column('Details', width=300, minwidth=200)
        self.tree.column('Delay', width=80, minwidth=60, anchor='center')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.tree.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        v_scrollbar.grid(row=0, column=1, sticky='ns', pady=2)
        h_scrollbar.grid(row=1, column=0, sticky='ew', padx=2)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Button-3>", self._on_right_click)
        self.tree.bind("<ButtonPress-1>", self._on_press)
        self.tree.bind("<B1-Motion>", self._on_motion)
        self.tree.bind("<ButtonRelease-1>", self._on_release)
        self.tree.bind("<KeyPress-Delete>", self._on_delete_key)
        self.tree.bind("<KeyPress-Return>", self._on_enter_key)
        
        # Drag and drop state
        self.drag_data = {"item": None, "start_index": None}
        
        # Create context menu
        self._create_context_menu()
    
    def _create_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.configure(
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['accent'],
            activeforeground='white',
            font=FONTS['default'],
            bd=0
        )
        
        self.context_menu.add_command(
            label=f"{EMOJI['edit']} Edit Action",
            command=self._edit_selected,
            accelerator="Enter"
        )
        self.context_menu.add_command(
            label=f"{EMOJI['copy']} Duplicate Action",
            command=self._duplicate_selected,
            accelerator="Ctrl+D"
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label=f"{EMOJI['up']} Move Up",
            command=self._move_up_selected,
            accelerator="Ctrl+Up"
        )
        self.context_menu.add_command(
            label=f"{EMOJI['down']} Move Down",
            command=self._move_down_selected,
            accelerator="Ctrl+Down"
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label=f"{EMOJI['delete']} Delete Action",
            command=self._delete_selected,
            accelerator="Delete"
        )
    
    def update_actions(self, actions: List):
        """Update the list with new actions"""
        self.actions = actions
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add actions to tree
        for i, action in enumerate(actions):
            self._add_action_to_tree(action, i)
        
        logger.debug(f"Updated action list with {len(actions)} actions")
    
    def _add_action_to_tree(self, action, index: int):
        """Add a single action to the tree"""
        # Get action icon and details
        icon = self._get_action_icon(action)
        action_type = action.__class__.__name__.replace('Action', '')
        details = self._get_action_details(action)
        delay = getattr(action, 'delay', 0)
        
        # Special handling for DelayAction
        if hasattr(action, 'wait_time'):
            delay = action.wait_time
        
        # Insert into tree
        item = self.tree.insert('', 'end', values=(icon, action_type, details, delay))
        
        # Apply action-specific styling
        action_tag = f"{action_type.lower()}_action"
        self.tree.set(item, 'Icon', icon)
        
        # Configure tags for visual distinction
        if action_tag not in self.configured_tags:
            bg_color = COLORS.get(f'{action_type.lower()}_action', COLORS['bg_secondary'])
            self.tree.tag_configure(action_tag, background=bg_color)
            self.configured_tags.add(action_tag)
        
        self.tree.item(item, tags=(action_tag,))
    
    def _get_action_icon(self, action) -> str:
        """Get appropriate icon for action type"""
        action_icons = {
            'TypeAction': EMOJI['keyboard'],
            'ClickAction': EMOJI['mouse'],
            'DelayAction': EMOJI['delay'],
            'HotkeyAction': EMOJI['hotkey'],
            'SpecialKeyAction': EMOJI['keyboard'],
            'ScrollAction': '🖱️',
            'DragAction': '🖱️'
        }
        return action_icons.get(action.__class__.__name__, '❓')
    
    def _get_action_details(self, action) -> str:
        """Get formatted details for action"""
        if hasattr(action, 'text'):
            text = action.text[:50]
            return f"'{text}{'...' if len(action.text) > 50 else ''}'"
        elif hasattr(action, 'x') and hasattr(action, 'y'):
            if hasattr(action, 'button'):
                return f"{action.button} click at ({action.x}, {action.y})"
            else:
                return f"Position ({action.x}, {action.y})"
        elif hasattr(action, 'keys'):
            return f"Keys: {'+'.join(action.keys)}"
        elif hasattr(action, 'key'):
            return f"Key: {action.key}"
        elif hasattr(action, 'wait_time'):
            return f"Wait {action.wait_time} seconds"
        else:
            return str(action)
    
    def get_selected_index(self) -> Optional[int]:
        """Get index of selected item"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        return self.tree.index(item)
    
    def select_item(self, index: int):
        """Select item by index"""
        if 0 <= index < len(self.tree.get_children()):
            items = self.tree.get_children()
            self.tree.selection_set(items[index])
            self.tree.see(items[index])
    
    # Event handlers
    def _on_double_click(self, event):
        """Handle double-click event"""
        self._edit_selected()
    
    def _on_right_click(self, event):
        """Handle right-click event"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _on_press(self, event):
        """Handle mouse press for drag operation"""
        item = self.tree.identify_row(event.y)
        if item:
            self.drag_data["item"] = item
            self.drag_data["start_index"] = self.tree.index(item)
    
    def _on_motion(self, event):
        """Handle mouse motion for drag operation"""
        if self.drag_data["item"]:
            self.tree.configure(cursor="hand2")
    
    def _on_release(self, event):
        """Handle mouse release for drag operation"""
        if self.drag_data["item"]:
            target = self.tree.identify_row(event.y)
            if target and target != self.drag_data["item"]:
                target_index = self.tree.index(target)
                start_index = self.drag_data["start_index"]
                self.callback("move", start_index, target_index)
            
            self.tree.configure(cursor="")
            self.drag_data = {"item": None, "start_index": None}
    
    def _on_delete_key(self, event):
        """Handle delete key press"""
        self._delete_selected()
    
    def _on_enter_key(self, event):
        """Handle enter key press"""
        self._edit_selected()
    
    # Action methods
    def _edit_selected(self):
        """Edit selected action"""
        index = self.get_selected_index()
        if index is not None:
            self.callback("edit", index)
    
    def _delete_selected(self):
        """Delete selected action"""
        index = self.get_selected_index()
        if index is not None:
            self.callback("delete", index)
    
    def _duplicate_selected(self):
        """Duplicate selected action"""
        index = self.get_selected_index()
        if index is not None:
            self.callback("duplicate", index)
    
    def _move_up_selected(self):
        """Move selected action up"""
        index = self.get_selected_index()
        if index is not None and index > 0:
            self.callback("move", index, index - 1)
            self.select_item(index - 1)
    
    def _move_down_selected(self):
        """Move selected action down"""
        index = self.get_selected_index()
        if index is not None and index < len(self.actions) - 1:
            self.callback("move", index, index + 1)
            self.select_item(index + 1)

class ProgressDialog:
    """Modern progress dialog with cancellation"""
    
    def __init__(self, parent, title: str = "Progress"):
        self.parent = parent
        self.cancelled = False
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 200
        y = (self.dialog.winfo_screenheight() // 2) - 75
        self.dialog.geometry(f"+{x}+{y}")
        
        # Configure dialog
        self.dialog.configure(bg=COLORS['bg_primary'])
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # Create content
        self._create_content()
    
    def _create_content(self):
        """Create dialog content"""
        main_frame = ttk.Frame(self.dialog, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        self.title_var = tk.StringVar(value="Processing...")
        title_label = ttk.Label(main_frame, textvariable=self.title_var, 
                               style='Heading.TLabel')
        title_label.pack(pady=(5, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=300)
        self.progress.pack(pady=5)
        
        # Status text
        self.status_var = tk.StringVar(value="Starting...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                style='Secondary.TLabel')
        status_label.pack(pady=5)
        
        # Cancel button
        cancel_btn = ttk.Button(main_frame, text="Cancel", 
                               command=self.cancel, style='Danger.TButton')
        cancel_btn.pack(pady=10)
    
    def update_progress(self, value: float, status: str = ""):
        """Update progress (0-100)"""
        self.progress['value'] = value
        if status:
            self.status_var.set(status)
        self.dialog.update_idletasks()
    
    def set_title(self, title: str):
        """Set dialog title"""
        self.title_var.set(title)
    
    def cancel(self):
        """Cancel operation"""
        self.cancelled = True
        self.dialog.destroy()
    
    def is_cancelled(self) -> bool:
        """Check if operation was cancelled"""
        return self.cancelled
    
    def close(self):
        """Close dialog"""
        try:
            self.dialog.destroy()
        except tk.TclError:
            pass

def create_modern_dialog(parent, title: str, width: int = 400, height: int = 300) -> tuple:
    """Create a modern styled dialog window"""
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry(f"{width}x{height}")
    dialog.transient(parent)
    dialog.grab_set()
    dialog.configure(bg=COLORS['bg_primary'])
    
    # Center dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # Create main frame
    main_frame = ttk.Frame(dialog, style='Card.TFrame')
    main_frame.pack(fill='both', expand=True, padx=15, pady=15)
    
    return dialog, main_frame

def show_error_dialog(parent, title: str, message: str):
    """Show styled error dialog"""
    dialog, main_frame = create_modern_dialog(parent, title, 450, 200)
    
    # Error icon and message
    ttk.Label(main_frame, text="❌", font=FONTS['large']).pack(pady=10)
    
    ttk.Label(main_frame, text=title, style='Heading.TLabel').pack(pady=5)
    
    msg_label = ttk.Label(main_frame, text=message, style='Card.TLabel',
                         wraplength=400, justify='center')
    msg_label.pack(pady=10, padx=20)
    
    # OK button
    ttk.Button(main_frame, text="OK", command=dialog.destroy,
              style='Primary.TButton').pack(pady=10)
    
    dialog.focus_set()

def show_info_dialog(parent, title: str, message: str):
    """Show styled info dialog"""
    dialog, main_frame = create_modern_dialog(parent, title, 450, 200)
    
    # Info icon and message
    ttk.Label(main_frame, text="ℹ️", font=FONTS['large']).pack(pady=10)
    
    ttk.Label(main_frame, text=title, style='Heading.TLabel').pack(pady=5)
    
    msg_label = ttk.Label(main_frame, text=message, style='Card.TLabel',
                         wraplength=400, justify='center')
    msg_label.pack(pady=10, padx=20)
    
    # OK button
    ttk.Button(main_frame, text="OK", command=dialog.destroy,
              style='Primary.TButton').pack(pady=10)
    
    dialog.focus_set()

def show_confirm_dialog(parent, title: str, message: str) -> bool:
    """Show styled confirmation dialog"""
    result = [False]  # Use list to modify from nested function
    
    dialog, main_frame = create_modern_dialog(parent, title, 450, 220)
    
    # Question icon and message
    ttk.Label(main_frame, text="❓", font=FONTS['large']).pack(pady=10)
    
    ttk.Label(main_frame, text=title, style='Heading.TLabel').pack(pady=5)
    
    msg_label = ttk.Label(main_frame, text=message, style='Card.TLabel',
                         wraplength=400, justify='center')
    msg_label.pack(pady=10, padx=20)
    
    # Buttons
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20)
    
    def on_yes():
        result[0] = True
        dialog.destroy()
    
    def on_no():
        result[0] = False
        dialog.destroy()
    
    ttk.Button(btn_frame, text="No", command=on_no,
              style='TButton').pack(side='left', padx=10)
    ttk.Button(btn_frame, text="Yes", command=on_yes,
              style='Primary.TButton').pack(side='left', padx=10)
    
    dialog.focus_set()
    dialog.wait_window()
    
    return result[0]