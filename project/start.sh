#!/bin/bash

# Quantum News Agent Startup Script
# This script starts the complete quantum news system

echo "🚀 Starting Quantum News Agent System..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found at ../.venv"
    echo "Please run: python -m venv ../.venv && source ../.venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source ../.venv/bin/activate

# Check if Google API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Warning: GOOGLE_API_KEY not set in environment"
    echo "   You may need to set it: export GOOGLE_API_KEY='your_key_here'"
fi

# Navigate to news_agent directory
cd news_agent

echo "📊 Running initial article processing..."
python daily_runner.py

echo ""
echo "🌐 Starting web application..."
echo "   Access at: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

# Start the web application
python enhanced_app.py