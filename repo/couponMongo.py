from bson import ObjectId

from fastapi import HTTPException
from pymongo.database import Database

from core.model import CouponItem, CouponItemMeta
from core.repo import CouponRepository


class CouponMongoRepo(CouponRepository):
    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self._collection = db["coupons"]

    def createCoupon(self, couponItem: CouponItem) -> CouponItem:
        if not couponItem.id:
            couponItem.id = str(ObjectId())
        self._collection.insert_one(couponItem.model_dump())

        coupon = self._collection.find_one({"id": couponItem.id})
        if coupon:
            return CouponItem(**coupon)
        else:
            raise HTTPException(status_code=500, detail="Failed to create coupon")

    def getCoupon(self, couponId: str) -> CouponItem:
        coupon = self._collection.find_one({"id": couponId})
        if coupon:
            return CouponItem(**coupon)
        else:
            raise HTTPException(status_code=404, detail="Coupon not found")

    def updateCoupon(self, couponItem: CouponItem) -> CouponItem:
        self._collection.update_one({"id": couponItem.id}, {"$set": couponItem.model_dump()})

        coupon = self._collection.find_one({"id": couponItem.id})
        if couponItem == coupon:
            return CouponItem(**coupon)
        else:
            raise HTTPException(status_code=500, detail="Failed to update coupon")

    def deleteCoupon(self, couponId: str) -> bool:
        result = self._collection.delete_one({"id": couponId})
        return result.deleted_count > 0
