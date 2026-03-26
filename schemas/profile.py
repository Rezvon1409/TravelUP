from pydantic import BaseModel
from typing import Literal

class ProfileSchema(BaseModel):
    id: int
    user_id: int
    theme: Literal["light", "dark", "system"]
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    age: int | None = None
    bio: str | None = None
    phone: str | None = None

    class Config:
        from_attributes = True


class UpdateProfileSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    age: int | None = None
    bio: str | None = None
    phone: str | None = None


class UpdateThemeSchema(BaseModel):
    theme: Literal["light", "dark", "system"]