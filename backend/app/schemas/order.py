from pydantic import BaseModel
from typing import Literal


class OrderCreate(BaseModel):
    product_id: int
    quantity: float


class OrderStatusUpdate(BaseModel):
    status: Literal[
        "PENDING",
        "ACCEPTED",
        "REJECTED",
        "COMPLETED",
        "CANCELLED"
    ]


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    product_id: int
    quantity: float
    total_amount: float
    status: str

    class Config:
        from_attributes = True