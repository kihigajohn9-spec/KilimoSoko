from pydantic import BaseModel


class FarmerCreate(BaseModel):
    farm_name: str | None = None
    location: str | None = None
    region: str | None = None
    district: str | None = None


class FarmerResponse(BaseModel):
    id: int
    user_id: int
    farm_name: str | None
    location: str | None
    region: str | None
    district: str | None

    model_config = {
        "from_attributes": True
    }
    