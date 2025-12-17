from oagi import Agent
from app.db import SessionLocal
from app.models import Contact

def run_research(query: str):
    agent = Agent(model="lux-thinker-1")
    task_description = f"""
    You are a research agent. Find people relevant to the query:
    '{query}'
    Extract:
    - Name
    - Email (publicly listed only)
    - Affiliation / Institution
    - Field of research
    - Personal website (if available)
    Return results as structured JSON.
    """
    results = agent.execute(task_description)

    db = SessionLocal()
    for person in results:
        contact = Contact(
            name=person.get("name"),
            email=person.get("email"),
            website=person.get("website"),
            affiliation=person.get("affiliation"),
            field=person.get("field"),
            source_url=person.get("source_url")
        )
        db.add(contact)
    db.commit()
