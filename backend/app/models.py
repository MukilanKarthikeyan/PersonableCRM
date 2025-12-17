# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Contact(Base):
    """
    Contact model - stores information about people discovered through research
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    affiliation = Column(String, nullable=True)
    field = Column(String, nullable=True)
    website = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    confidence = Column(Float, nullable=True, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="contact", cascade="all, delete-orphan")
    research_sources = relationship("ResearchSource", back_populates="contact", cascade="all, delete-orphan")


class Conversation(Base):
    """
    Conversation model - tracks email threads and interactions with contacts
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    status = Column(String, default="draft")  # draft, sent, replied, follow_up
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    contact = relationship("Contact", back_populates="conversations")


class ResearchSource(Base):
    """
    ResearchSource model - tracks where contact information was found
    """
    __tablename__ = "research_sources"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    url = Column(String, nullable=False)
    extracted_at = Column(DateTime, default=datetime.utcnow)
    extraction_method = Column(String, nullable=True)  # lux_agent, manual, etc.
    
    # Relationships
    contact = relationship("Contact", back_populates="research_sources")


class ResearchTask(Base):
    """
    ResearchTask model - tracks agent research tasks
    """
    __tablename__ = "research_tasks"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    results_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)