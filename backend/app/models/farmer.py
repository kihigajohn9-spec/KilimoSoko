from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.data_base import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    user = relationship(
        "User",
        backref="farmer"
    )
    
    farms = relationship(
        "Farm", 
        back_populates="farmer",
        cascade="all, delete-orphan"
    )
