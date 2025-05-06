from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: UUID | str
    email: str
    first_name: str
    last_name: str
    services: list
    is_active: bool
    is_admin: bool
    is_service: bool
    created_at: datetime
    updated_at: datetime

    @property
    def is_authenticated(self):
        return True


class UserInputSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8)
    first_name: str = ""
    last_name: str = ""


class UserUpdateInputSchema(BaseModel):
    email: str | None = Field(None, min_length=5, max_length=320)
    password: str | None = Field(None, min_length=8)
    first_name: str | None = None
    last_name: str | None = None
    services: list | None = None


class UserDeleteSchema(BaseModel):
    success: bool
