from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ItemState(Enum):
    UNDEFINED = -1
    PENDING = 0
    ACTIVE = 1
    INACTIVE = 2
    FINISHED = 3
    FAILED = 4


class UserItemMeta(BaseModel):
    id: str
    username: str
    thumbnailId: Optional[str] = None


class DonationItemMeta(BaseModel):
    id: Optional[str] = None
    name: str
    currentPoint: int = Field(..., ge=0)
    totalPoint: int = Field(..., ge=0)
    thumbnailId: Optional[str] = None


class CouponItemMeta(BaseModel):
    id: Optional[str] = None
    itemName: str
    brandName: str
    thumbnailId: Optional[str] = None
    expiredAt: str


class ChallengeItemMeta(BaseModel):
    id: Optional[str] = None
    name: str
    totalParticipants: int = Field(..., ge=0)
    currentParticipants: int
    dateEnd: str


class ChallengeRecordItem(BaseModel):
    userId: str
    imageId: str
    date: str
    approved: bool = False


class RewardItemMeta(BaseModel):
    id: str
    itemName: str
    brandName: str
    itemType: str
    point: int = Field(..., ge=0)
    thumbnailId: str


class UserItem(UserItemMeta):
    id: str
    username: str
    point: int = Field(..., ge=0)
    couponList: list[CouponItemMeta] = []
    challengeList: list[ChallengeItemMeta] = []
    thumbnailId: str = ''


class DonationItem(DonationItemMeta):
    id: str
    name: str
    currentPoint: int = Field(..., ge=0)
    totalPoint: int = Field(..., ge=0)
    description: str
    participants: list[str] = []
    thumbnailId: Optional[str] = None
    state: ItemState = ItemState.UNDEFINED


class CouponItem(CouponItemMeta):
    id: str
    itemName: str
    brandName: str
    description: str
    thumbnailId: Optional[str] = None
    couponId: str
    expiredAt: str


class ChallengeItem(ChallengeItemMeta):
    id: str
    name: str
    totalParticipants: int = Field(..., ge=0)
    currentParticipants: int
    createdAt: str
    participants: list[UserItemMeta] = []
    participantRecords: list[ChallengeRecordItem] = []
    dateStart: str
    dateEnd: str
    description: str
    state: ItemState = ItemState.UNDEFINED


class RewardItem(RewardItemMeta):
    id: str
    owner: str
    itemName: str
    brandName: str
    itemType: str
    description: str
    imageId: str
    thumbnailId: str
    price: int = Field(..., ge=0)
    provider: str


class FileData(BaseModel):
    id: str
    owner: str
    name: str
    size: int
    contentType: str
    file: bytes
    isPrivate: bool = False
