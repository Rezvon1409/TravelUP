from sqlalchemy.orm import Session
from models.review import Review
from models.booking import Booking
from models.user import User
from fastapi import HTTPException, status


async def create_review(user: User, destination_id: int, rating: int, comment: str, db: Session):
    booking = db.query(Booking).filter(Booking.user_id == user.id,Booking.destination_id == destination_id,Booking.status == "confirmed").first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must have a confirmed booking")

    exists = db.query(Review).filter(Review.user_id == user.id,Review.destination_id == destination_id).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already reviewed this destination")

    new_review = Review(user_id=user.id,destination_id=destination_id,rating=rating,comment=comment)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


async def get_destination_reviews(destination_id: int, db: Session):
    return db.query(Review).filter(Review.destination_id == destination_id).all()


async def update_review(review_id: int, user: User, rating: int, comment: str, db: Session):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if review.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    review.rating = rating
    review.comment = comment
    db.commit()
    db.refresh(review)

    return review


async def delete_review(review_id: int, user: User, db: Session):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if review.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db.delete(review)
    db.commit()

    return {"msg": "Review deleted"}