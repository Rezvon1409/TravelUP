from pydantic import BaseModel
from datetime import date, datetime
from typing import Literal

class BookingCreateSchema(BaseModel):
    destination_id: int
    start_date: date
    end_date: date
    travelers_count: int
    total_price: float

class BookingUpdateStatusSchema(BaseModel):
    status: Literal["pending", "confirmed", "cancelled"]

class BookingSchema(BaseModel):
    id: int
    user_id: int
    destination_id: int
    start_date: date
    end_date: date
    travelers_count: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True