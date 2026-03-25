from sqlalchemy.orm import Session
from models.user import User
from models.profile import UserProfile
from core.security import *
from fastapi import HTTPException , status
from core.security import decode_token


async def  register_user(username : str , password : str , db :  Session):
    user = db.query(User).filter(User.username == username).first()
    if user : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Username already exists')
    new_user = User(username=username , pasword_hash = hash_password(password))
    db.asd(new_user)
    db.commit()
    db.refresh(new_user)

    profile = UserProfile(user_id = new_user.id)
    db.add(profile)
    db.commit()

    return new_user


async def login_user(username : str , password : str , db : Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    if not verify_password(password , user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    access_token = create_access_token(data={'sub' : str(user.id)})
    refresh_token = create_refresh_token(data={'sub' : str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }


async def refresh_tokens(refresh_token : str , db : Session):
    payload = decode_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user_id = payload.get('sub')
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    access_token = create_access_token(data={'sub': str(user_id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token, 
        "refresh_token": new_refresh_token, 
        "token_type": "bearer"
    }