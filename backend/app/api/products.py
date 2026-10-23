from fastapi import APIRouter, Depends, status,Query,status
from sqlalchemy.orm import Session

from app.core.data_base import get_db
from app.core.security import require_role
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.services.product_service import (
    create_product,
    get_all_products,
    get_product,
    update_product,
    delete_product
)


router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    product_data: ProductCreate,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return create_product(
        db=db,
        user=current_user,
        product_data=product_data
    )


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_all(
    search: str | None = Query(
        default=None,
        description="Search product by name"
    ),
    category: str | None = Query(
        default=None,
        description="Filter by category"
    ),
    location: str | None = Query(
        default=None,
        description="Filter by location"
    ),
    min_price: float | None = Query(
        default=None,
        ge=0,
        description="Minimum product price"
    ),
    max_price: float | None = Query(
        default=None,
        ge=0,
        description="Maximum product price"
    ),
    available_only: bool = Query(
        default=True,
        description="Show only available products"
    ),
    db: Session = Depends(get_db)
):
    return get_all_products(
        db=db,
        search=search,
        category=category,
        location=location,
        min_price=min_price,
        max_price=max_price,
        available_only=available_only
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_one(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product(
        db=db,
        product_id=product_id
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return update_product(
        db=db,
        user=current_user,
        product_id=product_id,
        product_data=product_data
    )


@router.delete(
    "/{product_id}"
)
def delete(
    product_id: int,
    current_user: User = Depends(
        require_role("farmer")
    ),
    db: Session = Depends(get_db)
):
    return delete_product(
        db=db,
        user=current_user,
        product_id=product_id
    )