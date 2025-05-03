from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserOutputSchema(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    is_service: bool
    created_at: datetime
    updated_at: datetime


class UserInputSchema(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8)
    first_name: str = ""
    last_name: str = ""


class UserLoginSchema(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8)
