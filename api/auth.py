from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth import *
from services.auth import *

router =APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register(data: RegisterSchema, db: Session = Depends(get_db)):
    result = await register_user(data.username, data.password, db)
    return result

@router.post('/login', response_model=TokenSchema)
async def login(data : LoginSchema , db : Session = Depends(get_db)):
    return await login_user(data.username , data.passwrod , db)

@router.post('/refresh' , response_model=TokenSchema)
async def refresh(data : RefreshSchema , db : Session = Depends(get_db)):
    return await refresh_tokens(data.refresh_token , db)


@router.post("/logout")
async def logout():
    return {"msg": "Logged out"}