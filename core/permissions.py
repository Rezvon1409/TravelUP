from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, selectinload

from database import get_db
from core.security import decode_token
from models.user import User, Role
from models.booking import Booking
from models.review import Review


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    user = (db.query(User).options(selectinload(User.permissions),selectinload(User.roles).selectinload(Role.permissions)).filter(User.id == user_id).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return user


def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")
    return user


def has_permission(required_permissions: list[str]):
    def checker(user: User = Depends(get_current_user)):
        user_perms = {p.name for p in user.permissions} | {p.name for role in user.roles for p in role.permissions}

        if not any(req in user_perms for req in required_permissions):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")

        return user

    return checker


def check_role(required_roles: list[str]):
    def checker(user: User = Depends(get_current_user)):
        user_roles = {role.name for role in user.roles}

        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Role check failed")

        return user

    return checker


def get_booking_owner(booking_id: int,user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.user_id != user.id and not user.is_admin:
        raise HTTPException(403, "Access denied")

    return booking


def get_review_owner(review_id: int,user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(404, "Review not found")

    if review.user_id != user.id and not user.is_admin:
        raise HTTPException(403, "Access denied")

    return review