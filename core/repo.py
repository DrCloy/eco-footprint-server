from abc import ABC, abstractmethod
from core.model import UserData, DonationData, CampainData


class UserRepository(ABC):
    @abstractmethod
    def getUserInfo(self, userId: str) -> UserData:
        pass


class DonationRepository(ABC):
    @abstractmethod
    def getAllDonations(self) -> list[DonationData]:
        pass

    @abstractmethod
    def getDonation(self, donationId: int) -> DonationData:
        pass

    @abstractmethod
    def createDonation(self, donation: DonationData) -> DonationData:
        pass


class CampainRepository(ABC):
    @abstractmethod
    def getCampain(self, campainId: int) -> CampainData:
        pass
