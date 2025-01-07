from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class LoginRequestSchema(BaseModel):
    user_name: str
    password: str


class LoginResponseSchema(BaseModel):
    user_name: str
    email: str
    token: str