from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.data_base import get_db
from app.core.security import require_role
from app.models.user import User

from app.schemas.farm import (
    FarmCreate,
    FarmUpdate,
    FarmResponse
)

from app.services.farm_service import (
    create_farm,
    get_my_farms,
    get_farm,
    update_farm,
    delete_farm
)


router = APIRouter(
    prefix="/api/farms",
    tags=["Farms"]
)


@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    farm_data: FarmCreate,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return create_farm(
        db=db,
        user=current_user,
        farm_data=farm_data
    )


@router.get(
    "/my-farms",
    response_model=list[FarmResponse]
)
def get_mine(
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return get_my_farms(
        db=db,
        user=current_user
    )


@router.get(
    "/{farm_id}",
    response_model=FarmResponse
)
def get_one(
    farm_id: int,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return get_farm(
        db=db,
        user=current_user,
        farm_id=farm_id
    )


@router.put(
    "/{farm_id}",
    response_model=FarmResponse
)
def update(
    farm_id: int,
    farm_data: FarmUpdate,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return update_farm(
        db=db,
        user=current_user,
        farm_id=farm_id,
        farm_data=farm_data
    )


@router.delete("/{farm_id}")
def delete(
    farm_id: int,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return delete_farm(
        db=db,
        user=current_user,
        farm_id=farm_id
    )