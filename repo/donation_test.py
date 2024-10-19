from fastapi import HTTPException

from core.model import DonationData
from core.repo import DonationRepository


class Donation1(DonationData):
    id: int = 1
    user_id: str = "1"
    amount: int = 100
    message: str = "Thank you for your donation"


class Donation2(DonationData):
    id: int = 2
    user_id: str = "2"
    amount: int = 200
    message: str = "Thank you for your donation"


class Donation3(DonationData):
    id: int = 3
    user_id: str = "3"
    amount: int = 300
    message: str = "Thank you for your donation"


class Donation4(DonationData):
    id: int = 4
    user_id: str = "4"
    amount: int = 400
    message: str = "Thank you for your donation"


class DonationTestRepo(DonationRepository):
    def get_all_donations(self) -> list[DonationData]:
        return [Donation1(), Donation2(), Donation3(), Donation4()]

    def get_donation(self, donation_id: int) -> DonationData:
        if donation_id == 1:
            return Donation1()
        elif donation_id == 2:
            return Donation2()
        elif donation_id == 3:
            return Donation3()
        elif donation_id == 4:
            return Donation4()
        else:
            raise HTTPException(status_code=404, detail="Donation not found")
