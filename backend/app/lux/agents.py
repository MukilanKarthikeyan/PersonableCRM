# backend/app/lux/agents.py

from lux import LuxAgent

def people_research_agent():
    return LuxAgent(
        name="people_researcher",
        instructions="""
        You are a research agent.
        Your task is to:
        - Find people matching the given research query
        - Visit their personal or institutional pages
        - Extract name, email, website, affiliation, field
        - Only return publicly listed contact info
        - Return structured JSON only
        """
    )
