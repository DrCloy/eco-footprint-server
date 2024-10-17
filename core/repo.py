from abc import ABC, abstractmethod
from core.model import UserData, DonationData, CampainData


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> UserData:
        pass


class DonationRepository(ABC):
    @abstractmethod
    def get_donation(self, donation_id: int) -> DonationData:
        pass


class CampainRepository(ABC):
    @abstractmethod
    def get_campain(self, campain_id: int) -> CampainData:
        pass
