from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.product import Product


def create_order(
    db: Session,
    buyer_id: int,
    product_id: int,
    quantity: float
):
    # Check product
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return None, "Product not found"

    # Check availability
    if not product.is_available:
        return None, "Product is not available"

    # Check quantity
    if quantity <= 0:
        return None, "Quantity must be greater than 0"

    if quantity > product.quantity:
        return None, "Not enough product quantity available"

    # Calculate total
    total_amount = product.price * quantity

    # Create order
    order = Order(
        buyer_id=buyer_id,
        product_id=product_id,
        quantity=quantity,
        total_amount=total_amount,
        status="PENDING"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order, None