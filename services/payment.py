from sqlalchemy.orm import Session
from models.payment import Payment
from models.booking import Booking
from models.user import User
from fastapi import HTTPException, status


async def create_payment(user: User, booking_id: int, amount: float, currency: str, provider: str, db: Session):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if booking.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    exists = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment already exists")

    new_payment = Payment(booking_id=booking_id,amount=amount,currency=currency,provider=provider,status="pending")
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


async def get_my_payments(user: User, db: Session):
    return db.query(Payment).join(Booking).filter(Booking.user_id == user.id).all()


async def get_all_payments(db: Session):
    return db.query(Payment).all()