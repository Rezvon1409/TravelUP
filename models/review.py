from sqlalchemy import Column , String , Integer , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer , primary_key=True , autoincrement=True , index=True)
    user_id = Column(Integer , ForeignKey('users.id') , nullable=False)
    destination_id = Column(Integer, ForeignKey('destinations.id') , nullable=False)
    rating = Column(Integer , nullable= False)
    comment = Column(String , nullable=True)
    created_at = Column(DateTime , default=datetime.utcnow)
    
