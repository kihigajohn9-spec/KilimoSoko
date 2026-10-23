from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.models.farmer import Farmer
from app.models.user import User
from app.schemas.farm import FarmCreate, FarmUpdate


def get_farmer(
    db: Session,
    user: User
):
    if not (
        farmer := db.query(Farmer).filter(
            Farmer.user_id == user.id
        ).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer profile not found"
        )

    return farmer


def create_farm(
    db: Session,
    user: User,
    farm_data: FarmCreate
):
    farmer = get_farmer(db, user)

    farm = Farm(
        farmer_id=farmer.id,
        farm_name=farm_data.farm_name,
        location=farm_data.location,
        region=farm_data.region,
        district=farm_data.district,
        size=farm_data.size,
        size_unit=farm_data.size_unit
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


def get_my_farms(
    db: Session,
    user: User
):
    farmer = get_farmer(db, user)

    return db.query(Farm).filter(
        Farm.farmer_id == farmer.id
    ).all()


def get_farm(
    db: Session,
    user: User,
    farm_id: int
):
    farmer = get_farmer(db, user)

    if not (
        farm := db.query(Farm).filter(
            Farm.id == farm_id,
            Farm.farmer_id == farmer.id
        ).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found"
        )

    return farm


def update_farm(
    db: Session,
    user: User,
    farm_id: int,
    farm_data: FarmUpdate
):
    farm = get_farm(
        db=db,
        user=user,
        farm_id=farm_id
    )

    update_data = farm_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(farm, field, value)

    db.commit()
    db.refresh(farm)

    return farm


def delete_farm(
    db: Session,
    user: User,
    farm_id: int
):
    farm = get_farm(
        db=db,
        user=user,
        farm_id=farm_id
    )

    db.delete(farm)
    db.commit()

    return {
        "message": "Farm deleted successfully"
    }