# backend/app/lux/client.py
from oagi import Agent
from app.config import LUX_API_KEY, LUX_MODEL
import logging

logger = logging.getLogger(__name__)

_client = None

def get_lux_client() -> Agent:
    """
    Returns a singleton Lux Agent instance.
    
    The Lux agent is configured with the API key and model from environment variables.
    """
    global _client
    
    if _client is None:
        if not LUX_API_KEY:
            raise ValueError(
                "LUX_API_KEY not found. Please set it in your .env file or environment variables."
            )
        
        logger.info(f"Initializing Lux client with model: {LUX_MODEL}")
        
        try:
            _client = Agent(
                model=LUX_MODEL,
                api_key=LUX_API_KEY
            )
            logger.info("Lux client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Lux client: {str(e)}")
            raise
    
    return _client


def reset_client():
    """
    Reset the client singleton (useful for testing or reconfiguration)
    """
    global _client
    _client = None