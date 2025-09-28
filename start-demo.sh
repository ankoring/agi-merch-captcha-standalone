#!/bin/bash

echo "🤖 Starting AGI House Merch CAPTCHA Demo..."
echo "============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    echo "   Visit: https://python.org/"
    exit 1
fi

echo "✅ Python $(python3 --version) detected"

# Check if index.html exists
if [ ! -f "index.html" ]; then
    echo "❌ index.html not found. Please run this script from the correct directory."
    exit 1
fi

# Check if server.py exists
if [ ! -f "server.py" ]; then
    echo "❌ server.py not found. Please run this script from the correct directory."
    exit 1
fi

echo "🚀 Starting AGI CAPTCHA server..."
echo ""
echo "📱 Demo will be available at: http://localhost:8000"
echo "🔍 Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 server.py
