from sqlalchemy import Column , Integer , String , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class UserProfile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer , primary_key=True , autoincrement=True , index= True)
    user_id = Column(Integer , ForeignKey('users.id') , nullable=False)
    theme = Column(String , default='system')
    created_at = Column(DateTime, default=datetime.utcnow)


    user = relationship("User", back_populates="profile")