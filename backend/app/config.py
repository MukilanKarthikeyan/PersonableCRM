# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Lux API Configuration
LUX_API_KEY = os.getenv("LUX_API_KEY")
LUX_MODEL = os.getenv("LUX_MODEL", "lux-thinker-1")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm.db")

# Application Configuration
APP_NAME = "PersonableCRM"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")