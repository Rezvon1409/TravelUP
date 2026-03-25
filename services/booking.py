from sqlalchemy.orm import Session
from models.booking import Booking
from models.user import User
from fastapi import HTTPException, status
from datetime import date


async def create_booking(user: User, destination_id: int, start_date: date, end_date: date, travelers_count: int, total_price: float, db: Session):
    if start_date >= end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date must be after start_date")

    new_booking = Booking(user_id=user.id,destination_id=destination_id,start_date=start_date,end_date=end_date,travelers_count=travelers_count,total_price=total_price,status="pending")
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


async def get_my_bookings(user: User, db: Session):
    return db.query(Booking).filter(Booking.user_id == user.id).all()


async def get_all_bookings(db: Session):
    return db.query(Booking).all()


async def cancel_booking(booking_id: int, user: User, db: Session):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if booking.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if booking.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking already cancelled")

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return booking


async def update_booking_status(booking_id: int, new_status: str, db: Session):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    booking.status = new_status
    db.commit()
    db.refresh(booking)

    return booking