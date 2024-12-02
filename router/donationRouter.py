from fastapi import APIRouter, Request, HTTPException

from core.model import UserItem, DonationItem, DonationItemMeta
from core.repo import UserRepository, DonationRepository


class DonationRouter(APIRouter):
    """
    DonationRouter class

    This class is a router class for donation-related API endpoints.
    """

    def __init__(self, userRepo: UserRepository, donationRepo: DonationRepository):
        super().__init__(prefix="/donation")
        self._userRepo = userRepo
        self._donationRepo = donationRepo

        self.add_api_route(path="/create", endpoint=self._createDonation, methods=["POST"])
        self.add_api_route(path="/all", endpoint=self._getAllDonations, methods=["GET"])
        self.add_api_route(path="/{donationId}", endpoint=self._getDonation, methods=["GET"])
        self.add_api_route(path="/{donationId}/update", endpoint=self._updateDonation, methods=["PUT"])
        self.add_api_route(path="/{donationId}/participate/{userId}", endpoint=self._participateDonation, methods=["POST"])
        self.add_api_route(path="/{donationId}/delete", endpoint=self._deleteDonation, methods=["DELETE"])

    def _createDonation(self, donationItem: DonationItem, request: Request) -> DonationItem:
        """
        Create a new donation

        Args:
            donationItem (DonationItem): The donationItem to create
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found

        Returns:
            DonationItem: The created donationItem
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth["sub"]
        # TODO: Check if the user is admin

        donationItem.id = self._donationRepo.createDonation(donationItem)
        return donationItem

    def _getAllDonations(self):
        """
        Get all donations

        Returns:
            list[DonationItem]: The list of all donations
        """
        return self._donationRepo.getAllDonations()

    def _getDonation(self, donationId: str):
        """
        Get the donation with donationId

        Args:
            donationId (str): The donationId to get the donation

        Raises:
            HTTPException(status_code=404): If the donation is not found

        Returns:
            DonationItem: The donation
        """
        donation = self._donationRepo.getDonation(donationId)
        if donation is None:
            raise HTTPException(status_code=404, detail="Donation not found")

        return donation

    def _updateDonation(self, donationId: str, donationItem: DonationItem, request: Request) -> DonationItem:
        """
        Update the donation with donationId

        Args:
            donationId (str): The donationId to update
            donationItem (DonationItem): The donationItem to update
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the donation is not found

        Returns:
            DonationItem: The updated donation
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth["sub"]
        # TODO: Check if the user is admin

        donation = self._donationRepo.getDonation(donationId)
        if donation is None:
            raise HTTPException(status_code=404, detail="Donation not found")

        donationItem.id = donationId
        self._donationRepo.updateDonation(donationItem)
        return donationItem

    def _participateDonation(self, userId: str, donationId: str, request: Request) -> DonationItem:
        """
        Participate in the donation with donationId

        Args:
            userId (str): The userId to participate in the donation
            donationId (str): The donationId to participate
            request (Request): The request object
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(userId)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        donation = self._donationRepo.getDonation(donationId)
        if donation is None:
            raise HTTPException(status_code=404, detail="Donation not found")

        if userId in donation.participants:
            raise HTTPException(status_code=400, detail="Already participated in the donation")

        # TODO: Check if the user has already watched an ad
        # TODO: If the user has watched an ad, add points to the donation and the user

        donation.participants.append(userId)
        donation = self._donationRepo.updateDonation(donation)
        return donation

    def _deleteDonation(self, donationId: str, request: Request):
        """
        Delete the donation with donationId

        Args:
            donationId (str): The donationId to delete
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the donation is not found

        Returns:
            bool: True if the deletion is successful, False otherwise
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth["sub"]
        # TODO: Check if the user is admin

        donation = self._donationRepo.getDonation(donationId)
        if donation is None:
            raise HTTPException(status_code=404, detail="Donation not found")

        return self._donationRepo.deleteDonation(donationId)
