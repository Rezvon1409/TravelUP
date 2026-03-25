from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.permissions import get_current_user, get_admin_user
from models.user import User
from schemas.payment import PaymentSchema, PaymentCreateSchema
from services.payment import create_payment, get_my_payments, get_all_payments
from typing import List

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", response_model=PaymentSchema)
async def pay(data: PaymentCreateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await create_payment(user, data.booking_id, data.amount, data.currency, data.provider, db)


@router.get("/my", response_model=List[PaymentSchema])
async def my_payments(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await get_my_payments(user, db)


@router.get("", response_model=List[PaymentSchema])
async def all_payments(user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return await get_all_payments(db)