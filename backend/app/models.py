from sqlalchemy import Column, Integer, String
from .db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    affiliation = Column(String, nullable=True)
    field = Column(String, nullable=True)
    website = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
