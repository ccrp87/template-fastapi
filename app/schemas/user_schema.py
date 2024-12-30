from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserRequestSchema(BaseModel):
    username: str
    email: str
    phone:str


class UserResponseSchema(UserRequestSchema):
    id: int
    is_active: bool
    created_at: datetime 
    updated_at: Optional[datetime]