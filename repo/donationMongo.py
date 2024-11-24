from fastapi import HTTPException

from core.model import DonationItemMeta, DonationItem
from core.repo import DonationRepository


class DonationMongoRepo(DonationRepository):
    """
    Implementation of DonationRepository using MongoDB
    """

    def __init__(self, db):
        super().__init__()
        self._db = db
        self._collection = db["donations"]

    def createDonation(self, donationItem: DonationItem) -> DonationItem:
        """
        Create a new donation item

        Args:
            donationItem (DonationItem): The donation item to create

        Raises:
            HTTPException: If the donation item cannot be created

        Returns:
            DonationItem: The created donation item
        """
        self._collection.insert_one(donationItem.model_dump())

        donation = self._collection.find_one({"id": donationItem.id})
        if donation:
            return DonationItem(**donation)
        else:
            raise HTTPException(status_code=500, detail="Failed to create donation")

    def getAllDonations(self) -> list[DonationItemMeta]:
        """
        Get all donation items

        Returns:
            list[DonationItemMeta]: A list of donation items
        """
        donations = self._collection.find()
        return [DonationItemMeta(**donation) for donation in donations]

    def getDonation(self, donationId: str) -> DonationItem:
        """
        Get a donation item by ID

        Args:
            donationId (str): The ID of the donation item to get

        Returns:
            DonationItem: The donation item if found, None otherwise
        """
        donation = self._collection.find_one({"id": donationId})
        if donation:
            return DonationItem(**donation)
        else:
            return None

    def updateDonation(self, donationItem: DonationItem) -> DonationItem:
        """
        Update a donation item

        Args:
            donationItem (DonationItem): The donation item to update

        Raises:
            HTTPException: If the donation item cannot be updated

        Returns:
            DonationItem: The updated donation item
        """
        self._collection.update_one({"id": donationItem.id}, {"$set": donationItem.model_dump()})

        donation = self._collection.find_one({"id": donationItem.id})
        if donationItem == donation:
            return DonationItem(**donation)
        else:
            raise HTTPException(status_code=500, detail="Failed to update donation")

    def deleteDonation(self, donationId: str) -> bool:
        """
        Delete a donation item by ID

        Args:
            donationId (str): The ID of the donation item to delete

        Returns:
            bool: True if the donation item was deleted, False otherwise
        """
        result = self._collection.delete_one({"id": donationId})
        return result.deleted_count > 0
