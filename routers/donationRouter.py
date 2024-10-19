from core.model import DonationData
from core.repo import DonationRepository
from fastapi import APIRouter


def create_donation_router(repo: DonationRepository):
    router = APIRouter(prefix="/donation", tags=["Donation"])

    @router.get("/")
    def get_all_donations():
        return repo.get_all_donations()

    @router.get("/{donation_id}")
    def get_donation(donation_id: int):
        return repo.get_donation(donation_id)

    return router
