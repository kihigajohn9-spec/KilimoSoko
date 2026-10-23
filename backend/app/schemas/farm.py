from pydantic import BaseModel


class FarmCreate(BaseModel):
    farm_name: str
    location: str
    region: str
    district: str
    size: float | None = None
    size_unit: str | None = None


class FarmUpdate(BaseModel):
    farm_name: str | None = None
    location: str | None = None
    region: str | None = None
    district: str | None = None
    size: float | None = None
    size_unit: str | None = None


class FarmResponse(BaseModel):
    id: int
    farmer_id: int
    farm_name: str
    location: str
    region: str
    district: str
    size: float | None
    size_unit: str | None

    model_config = {
        "from_attributes": True
    }