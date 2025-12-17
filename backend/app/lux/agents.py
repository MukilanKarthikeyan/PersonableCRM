# backend/app/lux/agents.py

"""
Agent definitions for Lux-powered research.

This module defines the instructions and behavior for the Lux agent
that performs people research and contact extraction.
"""

def get_people_research_instructions(query: str) -> str:
    """
    Generate instructions for the Lux agent to research people.
    
    Args:
        query: The research query (e.g., "robotics professors at MIT")
    
    Returns:
        Detailed instructions for the agent
    """
    return f"""
You are an expert research agent specialized in finding and extracting professional contact information.

YOUR TASK:
Find people relevant to the following query: "{query}"

STEP-BY-STEP PROCESS:
1. Search the web for people matching the query
2. Visit their personal pages, institutional pages, or professional profiles
3. Extract the following information (only if publicly available):
   - Full name
   - Email address (only if publicly listed)
   - Website or personal page URL
   - Current affiliation (university, company, etc.)
   - Field of work/research
   - Source URL where you found this information

CRITICAL REQUIREMENTS:
- Only extract emails that are publicly displayed (no scraping behind logins)
- Verify that contact information is current
- Focus on academic, professional, or business contexts
- Skip personal social media profiles unless they contain professional info
- Be thorough but respectful of privacy

OUTPUT FORMAT:
Return your findings as a JSON array of objects with this structure:
[
  {{
    "name": "Full Name",
    "email": "email@domain.edu",
    "website": "https://...",
    "affiliation": "Institution/Company",
    "field": "Research area or job role",
    "source_url": "https://where-you-found-this"
  }}
]

IMPORTANT:
- Return ONLY valid JSON, no additional text
- Each person must have at least: name and email
- If you can't find enough valid contacts, return an empty array []
- Aim for quality over quantity (5-10 high-quality contacts is better than 50 low-quality ones)
"""


def get_enrichment_instructions(contact_data: dict) -> str:
    """
    Generate instructions for enriching an existing contact.
    
    Args:
        contact_data: Basic contact information to enrich
    
    Returns:
        Instructions for the enrichment agent
    """
    return f"""
You are a contact enrichment specialist. Given basic information about a person,
find additional context to make outreach more personalized.

CONTACT TO ENRICH:
Name: {contact_data.get('name')}
Email: {contact_data.get('email')}
Website: {contact_data.get('website', 'Not provided')}

YOUR TASK:
1. Visit their website or find recent information about them
2. Find:
   - Recent publications, projects, or work
   - Current research interests or business focus
   - Recent news or updates about them
   - Any public statements about what they're looking for (collaborations, etc.)

OUTPUT FORMAT:
Return a JSON object with:
{{
  "recent_work": "Brief description of recent projects/publications",
  "interests": ["interest1", "interest2", "interest3"],
  "context": "Any relevant context for personalized outreach",
  "last_updated": "When this information was found"
}}

Return ONLY valid JSON, no additional text.
"""