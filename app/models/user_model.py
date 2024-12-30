from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    phone:str
    email: str
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field()
    updated_at: Optional[datetime] = Field(default=None)

