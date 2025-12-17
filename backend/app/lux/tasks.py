# backend/app/lux/tasks.py

def build_people_task(query: str):
    return {
        "goal": f"Find people relevant to: {query}",
        "steps": [
            "Search the web for relevant people",
            "Visit candidate pages",
            "Extract structured contact info",
            "Validate emails are publicly listed"
        ],
        "output_schema": {
            "type": "array",
            "items": {
                "name": "string",
                "email": "string",
                "website": "string",
                "affiliation": "string",
                "field": "string",
                "source_url": "string"
            }
        }
    }
