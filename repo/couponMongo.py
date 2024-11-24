from bson import ObjectId

from fastapi import HTTPException
from pymongo.database import Database

from core.model import CouponItem, CouponItemMeta
from core.repo import CouponRepository


class CouponMongoRepo(CouponRepository):
    """
    Implementation of CouponRepository using MongoDB
    """

    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self._collection = db["coupons"]

    def createCoupon(self, couponItem: CouponItem) -> CouponItem:
        """
        Create a new coupon item

        Args:
            couponItem (CouponItem): Coupon item to be created

        Raises:
            HTTPException: Failed to create coupon

        Returns:
            CouponItem: Created coupon item
        """
        if not couponItem.id:
            couponItem.id = str(ObjectId())
        self._collection.insert_one(couponItem.model_dump())

        coupon = self._collection.find_one({"id": couponItem.id})
        if coupon:
            return CouponItem(**coupon)
        else:
            raise HTTPException(status_code=500, detail="Failed to create coupon")

    def getCoupon(self, couponId: str) -> CouponItem:
        """
        Get a coupon item by id

        Args:
            couponId (str): Coupon id

        Returns:
            CouponItem: Coupon item
        """
        coupon = self._collection.find_one({"id": couponId})
        if coupon:
            return CouponItem(**coupon)
        else:
            return None

    def updateCoupon(self, couponItem: CouponItem) -> CouponItem:
        """
        Update a coupon item

        Args:
            couponItem (CouponItem): Coupon item to be updated

        Raises:
            HTTPException: Failed to update coupon

        Returns:
            CouponItem: Updated coupon item
        """
        self._collection.update_one({"id": couponItem.id}, {"$set": couponItem.model_dump()})

        coupon = self._collection.find_one({"id": couponItem.id})
        if couponItem == coupon:
            return CouponItem(**coupon)
        else:
            raise HTTPException(status_code=500, detail="Failed to update coupon")

    def deleteCoupon(self, couponId: str) -> bool:
        """
        Delete a coupon item by id

        Args:
            couponId (str): Coupon id

        Returns:
            bool: True if coupon is deleted, False otherwise
        """
        result = self._collection.delete_one({"id": couponId})
        return result.deleted_count > 0
