"""Schemas for the database models"""

from datetime import datetime
from pydantic import BaseModel, Field

# from config import ALLOWED_EXTENSIONS

class account(BaseModel):
    id: int
    name: str
    merchant: int # foreign key to merchant
    lastfour: int = Field(min=0,le=10000) # max 4
    balance: int # store currency as integer

class address(BaseModel):
    id: int
    name: str
    street1: str | None = None # optional
    street2: str | None = None # optional
    city: str | None = None # optional
    state: str | None = None # optional
    postal: str | None = None # optional
    country: str

class category(BaseModel):
    id: int
    name: str

class merchant(BaseModel):
    id: int
    name: str
    location: int | None = None # optional, foreign key to location

class receipt (BaseModel):
    id: int
    date: datetime
    category: int # foreign key to category
    tags: str | None = None # optional
    items: str | None = None # optional
    merchant: int # foreign key to merchant
    location: int # foreign key to address
    account: int # foreign key to account
    amount: int # store currency as integer
    income: bool
    image: str | None = None # optional, base64 string of the receipt img