from sqlalchemy.orm import Session
from app.models import Contact
from app.schemas import ContactCreate, ContactOut
from typing import List, Optional

# ------------------------------
# Create a new contact
# ------------------------------
def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# ------------------------------
# Get all contacts
# ------------------------------
def get_all_contacts(db: Session) -> List[Contact]:
    return db.query(Contact).all()

# ------------------------------
# Find a contact by email
# ------------------------------
def get_contact_by_email(db: Session, email: str) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.email == email).first()

# ------------------------------
# Update a contact
# ------------------------------
def update_contact(db: Session, contact_id: int, updates: dict) -> Optional[Contact]:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return None
    for key, value in updates.items():
        if hasattr(contact, key):
            setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact

# ------------------------------
# Delete a contact
# ------------------------------
def delete_contact(db: Session, contact_id: int) -> bool:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return False
    db.delete(contact)
    db.commit()
    return True
