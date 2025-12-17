# backend/app/services/crm.py

"""
CRM service layer - handles all contact-related business logic.
"""

from sqlalchemy.orm import Session
from app.models import Contact, Conversation, ResearchSource
from app.schemas import ContactCreate, ContactUpdate, ConversationCreate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


# ==================== Contact Operations ====================

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    """Create a new contact in the database."""
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    logger.info(f"Created contact: {db_contact.name} ({db_contact.email})")
    return db_contact


def get_all_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    """Get all contacts with pagination."""
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact_by_id(db: Session, contact_id: int) -> Optional[Contact]:
    """Get a contact by ID."""
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contact_by_email(db: Session, email: str) -> Optional[Contact]:
    """Find a contact by email address."""
    return db.query(Contact).filter(Contact.email == email).first()


def update_contact(db: Session, contact_id: int, updates: ContactUpdate) -> Optional[Contact]:
    """Update a contact with new information."""
    contact = get_contact_by_id(db, contact_id)
    if not contact:
        return None
    
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)
    
    db.commit()
    db.refresh(contact)
    logger.info(f"Updated contact: {contact.name}")
    return contact


def delete_contact(db: Session, contact_id: int) -> bool:
    """Delete a contact and all related data."""
    contact = get_contact_by_id(db, contact_id)
    if not contact:
        return False
    
    db.delete(contact)
    db.commit()
    logger.info(f"Deleted contact: {contact.name}")
    return True


def search_contacts(db: Session, query: str) -> List[Contact]:
    """Search contacts by name, email, or affiliation."""
    search_pattern = f"%{query}%"
    return db.query(Contact).filter(
        (Contact.name.ilike(search_pattern)) |
        (Contact.email.ilike(search_pattern)) |
        (Contact.affiliation.ilike(search_pattern)) |
        (Contact.field.ilike(search_pattern))
    ).all()


# ==================== Conversation Operations ====================

def create_conversation(db: Session, conversation: ConversationCreate) -> Conversation:
    """Create a new conversation entry."""
    db_conversation = Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    logger.info(f"Created conversation for contact_id: {conversation.contact_id}")
    return db_conversation


def get_conversations_by_contact(db: Session, contact_id: int) -> List[Conversation]:
    """Get all conversations for a specific contact."""
    return db.query(Conversation).filter(
        Conversation.contact_id == contact_id
    ).order_by(Conversation.created_at.desc()).all()


def update_conversation_status(db: Session, conversation_id: int, status: str) -> Optional[Conversation]:
    """Update the status of a conversation."""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        return None
    
    conversation.status = status
    db.commit()
    db.refresh(conversation)
    return conversation


# ==================== Research Source Operations ====================

def add_research_source(db: Session, contact_id: int, url: str, method: str = "lux_agent") -> ResearchSource:
    """Add a research source to a contact."""
    source = ResearchSource(
        contact_id=contact_id,
        url=url,
        extraction_method=method
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def get_research_sources(db: Session, contact_id: int) -> List[ResearchSource]:
    """Get all research sources for a contact."""
    return db.query(ResearchSource).filter(
        ResearchSource.contact_id == contact_id
    ).all()


# ==================== Bulk Operations ====================

def bulk_create_contacts(db: Session, contacts: List[dict]) -> List[Contact]:
    """
    Create multiple contacts at once.
    Skips duplicates based on email.
    
    Returns:
        List of created contacts (excluding duplicates)
    """
    created = []
    skipped = []
    
    for contact_data in contacts:
        email = contact_data.get('email')
        
        # Check if contact already exists
        existing = get_contact_by_email(db, email)
        if existing:
            skipped.append(email)
            logger.info(f"Skipping duplicate contact: {email}")
            continue
        
        # Create new contact
        try:
            contact = Contact(**contact_data)
            db.add(contact)
            created.append(contact)
        except Exception as e:
            logger.error(f"Error creating contact {email}: {str(e)}")
            continue
    
    if created:
        db.commit()
        for contact in created:
            db.refresh(contact)
    
    logger.info(f"Bulk create: {len(created)} created, {len(skipped)} skipped")
    return created