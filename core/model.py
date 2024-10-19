from pydantic import BaseModel, Field
from typing import Union, Optional


class UserData(BaseModel):
    id: str
    username: str
    point: int = Field(..., ge=0)
    thumbnailURL: str


class DonationData(BaseModel):
    id: int
    name: str
    amount: int = Field(..., ge=0)
    description: str


class CampainData(BaseModel):
    id: int
    name: str
    description: str
    participants: Union[list[UserData], list[str]]
