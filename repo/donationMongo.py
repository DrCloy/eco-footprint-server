from fastapi import HTTPException

from core.model import UserItemMeta, UserItem, DonationItemMeta, DonationItem
from core.repo import DonationRepository


class DonationMongoRepo(DonationRepository):
    def __init__(self, db):
        super().__init__()
        self._db = db
        self._collection = db["donations"]

    def createDonation(self, donationItem: DonationItem) -> DonationItem:
        self._collection.insert_one(donationItem.model_dump())

        donation = self._collection.find_one({"id": donationItem.id})
        if donation:
            return DonationItem(**donation)
        else:
            raise HTTPException(status_code=500, detail="Failed to create donation")

    def getAllDonations(self) -> list[DonationItemMeta]:
        donations = self._collection.find()
        return [DonationItemMeta(**donation) for donation in donations]

    def getDonation(self, donationId: str) -> DonationItem:
        donation = self._collection.find_one({"id": donationId})
        if donation:
            return DonationItem(**donation)
        else:
            return None

    def updateDonation(self, donationItem: DonationItem) -> DonationItem:
        self._collection.update_one({"id": donationItem.id}, {"$set": donationItem.model_dump()})

        donation = self._collection.find_one({"id": donationItem.id})
        if donationItem == donation:
            return DonationItem(**donation)
        else:
            raise HTTPException(status_code=500, detail="Failed to update donation")

    def deleteDonation(self, donationId: str) -> bool:
        result = self._collection.delete_one({"id": donationId})
        return result.deleted_count > 0
