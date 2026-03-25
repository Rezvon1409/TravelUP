from sqlalchemy import Column , Float , String , DateTime , Integer
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer , primary_key=True , autoincrement=True , index=True)
    title = Column(String , nullable=False)
    description = Column(String , nullable=False)
    country = Column(String , nullable=False)
    city = Column(String , nullable=False)
    cover_image = Column(String , nullable=False)
    rating = Column(Float , default=0.0)
    created_at = Column(DateTime , default=datetime.utcnow)

    