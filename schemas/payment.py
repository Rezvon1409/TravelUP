from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class PaymentCreateSchema(BaseModel):
    booking_id: int
    amount: float
    currency: str = "TJS"
    provider: str

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"

class PaymentSchema(BaseModel):
    id: int
    booking_id: int
    amount: float
    currency: str
    provider: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True