from pydantic import BaseModel
from datetime import datetime

class DestinationCreateSchema(BaseModel):
    title: str
    description: str
    country: str
    city: str
    cover_image: str
    rating: float = 0.0

class DestinationSchema(BaseModel):
    id: int
    title: str
    description: str
    country: str
    city: str
    cover_image: str
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True