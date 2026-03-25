from pydantic import BaseModel
from typing import Literal

class ProfileSchema(BaseModel):
    id : int 
    user_id : int 
    theme: Literal["light", "dark", "system"]

    class Config:
        from_attributes = True

class UpdateThemeSchema(BaseModel):
    theme: Literal["light", "dark", "system"]