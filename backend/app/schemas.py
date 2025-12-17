from pydantic import BaseModel
from typing import Optional

# Used for reading data from DB
class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    affiliation: Optional[str]
    field: Optional[str]
    website: Optional[str]
    source_url: Optional[str]

    class Config:
        orm_mode = True

# Used for creating new contacts
class ContactCreate(BaseModel):
    name: str
    email: str
    affiliation: Optional[str]
    field: Optional[str]
    website: Optional[str]
    source_url: Optional[str]
