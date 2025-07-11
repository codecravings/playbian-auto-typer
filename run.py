#!/usr/bin/env python3
"""
Playbian Auto Typer & Clicker - Application Launcher
This script handles dependency checking, setup, and launching the main application.
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

# Minimum Python version required
MIN_PYTHON_VERSION = (3, 8)

# Required packages for core functionality
CORE_PACKAGES = {
    'pyautogui': 'pyautogui>=0.9.54',
    'keyboard': 'keyboard>=1.13.0',
}

# Optional packages for enhanced features
OPTIONAL_PACKAGES = {
    'requests': 'requests>=2.31.0',  # For AI integration
    'psutil': 'psutil>=5.9.0',      # For system monitoring
    'PIL': 'Pillow>=10.0.0',        # For image operations
}

def check_python_version():
    """Check if Python version meets minimum requirements"""
    current_version = sys.version_info[:2]
    if current_version < MIN_PYTHON_VERSION:
        print(f"❌ Error: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ is required.")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        print(f"   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python version {current_version[0]}.{current_version[1]} - OK")
    return True

def check_package(package_name, install_command=None):
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_spec):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package_spec}...")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package_spec],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Successfully installed {package_spec}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_spec}: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    print("🔍 Checking dependencies...")
    
    missing_core = []
    missing_optional = []
    
    # Check core packages
    for package_name, package_spec in CORE_PACKAGES.items():
        if not check_package(package_name):
            missing_core.append(package_spec)
        else:
            print(f"✅ {package_name} - OK")
    
    # Check optional packages
    for package_name, package_spec in OPTIONAL_PACKAGES.items():
        if not check_package(package_name):
            missing_optional.append(package_spec)
        else:
            print(f"✅ {package_name} - OK")
    
    # Install missing core packages
    if missing_core:
        print(f"\n📋 Missing core dependencies: {', '.join(missing_core)}")
        print("🚀 Installing required packages...")
        
        for package_spec in missing_core:
            if not install_package(package_spec):
                print(f"\n❌ Failed to install core dependency: {package_spec}")
                print("   Please install manually using:")
                print(f"   pip install {package_spec}")
                return False
    
    # Optionally install missing optional packages
    if missing_optional:
        print(f"\n📋 Optional packages not found: {', '.join(missing_optional)}")
        print("   These packages enable additional features:")
        print("   - requests: AI integration with Gemini/OpenAI")
        print("   - psutil: System monitoring and performance stats")
        print("   - Pillow: Advanced image operations and screenshots")
        
        try:
            response = input("\n🤔 Install optional packages? (y/N): ").strip().lower()
            if response in ('y', 'yes'):
                for package_spec in missing_optional:
                    install_package(package_spec)
        except KeyboardInterrupt:
            print("\n⏸️  Installation cancelled by user")
    
    print("\n✅ Dependency check complete!")
    return True

def check_files():
    """Check if all required application files exist"""
    required_files = [
        'main_app.py',
        'config.py',
        'actions.py',
        'ui_components.py',
        'utils.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("   Please ensure all application files are present.")
        return False
    
    print("✅ All required files found")
    return True

def setup_environment():
    """Setup environment and configuration"""
    try:
        # Import config to trigger initial setup
        import config
        config.ensure_config_dir()
        print("✅ Configuration directory initialized")
        return True
    except Exception as e:
        print(f"❌ Failed to setup environment: {e}")
        return False

def launch_application():
    """Launch the main application"""
    try:
        print("🚀 Launching Playbian Auto Typer & Clicker...")
        
        # Import and run the main application
        from main_app import main
        main()
        
    except KeyboardInterrupt:
        print("\n⏸️  Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        print("\nFor help, please:")
        print("1. Check the log files in ~/.playbian_auto_typer/")
        print("2. Report issues at: https://github.com/yourusername/playbian-auto-typer/issues")
        return False
    
    return True

def show_banner():
    """Show application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         🖱️⌨️  Playbian Auto Typer & Clicker v2.1             ║
    ║                                                              ║
    ║              Modern Automation for Everyone                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_help():
    """Show help information"""
    help_text = """
Usage: python run.py [options]

Options:
  --help, -h          Show this help message
  --check-deps        Only check dependencies, don't launch
  --install-optional  Install optional packages
  --version           Show version information
  --setup             Run setup without launching

Examples:
  python run.py                    # Normal launch
  python run.py --check-deps       # Check dependencies only
  python run.py --install-optional # Install all optional packages

For more information, visit:
https://github.com/yourusername/playbian-auto-typer
    """
    print(help_text)

def show_version():
    """Show version information"""
    try:
        from config import APP_NAME, APP_VERSION, APP_AUTHOR
        print(f"{APP_NAME} v{APP_VERSION}")
        print(f"Created by {APP_AUTHOR}")
    except ImportError:
        print("Playbian Auto Typer & Clicker v2.1")
    
    print(f"Python {sys.version}")
    print(f"Platform: {sys.platform}")

def main():
    """Main launcher function"""
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--help' in args or '-h' in args:
        show_banner()
        show_help()
        return
    
    if '--version' in args:
        show_version()
        return
    
    # Show banner
    show_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if files exist
    if not check_files():
        sys.exit(1)
    
    # Handle special arguments
    if '--check-deps' in args:
        check_and_install_dependencies()
        return
    
    if '--install-optional' in args:
        # Force install all optional packages
        print("📦 Installing all optional packages...")
        for package_spec in OPTIONAL_PACKAGES.values():
            install_package(package_spec)
        return
    
    if '--setup' in args:
        check_and_install_dependencies()
        setup_environment()
        print("✅ Setup complete! Run 'python run.py' to launch the application.")
        return
    
    # Normal launch sequence
    print("🔧 Preparing to launch...")
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("\n❌ Dependency check failed. Please resolve the issues above.")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed.")
        sys.exit(1)
    
    # Launch application
    if not launch_application():
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please report this issue with the error details above.")
        sys.exit(1)
