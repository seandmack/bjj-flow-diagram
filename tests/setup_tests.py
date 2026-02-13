#!/usr/bin/env python3
"""
Cross-platform setup script for BJJ Flow Diagram tests
Works on Windows, Mac, and Linux
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, shell=False, suppress_output=True):
    """Run a command and return success status."""
    try:
        if suppress_output:
            subprocess.run(cmd, shell=shell, check=True, capture_output=True)
        else:
            subprocess.run(cmd, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode() if e.stderr else str(e)}")
        return False

def main():
    print("\n🥋 BJJ Flow Diagram Test Setup")
    print("=" * 40)
    print(f"Platform: {platform.system()}")
    print()

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} found")

    # Install system dependencies on Linux
    if platform.system() == "Linux":
        print("\n📦 Installing system dependencies for Playwright...")
        system_deps = [
            "libatk1.0-0t64", "libatk-bridge2.0-0t64", "libcups2t64",
            "libdrm2", "libxkbcommon0", "libatspi2.0-0t64",
            "libxcomposite1", "libxdamage1", "libxfixes3",
            "libxrandr2", "libgbm1", "libasound2t64"
        ]
        cmd = ["sudo", "apt-get", "install", "-y"] + system_deps
        if not run_command(cmd, suppress_output=False):
            print("⚠️  System dependencies installation had issues, but continuing...")
        else:
            print("✅ System dependencies installed")

    # Create virtual environment
    print("\n📦 Creating virtual environment...")
    if not run_command([sys.executable, "-m", "venv", "venv"]):
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    print("✅ Virtual environment created")

    # Determine activation command based on OS
    if platform.system() == "Windows":
        pip_cmd = os.path.join("venv", "Scripts", "pip")
        activate_cmd = os.path.join("venv", "Scripts", "activate.bat")
    else:
        pip_cmd = os.path.join("venv", "bin", "pip")
        activate_cmd = f"source {os.path.join('venv', 'bin', 'activate')}"

    # Upgrade pip
    print("\n🔧 Upgrading pip...")
    run_command([pip_cmd, "install", "--quiet", "--upgrade", "pip"])

    # Install dependencies
    print("\n📥 Installing dependencies...")
    if not run_command([pip_cmd, "install", "--quiet", "-r", "requirements.txt"]):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    print("✅ Dependencies installed")

    # Install Playwright browsers
    print("\n🌐 Installing Playwright browsers...")
    playwright_cmd = os.path.join("venv", "Scripts" if platform.system() == "Windows" else "bin", "playwright")
    if not run_command([playwright_cmd, "install", "chromium"]):
        print("❌ Failed to install Playwright browsers")
        sys.exit(1)
    print("✅ Playwright browsers installed")

    # Create test reports directory
    print("\n📁 Creating test reports directory...")
    os.makedirs("test-reports/screenshots", exist_ok=True)
    print("✅ Test reports directory created")

    # Success message
    print("\n" + "=" * 40)
    print("✅ Setup complete!")
    print("=" * 40)
    print("\nTo run tests:")
    print("\n  1. Start the local server (in one terminal):")
    print("     python -m http.server 8000")
    print("\n  2. In another terminal, activate the virtual environment:")
    print(f"     {activate_cmd}")
    print("\n  3. Run the tests:")
    print("     pytest                    # Run all tests")
    print("     pytest -m smoke          # Run smoke tests only")
    print("     pytest test_counters.py  # Run counter tests only")
    print("\n  4. View the test report:")
    if platform.system() == "Windows":
        print("     start test-reports\\report.html")
    elif platform.system() == "Darwin":  # Mac
        print("     open test-reports/report.html")
    else:  # Linux
        print("     xdg-open test-reports/report.html")
    print()

if __name__ == "__main__":
    main()
