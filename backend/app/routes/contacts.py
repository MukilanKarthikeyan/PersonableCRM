# backend/app/routes/contacts.py
from fastapi import APIRouter
from app.db import SessionLocal
from app.models import Contact
from app.schemas import ContactOut

router = APIRouter()

@router.get("/contacts")
def get_contacts():
    db = SessionLocal()
    contacts = db.query(Contact).all()
    return [ContactOut.from_orm(c) for c in contacts]
