from pydantic import BaseModel, Field
from typing import Union, Optional


class UserData(BaseModel):
    id: str
    username: str
    point: int = Field(..., ge=0)
    giftIds: list[str] = []
    DonationIds: list[str] = []
    campainIds: list[str] = []
    thumbnailURL: Optional[str] = None


class DonationData(BaseModel):
    id: str
    name: str
    totalPoint: int = Field(..., ge=0)
    participants: Union[list[UserData], list[str]]
    description: str


class CampainData(BaseModel):
    id: str
    name: str
    description: str
    participants: Union[list[UserData], list[str]]
