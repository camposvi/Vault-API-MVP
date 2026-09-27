from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6, json_schema_extra={"format":"password"})


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
