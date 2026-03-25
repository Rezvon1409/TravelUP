from pydantic import BaseModel
from datetime import datetime


class PaymentCreateSchema(BaseModel):
    booking_id: int
    amount: float
    currency: str = "TJS"
    provider: str

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