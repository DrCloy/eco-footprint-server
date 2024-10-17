from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: str
    username: str
    point: int = Field(..., ge=0)
    thumbnailURL: str


class DonationData(BaseModel):
    id: str
    name: str
    amount: int = Field(..., ge=0)
    description: str


class CampainData(BaseModel):
    id: str
    name: str
    description: str
