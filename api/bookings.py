from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.permissions import get_current_user, get_admin_user
from models.user import User
from schemas.booking import BookingSchema, BookingCreateSchema, BookingUpdateStatusSchema
from services.booking import create_booking, get_my_bookings, get_all_bookings, cancel_booking, update_booking_status
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingSchema)
async def book(data: BookingCreateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await create_booking(user, data.destination_id, data.start_date, data.end_date, data.travelers_count, data.total_price, db)


@router.get("/my", response_model=List[BookingSchema])
async def my_bookings(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await get_my_bookings(user, db)


@router.get("", response_model=List[BookingSchema])
async def all_bookings(user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return await get_all_bookings(db)


@router.patch("/{id}/cancel", response_model=BookingSchema)
async def cancel(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await cancel_booking(id, user, db)


@router.patch("/{id}/status", response_model=BookingSchema)
async def update_status(id: int, data: BookingUpdateStatusSchema, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return await update_booking_status(id, data.status, db)