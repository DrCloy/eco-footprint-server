import os
import random
import datetime

from fastapi import APIRouter, HTTPException, Request

from core.model import RewardItem, RewardItemMeta, CouponItem, CouponItemMeta, FileData
from core.repo import UserRepository, RewardRepository, CouponRepository, FileRepository

coupon_bugger = [
    '6739d85dccd5dff0b84a1652', '6739da95530613b298315b84', '6739daab530613b298315b86', '6739dab7530613b298315b88',
    '6739dac6530613b298315b8a', '6739dad9530613b298315b8c', '6739dae6530613b298315b8e', '6739daef530613b298315b90',
    '6739daf6530613b298315b92', '6739dafe530613b298315b94']
coupon_chicken = [
    '6739db1394d7281d17ff9848', '6739db1994d7281d17ff984a', '6739db3894d7281d17ff984c', '6739db3d94d7281d17ff984e',
    '6739db4494d7281d17ff9850', '6739db4a94d7281d17ff9852', '6739db5094d7281d17ff9854', '6739db5494d7281d17ff9856',
    '6739db5c94d7281d17ff9858', '6739db6794d7281d17ff985a']
coupon_coffee = [
    '6739db7894d7281d17ff985c', '6739db8494d7281d17ff9860', '6739dc0894d7281d17ff9862', '6739dc1394d7281d17ff9864',
    '6739dc1b94d7281d17ff9866', '6739dc2094d7281d17ff9868', '6739dc2794d7281d17ff986a', '6739dc2f94d7281d17ff986c',
    '6739dc3894d7281d17ff986e', '6739dc3e94d7281d17ff9870']


class RewardRouter(APIRouter):
    def __init__(self, userRepo: UserRepository, rewardRepo: RewardRepository, couponRepo: CouponRepository, fileRepo: FileRepository):
        super().__init__(prefix="/reward")
        self._userRepo = userRepo
        self._rewardRepo = rewardRepo
        self._couponRepo = couponRepo
        self._fileRepo = fileRepo

    def createReward(self, rewardItem: RewardItem, request: Request) -> RewardItem:
        if os.getenv("ENV_MODE") == "test":
            pass
        else:
            if not os.getenv("ADMIN_USER") == request.state.auth.get("sub"):
                raise HTTPException(status_code=403, detail="Forbidden")

        reward = self._rewardRepo.createReward(rewardItem)
        return reward

    def getAllRewards(self) -> list[RewardItemMeta]:
        return self._rewardRepo.getAllRewards()

    def getReward(self, rewardId: str) -> RewardItem:
        return self._rewardRepo.getReward(rewardId)

    def updateReward(self, rewardItem: RewardItem, request: Request) -> RewardItem:
        if os.getenv("ENV_MODE") == "test":
            pass
        else:
            if not os.getenv("ADMIN_USER") == request.state.auth.get("sub"):
                raise HTTPException(status_code=403, detail="Forbidden")

        reward = self._rewardRepo.updateReward(rewardItem)
        return reward

    def deleteReward(self, rewardId: str, request: Request) -> bool:
        if os.getenv("ENV_MODE") == "test":
            pass
        else:
            if not os.getenv("ADMIN_USER") == request.state.auth.get("sub"):
                raise HTTPException(status_code=403, detail="Forbidden")

        return self._rewardRepo.deleteReward(rewardId)

    def purchaseReward(self, rewardId: str, request: Request) -> CouponItem:
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(request.state.auth.get("sub"))
        reward = self._rewardRepo.getReward(rewardId)
        if user.point < reward.point:
            raise HTTPException(status_code=400, detail="Not enough point")
        user.point -= reward.point

        # TODO: 기프티콘 API를 호출하여 기프티콘을 발급, 기프티콘 이미지를 저장

        # TODO: 기프티콘 API를 사용하는 기눙 추가 이후, 아래 코드와 위의 쿠폰 ID 삭제
        if reward.itemType == '햄버거':
            couponId = random.choice(coupon_bugger)
        elif reward.itemType == '치킨':
            couponId = random.choice(coupon_chicken)
        elif reward.itemType == '커피':
            couponId = random.choice(coupon_coffee)

        coupon = CouponItem(
            itemName=reward.itemName,
            brandName=reward.brandName,
            description=reward.description,
            thumbnailId=couponId,
            couponId=couponId,
            expiredAt=str(int((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()))
        )
        coupon = self._couponRepo.createCoupon(coupon)
        user.couponList.append(CouponItemMeta(**coupon))

        user = self._userRepo.updateUser(user)

        return coupon

    def extendExpiration(self, couponId: str, request: Request) -> CouponItem:
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(request.state.auth.get("sub"))

        if not next((coupon for coupon in user.couponList if coupon.couponId == couponId), None):
            raise HTTPException(status_code=400, detail="Coupon not found")
        coupon = self._couponRepo.getCoupon(couponId)
        coupon.expiredAt = str(int((datetime.datetime.fromtimestamp(int(coupon.expiredAt)) + datetime.timedelta(days=7)).timestamp()))
        coupon = self._couponRepo.updateCoupon(coupon)

        return coupon

    def deleteCoupon(self, couponId: str, request: Request) -> bool:
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(request.state.auth.get("sub"))

        if not next((coupon for coupon in user.couponList if coupon.couponId == couponId), None):
            raise HTTPException(status_code=400, detail="Coupon not found")

        return self._couponRepo.deleteCoupon(couponId)
