from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.data_base import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.order import Order

from app.schemas.order import (
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse
)

from app.services.order_service import create_order


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


# 1. Place Order
@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def place_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only buyers can place orders"
        )

    order, error = create_order(
        db=db,
        buyer_id=current_user.id,
        product_id=order_data.product_id,
        quantity=order_data.quantity
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return order


# 2. My Orders
@router.get(
    "/my-orders",
    response_model=list[OrderResponse]
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).filter(
    Order.buyer_id == current_user.id
).all()


# 3. Get One Order
@router.get(
    "/{id}",
    response_model=OrderResponse
)
def get_order(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if order.buyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this order"
        )

    return order


# 4. Update Order Status
@router.put(
    "/{id}/status",
    response_model=OrderResponse
)
def update_order_status(
    id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if current_user.role != "farmer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only farmers can update order status"
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order