from sqlalchemy import Column , Integer , String , ForeignKey , DateTime , Date , Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer , primary_key=True , autoincrement=True , index=True)
    user_id = Column(Integer , ForeignKey('users.id'), nullable=False)
    destination_id = Column(Integer , ForeignKey('destinations.id'), nullable=False)
    start_date = Column(Date , nullable=False)
    end_date = Column(Date , nullable=False)
    travelers_count = Column(Integer , nullable=False)
    total_price = Column(Float , nullable=False)
    status = Column(String , default='pending')
    created_at = Column(DateTime , default=datetime.utcnow)
    