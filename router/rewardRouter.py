from fastapi import APIRouter, HTTPException, Request

from core.model import UserItem, UserItemMeta, RewardItem, RewardItemMeta, CouponItem, CouponItemMeta, FileData
from core.repo import UserRepository, RewardRepository, CouponRepository, FileRepository


class RewardRouter(APIRouter):
    def __init__(self, userRepo: UserRepository, rewardRepo: RewardRepository, couponRepo: CouponRepository, fileRepo: FileRepository):
        super().__init__(prefix="/reward")
        self._userRepo = userRepo
        self._rewardRepo = rewardRepo
        self._couponRepo = couponRepo
        self._fileRepo = fileRepo

    def createReward(self, rewardItem: RewardItem, request: Request) -> RewardItem:
        pass

    def getAllRewards(self) -> list[RewardItemMeta]:
        pass

    def getReward(self, rewardId: str) -> RewardItem:
        pass

    def updateReward(self, rewardItem: RewardItem) -> RewardItem:
        pass

    def deleteReward(self, rewardId: str) -> bool:
        pass

    def createCoupon(self, couponItem: CouponItem, request: Request) -> CouponItem:
        pass

    def extendExpiration(self, couponId: str, request: Request) -> CouponItem:
        pass

    def deleteCoupon(self, couponId: str) -> bool:
        pass
