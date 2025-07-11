# 🖱️⌨️ Playbian Auto Typer & Clicker v2.1

A modern, feature-rich automation tool for keyboard and mouse actions with a beautiful dark mode interface, AI integration capabilities, and enhanced user experience.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.1-brightgreen)

## ✨ Features

### 🎨 Modern Dark UI
- **Glassmorphism-inspired design** with modern dark theme
- **Responsive layout** that adapts to different screen sizes
- **Smooth animations** and hover effects
- **Professional color scheme** optimized for long usage sessions

### 🔧 Enhanced Automation
- **Multiple action types**: Typing, clicking, delays, hotkeys, special keys
- **Drag & drop** action reordering
- **Loop execution** with customizable intervals
- **Real-time progress tracking** during automation
- **Action validation** and error handling

### 🤖 AI Integration (Future-Ready)
- **Gemini API support** for intelligent action generation
- **OpenAI GPT integration** for natural language automation
- **Smart action suggestions** and optimization
- **Action sequence explanation** in plain English

### 🎯 Advanced Features
- **Mouse position tracking** with Ctrl+T hotkey (changed from F2)
- **Screenshot capture** and image recognition
- **Action templates** and sequence sharing
- **Comprehensive settings** and preferences
- **Recent files** management
- **Auto-save** functionality

