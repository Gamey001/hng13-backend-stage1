# app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class StringRow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sha256_hash: str = Field(index=True, unique=True)
    value: str
    properties: str  # JSON string
    created_at: datetime
