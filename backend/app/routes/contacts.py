# backend/app/routes/contacts.py

"""
Contact management API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import (
    ContactOut, 
    ContactCreate, 
    ContactUpdate,
    ContactDetailOut,
    ConversationCreate,
    ConversationOut
)
from app.services import crm
from typing import List

router = APIRouter()


@router.get("/contacts", response_model=List[ContactOut])
def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get all contacts with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    contacts = crm.get_all_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/contacts/search", response_model=List[ContactOut])
def search_contacts(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Search contacts by name, email, affiliation, or field.
    
    - **q**: Search query string
    """
    contacts = crm.search_contacts(db, q)
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactDetailOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Get a specific contact by ID with full details including conversations and sources.
    """
    contact = crm.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/contacts", response_model=ContactOut, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Create a new contact manually.
    
    Checks for duplicate emails before creating.
    """
    # Check if email already exists
    existing = crm.get_contact_by_email(db, contact.email)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Contact with email {contact.email} already exists"
        )
    
    return crm.create_contact(db, contact)


@router.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: int, 
    updates: ContactUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing contact.
    
    Only provided fields will be updated.
    """
    contact = crm.update_contact(db, contact_id, updates)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Delete a contact and all related data (conversations, research sources).
    """
    success = crm.delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None


# ==================== Conversation Routes ====================

@router.post("/contacts/{contact_id}/conversations", response_model=ConversationOut, status_code=201)
def create_conversation(
    contact_id: int,
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation/email thread for a contact.
    """
    # Verify contact exists
    contact = crm.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # Override contact_id from path
    conversation.contact_id = contact_id
    
    return crm.create_conversation(db, conversation)


@router.get("/contacts/{contact_id}/conversations", response_model=List[ConversationOut])
def list_conversations(contact_id: int, db: Session = Depends(get_db)):
    """
    Get all conversations for a specific contact.
    """
    # Verify contact exists
    contact = crm.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return crm.get_conversations_by_contact(db, contact_id)


@router.patch("/conversations/{conversation_id}/status", response_model=ConversationOut)
def update_conversation_status(
    conversation_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Update the status of a conversation.
    
    Valid statuses: draft, sent, replied, follow_up
    """
    valid_statuses = ["draft", "sent", "replied", "follow_up"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    conversation = crm.update_conversation_status(db, conversation_id, status)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation