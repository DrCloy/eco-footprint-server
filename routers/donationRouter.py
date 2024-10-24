from core.model import DonationData
from core.repo import DonationRepository
from fastapi import APIRouter


def create_donation_router(repo: DonationRepository):
    router = APIRouter(prefix="/donation", tags=["Donation"])

    @router.get("/")
    def get_all_donations():
        return repo.getAllDonations()

    @router.get("/{donation_id}")
    def get_donation(donationId: int):
        return repo.getDonation(donationId)

    @router.post("/create")
    def create_donation(donation: DonationData):
        return repo.createDonation(donation)

    return router
