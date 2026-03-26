from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum

class BookingCreateSchema(BaseModel):
    destination_id: int
    start_date: date
    end_date: date
    travelers_count: int
    total_price: float



class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"



class BookingUpdateStatusSchema(BaseModel):
    status: BookingStatus

class BookingSchema(BaseModel):
    id: int
    user_id: int
    destination_id: int
    start_date: date
    end_date: date
    travelers_count: int
    total_price: float
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True