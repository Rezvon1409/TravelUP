from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.permissions import get_current_user
from models.user import User
from models.profile import UserProfile
from schemas.profile import ProfileSchema, UpdateThemeSchema

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileSchema)
async def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile


@router.patch("/theme")
async def update_theme(data: UpdateThemeSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    profile.theme = data.theme
    db.commit()
    db.refresh(profile)
    return profile