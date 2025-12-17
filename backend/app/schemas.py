# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ==================== Contact Schemas ====================

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    affiliation: Optional[str] = None
    field: Optional[str] = None
    website: Optional[str] = None
    source_url: Optional[str] = None
    confidence: Optional[float] = 1.0


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    affiliation: Optional[str] = None
    field: Optional[str] = None
    website: Optional[str] = None
    source_url: Optional[str] = None
    confidence: Optional[float] = None


class ContactOut(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# ==================== Conversation Schemas ====================

class ConversationBase(BaseModel):
    subject: Optional[str] = None
    body: str
    status: str = "draft"


class ConversationCreate(ConversationBase):
    contact_id: int


class ConversationOut(ConversationBase):
    id: int
    contact_id: int
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# ==================== Research Schemas ====================

class ResearchTaskCreate(BaseModel):
    query: str


class ResearchTaskOut(BaseModel):
    id: int
    query: str
    status: str
    results_count: int
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True


class ResearchSourceOut(BaseModel):
    id: int
    contact_id: int
    url: str
    extracted_at: datetime
    extraction_method: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True


# ==================== Response Schemas ====================

class ContactDetailOut(ContactOut):
    conversations: List[ConversationOut] = []
    research_sources: List[ResearchSourceOut] = []

    class Config:
        from_attributes = True
        orm_mode = True