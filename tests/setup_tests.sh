#!/bin/bash

# BJJ Flow Diagram Test Setup Script

echo "🥋 BJJ Flow Diagram Test Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create test reports directory
echo ""
echo "📁 Creating test reports directory..."
mkdir -p test-reports/screenshots

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run tests:"
echo "  1. Start the local server:"
echo "     python3 -m http.server 8000"
echo ""
echo "  2. In another terminal, activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Run the tests:"
echo "     pytest                    # Run all tests"
echo "     pytest -m smoke          # Run smoke tests only"
echo "     pytest test_counters.py  # Run counter tests only"
echo ""
echo "  4. View the test report:"
echo "     open test-reports/report.html"
echo ""
