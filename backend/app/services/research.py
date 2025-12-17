# backend/app/services/research.py

"""
Research service - orchestrates Lux agent research and contact storage.
"""

from app.lux.tasks import execute_people_research, validate_contact_data
from app.services.crm import bulk_create_contacts, add_research_source, get_contact_by_email
from app.db import SessionLocal
from app.models import ResearchTask
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def run_research(query: str) -> dict:
    """
    Execute a complete research workflow:
    1. Create research task record
    2. Run Lux agent
    3. Validate results
    4. Store contacts in database
    5. Link research sources
    
    Args:
        query: The research query
    
    Returns:
        Dictionary with results summary
    """
    db = SessionLocal()
    task = None
    
    try:
        # Create research task record
        task = ResearchTask(
            query=query,
            status="running"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        logger.info(f"Starting research task {task.id}: {query}")
        
        # Execute Lux agent research
        contacts_data = execute_people_research(query)
        
        # Validate contacts
        valid_contacts = []
        for contact in contacts_data:
            if validate_contact_data(contact):
                valid_contacts.append(contact)
            else:
                logger.warning(f"Skipping invalid contact: {contact}")
        
        logger.info(f"Validated {len(valid_contacts)} out of {len(contacts_data)} contacts")
        
        # Store contacts in database
        created_contacts = bulk_create_contacts(db, valid_contacts)
        
        # Link research sources
        for contact_data in valid_contacts:
            email = contact_data.get('email')
            source_url = contact_data.get('source_url')
            
            if source_url:
                contact = get_contact_by_email(db, email)
                if contact:
                    add_research_source(
                        db=db,
                        contact_id=contact.id,
                        url=source_url,
                        method="lux_agent"
                    )
        
        # Update task status
        task.status = "completed"
        task.results_count = len(created_contacts)
        task.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Research task {task.id} completed successfully")
        
        return {
            "success": True,
            "task_id": task.id,
            "query": query,
            "total_found": len(contacts_data),
            "valid_contacts": len(valid_contacts),
            "new_contacts": len(created_contacts),
            "duplicates": len(valid_contacts) - len(created_contacts)
        }
        
    except Exception as e:
        logger.error(f"Research task failed: {str(e)}")
        
        # Update task status to failed
        if task:
            task.status = "failed"
            task.error_message = str(e)
            task.completed_at = datetime.utcnow()
            db.commit()
        
        return {
            "success": False,
            "task_id": task.id if task else None,
            "query": query,
            "error": str(e)
        }
        
    finally:
        db.close()


def get_research_tasks(db, skip: int = 0, limit: int = 50):
    """Get all research tasks with pagination."""
    return db.query(ResearchTask).order_by(
        ResearchTask.created_at.desc()
    ).offset(skip).limit(limit).all()


def get_research_task_by_id(db, task_id: int):
    """Get a specific research task by ID."""
    return db.query(ResearchTask).filter(ResearchTask.id == task_id).first()