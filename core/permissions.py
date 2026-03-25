from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, selectinload
from database import get_db
from core.security import decode_token
from models.user import User, Role
from models.booking import Booking
from models.review import Review

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    user = db.query(User).options(selectinload(User.permissions),selectinload(User.roles).selectinload(Role.permissions)).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return user




def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")
    return user



def has_permission(required_permissions: list[str]):
    def checker(user: User = Depends(get_current_user)):
        user_perms = {p.name for p in user.permissions}
        for role in user.roles:
            for p in role.permissions:
                user_perms.add(p.name)

        for req in required_permissions:
            if req not in user_perms:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")
        return user
    return checker




def check_role(required_roles: list[str]):
    def checker(user: User = Depends(get_current_user)):
        user_roles = {role.name for role in user.roles}
        for req in required_roles:
            if req not in user_roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Role check failed")
        return user
    return checker




def get_booking_owner(booking_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return booking


def get_review_owner(review_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    if review.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return review