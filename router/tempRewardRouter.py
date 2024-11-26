import os
import io
import base64
import random
import datetime

from fastapi import APIRouter, HTTPException, Request, UploadFile

from core.model import RewardItem, RewardItemMeta, CouponItem, CouponItemMeta, FileData
from core.repo import UserRepository, RewardRepository, CouponRepository, FileRepository

coupon_bugger = ['6744a8355885bfc26714aa32', '6744a861d3331dac07b19577', '6744a86cd3331dac07b19579',
                 '6744a86cd3331dac07b19579', '6744a881d3331dac07b1957d', '6744a889d3331dac07b1957f', '6744a891d3331dac07b19581']
coupon_chicken = ['6744a89c7f333de2df997e7b', '6744a8a47f333de2df997e7d']
coupon_coffee = ['6744a8ad7f333de2df997e7f', '6744a8b57f333de2df997e81', '6744a8bd7f333de2df997e83']


class RewardRouter(APIRouter):
    """
    Reward Router Class

    This class is a router class for reward-related API endpoints.
    This class will be exchanged when gift coupon API is available.
    """

    def __init__(self, userRepo: UserRepository, rewardRepo: RewardRepository, couponRepo: CouponRepository, fileRepo: FileRepository):
        super().__init__(prefix="/reward")
        self._userRepo = userRepo
        self._rewardRepo = rewardRepo
        self._couponRepo = couponRepo
        self._fileRepo = fileRepo

        self.add_api_route(methods=["POST"], path="/create", endpoint=self._createReward)
        self.add_api_route(methods=["GET"], path="/all", endpoint=self._getAllRewards)
        self.add_api_route(methods=["GET"], path="/{rewardId}", endpoint=self.getReward)
        self.add_api_route(methods=["PUT"], path="/update", endpoint=self.updateReward)
        self.add_api_route(methods=["DELETE"], path="/delete/{rewardId}", endpoint=self.deleteReward)
        self.add_api_route(methods=["POST"], path="/purchase/{rewardId}", endpoint=self.purchaseReward)
        self.add_api_route(methods=["POST"], path="/extend/{couponId}", endpoint=self.extendExpiration)
        self.add_api_route(methods=["DELETE"], path="/delete/{couponId}", endpoint=self.deleteCoupon)

    def _createReward(self, rewardItem: RewardItem, request: Request) -> RewardItem:
        """
        Create a new reward item

        Args:
            rewardItem (RewardItem): The rewardItem to create
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authorized

        Returns:
            RewardItem: The created rewardItem
        """
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        # TODO: Check if the user is an admin

        reward = self._rewardRepo.createReward(rewardItem)
        return reward

    def _getAllRewards(self) -> list[RewardItemMeta]:
        """
        Get all rewards

        Returns:
            list[RewardItemMeta]: A list of RewardItemMeta
        """
        return self._rewardRepo.getAllRewards()

    def getReward(self, rewardId: str) -> RewardItem:
        """
        Get a reward data by rewardId

        Args:
            rewardId (str): The rewardId to get

        Returns:
            RewardItem: The rewardItem
        """
        return self._rewardRepo.getReward(rewardId)

    def updateReward(self, rewardItem: RewardItem, request: Request) -> RewardItem:
        """
        Update a reward item

        Args:
            rewardItem (RewardItem): The rewardItem to update
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authorized
            HTTPException(status_code=403): If the user is not an admin

        Returns:
            RewardItem: The updated rewardItem
        """
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        # TODO: Check if the user is an admin

        reward = self._rewardRepo.updateReward(rewardItem)
        return reward

    def deleteReward(self, rewardId: str, request: Request) -> bool:
        """
        Delete a reward item

        Args:
            rewardId (str): The rewardId to delete
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authorized
            HTTPException(status_code=403): If the user is not an admin

        Returns:
            bool: True if the reward is deleted, False otherwise"""
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        # TODO: Check if the user is an admin

        return self._rewardRepo.deleteReward(rewardId)

    def purchaseReward(self, rewardId: str, request: Request) -> CouponItem:
        """
        Purchase a reward item and add it to the user's coupon list

        Args:
            rewardId (str): The rewardId to purchase
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If the user does not have enough points
            HTTPException(status_code=401): If the user is not authorized

        Returns:
            CouponItem: The purchased coupon item
        """
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        if not self._userRepo.getUser(userId):
            raise HTTPException(status_code=404, detail="User not found")

        user = self._userRepo.getUser(userId)

        reward = self._rewardRepo.getReward(rewardId)
        if user.point < reward.price:
            raise HTTPException(status_code=400, detail="Not enough point")

        if reward.itemType == '햄버거':
            couponId = random.choice(coupon_bugger)
        elif reward.itemType == '치킨':
            couponId = random.choice(coupon_chicken)
        elif reward.itemType == '커피':
            couponId = random.choice(coupon_coffee)
        try:
            couponImage = self._fileRepo.getFile(couponId)
            imageFile = io.BytesIO(base64.b64decode(couponImage.file))
            newCouponImage = self._fileRepo.createFile(
                file=UploadFile(
                    file=imageFile,
                    size=couponImage.size,
                    filename=couponImage.name,
                    content_type=couponImage.contentType
                ),
                userId=userId,
                isPrivate=True)

            coupon = CouponItem(
                itemName=reward.itemName,
                brandName=reward.brandName,
                description=reward.description,
                thumbnailId=couponId,
                couponId=newCouponImage.id,
                expiredAt=str(int((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()))
            )
            coupon = self._couponRepo.createCoupon(coupon)

            user.couponList.append(CouponItemMeta(**coupon))
            user.point -= reward.price
            user = self._userRepo.updateUser(user)

            return coupon
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to purchase reward, " + str(e))

    def extendExpiration(self, couponId: str, request: Request) -> CouponItem:
        """
        Extend coupon expriation date

        Args:
            couponId (str): The couponId to extend expiration
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If the coupon is not found
            HTTPException(status_code=401): If the user is not authorized
            HTTPException(status_code=404): If the user is not found

        Returns:
            CouponItem: The extended coupon item
        """
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth.get("sub")

        user = self._userRepo.getUser(userId)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not next((coupon for coupon in user.couponList if coupon.couponId == couponId), None):
            raise HTTPException(status_code=400, detail="Coupon not found")

        coupon = self._couponRepo.getCoupon(couponId)
        coupon.expiredAt = str(int((datetime.datetime.fromtimestamp(int(coupon.expiredAt)) + datetime.timedelta(days=7)).timestamp()))
        coupon = self._couponRepo.updateCoupon(coupon)

        return coupon

    def deleteCoupon(self, couponId: str, request: Request) -> bool:
        """
        Delete a coupon item

        Args:
            couponId (str): The couponId to delete
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If the coupon is not found
            HTTPException(status_code=401): If the user is not authorized
            HTTPException(status_code=404): If the user is not found

        Returns:
            bool: True if the coupon is deleted, False otherwise
        """
        if not request.state.auth:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        user = self._userRepo.getUser(userId)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not next((coupon for coupon in user.couponList if coupon.couponId == couponId), None):
            raise HTTPException(status_code=400, detail="Coupon not found")

        return self._couponRepo.deleteCoupon(couponId)
