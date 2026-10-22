from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.farmer import Farmer
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(
    db: Session,
    user: User,
    product_data: ProductCreate
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

    product = Product(
        farmer_id=farmer.id,
        name=product_data.name,
        description=product_data.description,
        category=product_data.category,
        price=product_data.price,
        quantity=product_data.quantity,
        unit=product_data.unit,
        location=product_data.location
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_all_products(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    location: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    available_only: bool = True
):
    query = db.query(Product)

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    if category:
        query = query.filter(
            Product.category.ilike(f"%{category}%")
        )

    if location:
        query = query.filter(
            Product.location.ilike(f"%{location}%")
        )

    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    if available_only:
        query = query.filter(
            Product.is_available.is_(True)
        )

    return query.all()

def get_product(
    db: Session,
    product_id: int
):
    if not (
        product := db.query(Product).filter(
            Product.id == product_id
        ).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product

def update_product(
    db: Session,
    user: User,
    product_id: int,
    product_data: ProductUpdate
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

    if not (
        product := db.query(Product).filter(
            Product.id == product_id,
            Product.farmer_id == farmer.id
        ).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or does not belong to you"
        )

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

def delete_product(
    db: Session,
    user: User,
    product_id: int
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

    if not (
        product := db.query(Product).filter(
            Product.id == product_id,
            Product.farmer_id == farmer.id
        ).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or does not belong to you"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }