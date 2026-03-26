from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.permissions import get_current_user, get_admin_user
from models.user import User
from models.profile import UserProfile
from schemas.profile import ProfileSchema, UpdateThemeSchema, UpdateProfileSchema

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



@router.patch("/update", response_model=ProfileSchema)
async def update_profile(data: UpdateProfileSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


@router.patch("/admin/update/{user_id}", response_model=ProfileSchema)
async def admin_update_profile(user_id: int, data: UpdateProfileSchema, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(profile, key, value)

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