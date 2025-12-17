Write-Host "🔧 Setting up Lux CRM backend environment..."

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Install Python 3.10+ and add to PATH."
    exit 1
}

# Create venv
Write-Host "📦 Creating virtual environment..."
python -m venv venv

# Activate venv
Write-Host "⚡ Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
Write-Host "📥 Installing dependencies..."
pip install -r requirements.txt

Write-Host "✅ Backend environment setup complete!"
Write-Host ""
Write-Host "To activate later:"
Write-Host ".\venv\Scripts\Activate.ps1"
