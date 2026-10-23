from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.models.user import User
from app.schemas.farmers import FarmerCreate


def create_farmer_profile(
    db: Session,
    user: User,
    farmer_data: FarmerCreate
):
    if existing_farmer := db.query(Farmer).filter(
        Farmer.user_id == user.id
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farmer profile already exists"
        )

    farmer = Farmer(
        user_id=user.id,
        farm_name=farmer_data.farm_name,
        location=farmer_data.location,
        region=farmer_data.region,
        district=farmer_data.district
    )

    db.add(farmer)
    db.commit()
    db.refresh(farmer)

    return farmer