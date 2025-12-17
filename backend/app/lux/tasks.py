# backend/app/lux/tasks.py

"""
Task execution functions for Lux agents.

This module handles the actual execution of Lux agent tasks
and parsing of results.
"""

from app.lux.client import get_lux_client
from app.lux.agents import get_people_research_instructions, get_enrichment_instructions
import json
import logging

logger = logging.getLogger(__name__)


def execute_people_research(query: str) -> list:
    """
    Execute a people research task using the Lux agent.
    
    Args:
        query: The research query
    
    Returns:
        List of contact dictionaries
    
    Raises:
        Exception: If the agent fails or returns invalid data
    """
    try:
        client = get_lux_client()
        instructions = get_people_research_instructions(query)
        
        logger.info(f"Starting Lux research for query: {query}")
        
        # Execute the agent task
        result = client.execute(instructions)
        
        logger.debug(f"Raw Lux response: {result}")
        
        # Parse the result
        contacts = parse_agent_response(result)
        
        logger.info(f"Successfully extracted {len(contacts)} contacts")
        
        return contacts
        
    except Exception as e:
        logger.error(f"Lux research failed: {str(e)}")
        raise


def execute_contact_enrichment(contact_data: dict) -> dict:
    """
    Enrich an existing contact with additional information.
    
    Args:
        contact_data: Basic contact information
    
    Returns:
        Enrichment data dictionary
    """
    try:
        client = get_lux_client()
        instructions = get_enrichment_instructions(contact_data)
        
        logger.info(f"Enriching contact: {contact_data.get('name')}")
        
        result = client.execute(instructions)
        enrichment = parse_agent_response(result)
        
        logger.info("Contact enrichment successful")
        
        return enrichment
        
    except Exception as e:
        logger.error(f"Contact enrichment failed: {str(e)}")
        raise


def parse_agent_response(response: str) -> any:
    """
    Parse the agent's response, which should be JSON.
    
    Args:
        response: Raw response from the agent
    
    Returns:
        Parsed Python object (list or dict)
    
    Raises:
        ValueError: If response is not valid JSON
    """
    # Handle case where response might be wrapped in markdown code blocks
    if isinstance(response, str):
        # Remove markdown code blocks if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]  # Remove ```json
        if response.startswith("```"):
            response = response[3:]  # Remove ```
        if response.endswith("```"):
            response = response[:-3]  # Remove trailing ```
        response = response.strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse agent response as JSON: {e}")
            logger.debug(f"Response content: {response}")
            raise ValueError(f"Agent returned invalid JSON: {str(e)}")
    
    return response


def validate_contact_data(contact: dict) -> bool:
    """
    Validate that a contact has minimum required fields.
    
    Args:
        contact: Contact dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['name', 'email']
    
    for field in required_fields:
        if not contact.get(field):
            logger.warning(f"Contact missing required field: {field}")
            return False
    
    # Basic email validation
    email = contact.get('email', '')
    if '@' not in email or '.' not in email:
        logger.warning(f"Invalid email format: {email}")
        return False
    
    return True