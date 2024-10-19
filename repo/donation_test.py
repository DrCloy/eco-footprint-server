from fastapi import HTTPException

from core.model import DonationData
from core.repo import DonationRepository


class Donation1(DonationData):
    id: int = 1
    name: str = "donation1"
    amount: int = 100
    description: str = "Thank you for your donation"


class Donation2(DonationData):
    id: int = 2
    name: str = "donation2"
    amount: int = 200
    description: str = "Thank you for your donation"


class Donation3(DonationData):
    id: int = 3
    name: str = "donation3"
    amount: int = 300
    description: str = "Thank you for your donation"


class Donation4(DonationData):
    id: int = 4
    name: str = "donation4"
    amount: int = 400
    description: str = "Thank you for your donation"


class DonationTestRepo(DonationRepository):
    def __init__(self):
        self.donations = [Donation1(), Donation2(), Donation3(), Donation4()]

    def get_all_donations(self) -> list[DonationData]:
        return self.donations

    def get_donation(self, donation_id: int) -> DonationData:
        for donation in self.donations:
            if donation.id == donation_id:
                return donation
        raise HTTPException(status_code=404, detail="Donation not found")

    def create_donation(self, donation: DonationData) -> DonationData:
        self.donations.append(donation)
