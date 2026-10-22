from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.data_base import get_db
from app.core.security import require_role
from app.models.user import User
from app.schemas.farmers import FarmerCreate, FarmerResponse
from app.services.farmer_service import create_farmer_profile


router = APIRouter(
    prefix="/api/farmers",
    tags=["Farmers"]
)


@router.post(
    "/profile",
    response_model=FarmerResponse
)
def create_profile(
    farmer_data: FarmerCreate,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return create_farmer_profile(
        db=db,
        user=current_user,
        farmer_data=farmer_data
    )