from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category: str
    price: float
    quantity: float
    unit: str
    location: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    quantity: float | None = None
    unit: str | None = None
    location: str | None = None
    is_available: bool | None = None


class ProductResponse(BaseModel):
    id: int
    farmer_id: int
    name: str
    description: str | None
    category: str
    price: float
    quantity: float
    unit: str
    location: str | None
    is_available: bool

    model_config = {
        "from_attributes": True
    }