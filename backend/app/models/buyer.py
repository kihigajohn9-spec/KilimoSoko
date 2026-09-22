from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.data_base import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    business_name = Column(String(150), nullable=True)

    location = Column(String(150), nullable=True)

    region = Column(String(100), nullable=True)

    district = Column(String(100), nullable=True)

    user = relationship("User", backref="buyer")