#!/usr/bin/env bash
set -e

echo "🔧 Setting up Lux CRM backend environment..."

# Ensure Python exists
if ! command -v python &> /dev/null
then
    echo "❌ Python not found. Please install Python 3.10+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Backend environment setup complete!"
echo ""
echo "To activate later:"
echo "source venv/bin/activate"
