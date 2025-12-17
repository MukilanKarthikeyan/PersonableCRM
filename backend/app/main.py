from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models import Contact
from app.schemas import ContactOut, ContactCreate
from fastapi.middleware.cors import CORSMiddleware

# Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PersonableCRM Backend")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET all contacts
@app.get("/contacts", response_model=list[ContactOut])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

# POST new contact
@app.post("/contacts", response_model=ContactOut)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
