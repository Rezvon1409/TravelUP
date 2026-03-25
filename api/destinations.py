from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from core.permissions import get_admin_user
from models.destination import Destination
from models.user import User
from schemas.destination import DestinationSchema, DestinationCreateSchema
from typing import List

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("", response_model=List[DestinationSchema])
async def get_destinations(db: Session = Depends(get_db)):
    return db.query(Destination).all()


@router.get("/{id}", response_model=DestinationSchema)
async def get_destination(id: int, db: Session = Depends(get_db)):
    destination = db.query(Destination).filter(Destination.id == id).first()
    if not destination:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    return destination


@router.post("", response_model=DestinationSchema)
async def create_destination(data: DestinationCreateSchema, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    new_destination = Destination(**data.model_dump())
    db.add(new_destination)
    db.commit()
    db.refresh(new_destination)
    return new_destination


@router.put("/{id}", response_model=DestinationSchema)
async def update_destination(id: int, data: DestinationCreateSchema, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    destination = db.query(Destination).filter(Destination.id == id).first()
    if not destination:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    for key, value in data.model_dump().items():
        setattr(destination, key, value)
    db.commit()
    db.refresh(destination)
    return destination


@router.delete("/{id}")
async def delete_destination(id: int, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    destination = db.query(Destination).filter(Destination.id == id).first()
    if not destination:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
    db.delete(destination)
    db.commit()
    return {"msg": "Destination deleted"}