### 🛡️ Reliability & Safety
- **Error handling** with detailed logging
- **Action validation** before execution
- **Emergency stop** functionality (Esc key)
- **Backup system** for sequences
- **System resource monitoring**

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11, macOS 10.15+, or modern Linux distribution

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/playbian-auto-typer.git
   cd playbian-auto-typer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main_app.py
   ```

### Alternative: Minimal Installation
For core features only:
```bash
pip install pyautogui keyboard
python main_app.py
```

## 📁 Project Structure

```
playbian-auto-typer/
├── main_app.py           # Main application entry point
├── config.py             # Configuration and constants
├── actions.py            # Action classes and automation logic
├── ui_components.py      # UI components and modern styling
├── api_integration.py    # AI API integration (Gemini, OpenAI)
├── utils.py              # Utility functions and helpers
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── docs/                # Additional documentation (future)
```

## 🎮 Usage Guide

### Creating Actions

1. **Typing Actions**:
   - Enter text in the Type tab
   - Use special keys like `<enter>`, `<tab>`, `<ctrl>` for special characters
   - Set delays for precise timing

2. **Click Actions**:
   - Use Ctrl+T to track mouse position in real-time
   - Specify exact coordinates or capture current position
   - Choose left, right, or middle mouse button

3. **Delays**:
   - Add waiting periods between actions
   - Useful for page loads or animations

4. **Hotkeys**:
   - Create keyboard shortcuts like `ctrl,c` or `alt,tab`
   - Supports complex combinations

5. **Special Keys**:
   - Individual key presses (Enter, Escape, Arrow keys, etc.)
   - Function keys F1-F12 supported

### Managing Sequences

- **Drag & Drop**: Reorder actions by dragging them
- **Edit**: Double-click or press Enter on any action
- **Duplicate**: Ctrl+D to copy actions
- **Delete**: Delete key or right-click menu
- **Save/Load**: Ctrl+S to save, Ctrl+O to load sequences

### Automation Control

- **Start**: F5 or click the Start button
- **Stop**: Esc key or click the Stop button  
- **Loop**: Enable looping with custom count and intervals
- **Progress**: Real-time status updates during execution

## ⌨️ Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Start Automation | F5 | Begin executing the action sequence |
| Stop Automation | Esc | Emergency stop for running automation |
| Track Mouse | Ctrl+T | Toggle mouse position tracking |
| Save Sequence | Ctrl+S | Save current action sequence |
| Load Sequence | Ctrl+O | Open saved sequence file |
| New Sequence | Ctrl+N | Create new empty sequence |
| Delete Action | Delete | Remove selected action |
| Edit Action | Enter | Edit selected action |
| Duplicate Action | Ctrl+D | Copy selected action |
| Toggle Theme | Ctrl+Shift+T | Switch between themes |
| Help | F1 | Show help and documentation |

## 🔧 Configuration

### Settings File
Settings are automatically saved to:
- **Windows**: `%USERPROFILE%/.playbian_auto_typer/settings.json`
- **macOS/Linux**: `~/.playbian_auto_typer/settings.json`

### AI Integration Setup
To enable AI features:

1. **For Gemini AI**:
   - Get API key from [Google AI Studio](https://makersuite.google.com/)
   - Add to settings: `api_config.gemini.api_key = "your_key_here"`

2. **For OpenAI**:
   - Get API key from [OpenAI Platform](https://platform.openai.com/)
   - Add to settings: `api_config.openai.api_key = "your_key_here"`

## 🎨 Major Improvements in v2.1

### ✅ UI/UX Enhancements
- [x] **Complete dark mode redesign** with modern glassmorphism styling
- [x] **Improved navigation** with tabbed interface
- [x] **Enhanced visual feedback** with status icons and colors
- [x] **Better typography** and spacing for readability
- [x] **Responsive design** that works on different screen sizes

### ✅ Functionality Improvements
- [x] **Changed mouse tracking hotkey** from F2 to Ctrl+T for better accessibility
- [x] **Enhanced action list** with drag-and-drop reordering
- [x] **Improved error handling** with detailed error messages
- [x] **Better file management** with recent files and auto-save
- [x] **Advanced settings system** with persistent configuration

### ✅ Code Organization
- [x] **Modular architecture** split into logical components
- [x] **Separation of concerns** between UI, logic, and configuration
- [x] **Better error handling** and logging throughout
- [x] **Comprehensive documentation** and code comments
- [x] **Type hints** and improved code quality

### ✅ Future-Ready Features
- [x] **AI API integration framework** ready for Gemini and OpenAI
- [x] **Plugin architecture** for extensibility
- [x] **Comprehensive logging** and debugging tools
- [x] **Performance monitoring** and optimization hooks

## 🔮 Planned Features

- [ ] **Custom themes** and UI customization
- [ ] **Plugin system** for third-party extensions
- [ ] **Macro recording** from user actions
- [ ] **Cloud sync** for sequences across devices
- [ ] **Team collaboration** features
- [ ] **Mobile companion app** for remote control
- [ ] **Advanced scripting** with Python code blocks
- [ ] **Image-based automation** with computer vision

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Permission denied on Windows**:
   - Run as administrator
   - Check Windows Defender settings

3. **Mouse tracking not working**:
   - Check if Ctrl+T hotkey conflicts with other software
   - Try restarting the application

4. **Automation not starting**:
   - Ensure no actions list is empty
   - Check for validation errors in status bar

### Getting Help

1. **Check the logs**: Located in `~/.playbian_auto_typer/app.log`
2. **Generate error report**: Use the built-in error reporting tool
3. **Create an issue**: Report bugs on GitHub with system information

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper testing
4. **Follow code style**: Use black for formatting
5. **Submit a pull request** with detailed description

### Development Setup

```bash
# Clone and enter directory
git clone https://github.com/yourusername/playbian-auto-typer.git
cd playbian-auto-typer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run tests
pytest tests/

# Format code
black .

# Run linting
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyAutoGUI** - Core automation functionality
- **Keyboard** - Global hotkey support  
- **Tkinter** - GUI framework
- **Modern UI inspiration** - Various design systems and frameworks
- **Community feedback** - User suggestions and bug reports

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/playbian-auto-typer/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/playbian-auto-typer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/playbian-auto-typer/discussions)
- **Email**: support@playbian.com

## 🔄 Version History

### v2.1 (Current)
- Complete UI redesign with dark mode
- Modular code architecture
- AI integration framework
- Enhanced user experience
- Improved error handling
- Better documentation

### v2.0
- Major stability improvements
- New action types
- Better file management
- Enhanced settings system

### v1.0
- Initial release
- Basic automation features
- Simple UI
- Core functionality

---

**Made with ❤️ by the Playbian Team**

*Automating the world, one click at a time!*
