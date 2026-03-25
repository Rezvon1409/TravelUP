from sqlalchemy import Column , Integer , String , Boolean , ForeignKey , DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer , primary_key=True , autoincrement=True , index=True)
    username = Column(String , unique=True , nullable=False)
    password_hash = Column(String , nullable=False)
    is_admin = Column(Boolean , default=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime , default=datetime.utcnow)


    profile = relationship("UserProfile", back_populates="user", uselist=False)
    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")