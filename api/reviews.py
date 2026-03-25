from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.permissions import get_current_user
from models.user import User
from schemas.review import ReviewSchema, ReviewCreateSchema, ReviewUpdateSchema
from services.review import create_review, get_destination_reviews, update_review, delete_review
from typing import List

router = APIRouter(tags=["Reviews"])


@router.post("/reviews", response_model=ReviewSchema)
async def add_review(data: ReviewCreateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await create_review(user, data.destination_id, data.rating, data.comment, db)


@router.get("/destinations/{id}/reviews", response_model=List[ReviewSchema])
async def destination_reviews(id: int, db: Session = Depends(get_db)):
    return await get_destination_reviews(id, db)


@router.put("/reviews/{id}", response_model=ReviewSchema)
async def edit_review(id: int, data: ReviewUpdateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await update_review(id, user, data.rating, data.comment, db)


@router.delete("/reviews/{id}")
async def remove_review(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await delete_review(id, user, db)