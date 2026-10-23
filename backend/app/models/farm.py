from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.data_base import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    farmer_id = Column(
        Integer,
        ForeignKey("farmers.id"),
        nullable=False
    )

    farm_name = Column(
        String(150),
        nullable=False
    )

    location = Column(
        String(150),
        nullable=True
    )

    region = Column(
        String(100),
        nullable=True
    )

    district = Column(
        String(100),
        nullable=True
    )

    size = Column(
        Float,
        nullable=True
    )

    size_unit = Column(
        String(20),
        nullable=True
    )

    farmer = relationship(
        "Farmer",
        back_populates="farms"
    )