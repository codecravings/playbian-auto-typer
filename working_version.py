#!/usr/bin/env python3
"""
Working version of Playbian Auto Typer & Clicker
Simplified to ensure compatibility
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyautogui
import time
import json
import threading
import logging

# Simple logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleAction:
    def __init__(self, action_type, data, delay=0):
        self.action_type = action_type
        self.data = data
        self.delay = delay
    
    def execute(self):
        time.sleep(self.delay)
        if self.action_type == 'type':
            pyautogui.typewrite(self.data)
        elif self.action_type == 'click':
            x, y, button = self.data
            pyautogui.click(x, y, button=button)
        elif self.action_type == 'delay':
            time.sleep(self.data)
    
    def __str__(self):
        if self.action_type == 'type':
            return f"Type: '{self.data}' (delay: {self.delay}s)"
        elif self.action_type == 'click':
            x, y, button = self.data
            return f"Click {button} at ({x}, {y}) (delay: {self.delay}s)"
        elif self.action_type == 'delay':
            return f"Wait {self.data} seconds"

class WorkingAutoTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("Playbian Auto Typer (Working Version)")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        self.actions = []
        self.position_tracking = False
        self.running = False
        
        self.setup_style()
        self.setup_ui()
        self.start_position_tracking()
    
    def setup_style(self):
        """Setup dark theme styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TLabel', background='#2d2d2d', foreground='white')
        style.configure('TButton', background='#4d79ff', foreground='white')
        style.configure('TEntry', fieldbackground='#404040', foreground='white')
        style.configure('TCombobox', fieldbackground='#404040', foreground='white')
        style.configure('TLabelframe', background='#2d2d2d', foreground='white')
        style.configure('TLabelframe.Label', background='#2d2d2d', foreground='white')
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🖱️⌨️ Playbian Auto Typer (Working Version)", 
                               font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Add Actions")
        input_frame.pack(fill='x', pady=10)
        
        # Type action
        type_frame = ttk.Frame(input_frame)
        type_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(type_frame, text="Text:").pack(side='left')
        self.text_var = tk.StringVar()
        text_entry = ttk.Entry(type_frame, textvariable=self.text_var, width=30)
        text_entry.pack(side='left', padx=5)
        
        ttk.Label(type_frame, text="Delay:").pack(side='left', padx=(10,0))
        self.type_delay_var = tk.DoubleVar()
        ttk.Spinbox(type_frame, from_=0, to=10, increment=0.1, width=5, 
                   textvariable=self.type_delay_var).pack(side='left', padx=5)
        
        ttk.Button(type_frame, text="Add Type Action", 
                  command=self.add_type_action).pack(side='left', padx=10)
        
        # Click action
        click_frame = ttk.Frame(input_frame)
        click_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(click_frame, text="X:").pack(side='left')
        self.x_var = tk.IntVar()
        ttk.Entry(click_frame, textvariable=self.x_var, width=6).pack(side='left', padx=2)
        
        ttk.Label(click_frame, text="Y:").pack(side='left')
        self.y_var = tk.IntVar()
        ttk.Entry(click_frame, textvariable=self.y_var, width=6).pack(side='left', padx=2)
        
        ttk.Label(click_frame, text="Button:").pack(side='left', padx=(10,0))
        self.button_var = tk.StringVar(value="left")
        ttk.Combobox(click_frame, textvariable=self.button_var, 
                    values=["left", "right", "middle"], width=8).pack(side='left', padx=2)
        
        ttk.Label(click_frame, text="Delay:").pack(side='left', padx=(10,0))
        self.click_delay_var = tk.DoubleVar()
        ttk.Spinbox(click_frame, from_=0, to=10, increment=0.1, width=5, 
                   textvariable=self.click_delay_var).pack(side='left', padx=2)
        
        self.track_btn = ttk.Button(click_frame, text="🖱️ Track Mouse", 
                                   command=self.toggle_tracking)
        self.track_btn.pack(side='left', padx=5)
        
        ttk.Button(click_frame, text="Add Click Action", 
                  command=self.add_click_action).pack(side='left', padx=10)
        
        # Delay action
        delay_frame = ttk.Frame(input_frame)
        delay_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(delay_frame, text="Wait Time (s):").pack(side='left')
        self.wait_var = tk.DoubleVar(value=1.0)
        ttk.Spinbox(delay_frame, from_=0.1, to=60, increment=0.5, width=8, 
                   textvariable=self.wait_var).pack(side='left', padx=5)
        
        ttk.Button(delay_frame, text="⏱️ Add Delay", 
                  command=self.add_delay_action).pack(side='left', padx=10)
        
        # Actions list
        list_frame = ttk.LabelFrame(main_frame, text="Action Sequence")
        list_frame.pack(fill='both', expand=True, pady=10)
        
        # Listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.actions_listbox = tk.Listbox(list_container, bg='#404040', fg='white',
                                         selectbackground='#4d79ff', font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=self.actions_listbox.yview)
        self.actions_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.actions_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # List controls
        list_controls = ttk.Frame(list_frame)
        list_controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(list_controls, text="🗑️ Delete Selected", 
                  command=self.delete_selected).pack(side='left', padx=2)
        ttk.Button(list_controls, text="🧹 Clear All", 
                  command=self.clear_actions).pack(side='left', padx=2)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=5)
        
        start_btn = ttk.Button(control_frame, text="▶️ Start (F5)", 
                              command=self.start_automation)
        start_btn.pack(side='left', padx=5)
        
        stop_btn = ttk.Button(control_frame, text="⏹️ Stop (Esc)", 
                             command=self.stop_automation)
        stop_btn.pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="💾 Save", 
                  command=self.save_actions).pack(side='left', padx=5)
        ttk.Button(control_frame, text="📂 Load", 
                  command=self.load_actions).pack(side='left', padx=5)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=5)
        
        self.status_var = tk.StringVar(value="Ready - Add actions and press Start")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side='left')
        
        self.position_var = tk.StringVar(value="Mouse: (0, 0)")
        position_label = ttk.Label(status_frame, textvariable=self.position_var)
        position_label.pack(side='right')
        
        # Shortcuts
        self.root.bind('<F5>', lambda e: self.start_automation())
        self.root.bind('<Escape>', lambda e: self.stop_automation())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        
        # Focus on text entry
        text_entry.focus_set()
    
    def add_type_action(self):
        text = self.text_var.get().strip()
        if text:
            delay = self.type_delay_var.get()
            action = SimpleAction('type', text, delay)
            self.actions.append(action)
            self.actions_listbox.insert('end', str(action))
            self.text_var.set("")
            self.status_var.set(f"Added typing action. Total: {len(self.actions)}")
            logger.info(f"Added type action: {text}")
        else:
            self.status_var.set("Please enter text to type")
    
    def add_click_action(self):
        x, y = self.x_var.get(), self.y_var.get()
        button = self.button_var.get()
        delay = self.click_delay_var.get()
        action = SimpleAction('click', (x, y, button), delay)
        self.actions.append(action)
        self.actions_listbox.insert('end', str(action))
        self.status_var.set(f"Added click action. Total: {len(self.actions)}")
        logger.info(f"Added click action: {button} at ({x}, {y})")
    
    def add_delay_action(self):
        wait_time = self.wait_var.get()
        action = SimpleAction('delay', wait_time)
        self.actions.append(action)
        self.actions_listbox.insert('end', str(action))
        self.status_var.set(f"Added delay action. Total: {len(self.actions)}")
        logger.info(f"Added delay action: {wait_time}s")
    
    def delete_selected(self):
        selection = self.actions_listbox.curselection()
        if selection:
            index = selection[0]
            self.actions.pop(index)
            self.actions_listbox.delete(index)
            self.status_var.set(f"Deleted action. Total: {len(self.actions)}")
    
    def toggle_tracking(self):
        self.position_tracking = not self.position_tracking
        if self.position_tracking:
            self.track_btn.config(text="⏹️ Stop Tracking")
            self.status_var.set("Mouse tracking enabled - Move mouse to update coordinates")
            logger.info("Mouse tracking enabled")
        else:
            self.track_btn.config(text="🖱️ Track Mouse")
            self.status_var.set("Mouse tracking disabled")
            logger.info("Mouse tracking disabled")
    
    def start_position_tracking(self):
        def update():
            try:
                x, y = pyautogui.position()
                self.position_var.set(f"Mouse: ({x}, {y})")
                
                if self.position_tracking:
                    self.x_var.set(x)
                    self.y_var.set(y)
            except Exception as e:
                logger.error(f"Position tracking error: {e}")
            
            self.root.after(100, update)
        update()
    
    def start_automation(self):
        if self.running or not self.actions:
            if not self.actions:
                self.status_var.set("No actions to run! Add some actions first.")
            return
        
        self.running = True
        
        def run():
            try:
                # Countdown
                for i in range(3, 0, -1):
                    if not self.running:
                        return
                    self.root.after(0, lambda i=i: self.status_var.set(f"Starting in {i} seconds..."))
                    time.sleep(1)
                
                # Execute actions
                for i, action in enumerate(self.actions):
                    if not self.running:
                        break
                    
                    self.root.after(0, lambda i=i: self.status_var.set(f"Running action {i+1}/{len(self.actions)}: {str(action)[:50]}..."))
                    action.execute()
                
                if self.running:
                    self.root.after(0, lambda: self.status_var.set("✅ Automation completed successfully!"))
                else:
                    self.root.after(0, lambda: self.status_var.set("⏹️ Automation stopped by user"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"❌ Error: {e}"))
                logger.error(f"Automation error: {e}")
            finally:
                self.running = False
        
        threading.Thread(target=run, daemon=True).start()
    
    def stop_automation(self):
        if self.running:
            self.running = False
            self.status_var.set("Stopping automation...")
            logger.info("Automation stopped by user")
        else:
            self.status_var.set("No automation running")
    
    def clear_actions(self):
        if self.actions:
            if messagebox.askyesno("Confirm", "Clear all actions?"):
                self.actions.clear()
                self.actions_listbox.delete(0, 'end')
                self.status_var.set("All actions cleared")
    
    def save_actions(self):
        if not self.actions:
            self.status_var.set("No actions to save")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Action Sequence"
        )
        
        if filename:
            try:
                data = []
                for action in self.actions:
                    data.append({
                        'type': action.action_type,
                        'data': action.data,
                        'delay': action.delay
                    })
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.status_var.set(f"✅ Saved {len(self.actions)} actions to {filename}")
                logger.info(f"Saved actions to {filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save: {e}")
                self.status_var.set("❌ Failed to save actions")
    
    def load_actions(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Action Sequence"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                self.actions.clear()
                self.actions_listbox.delete(0, 'end')
                
                for item in data:
                    action = SimpleAction(item['type'], item['data'], item.get('delay', 0))
                    self.actions.append(action)
                    self.actions_listbox.insert('end', str(action))
                
                self.status_var.set(f"✅ Loaded {len(self.actions)} actions from {filename}")
                logger.info(f"Loaded actions from {filename}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load: {e}")
                self.status_var.set("❌ Failed to load actions")

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = WorkingAutoTyper(root)
        
        print("🚀 Playbian Auto Typer started successfully!")
        print("Features:")
        print("  ✅ Type text actions")
        print("  ✅ Mouse click actions") 
        print("  ✅ Delay actions")
        print("  ✅ Mouse tracking (click Track Mouse button)")
        print("  ✅ Save/Load sequences")
        print("  ✅ Keyboard shortcuts (F5=Start, Esc=Stop)")
        print("  ✅ Dark theme UI")
        print("\nPress F5 to start automation, Esc to stop.")
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Make sure you have pyautogui installed: pip install pyautogui")

if __name__ == "__main__":
    main()