from fastapi import UploadFile

from abc import ABC, abstractmethod
from core.model import *


class UserRepository(ABC):
    @abstractmethod
    def createUser(self, userItem: UserItem) -> UserItem:
        pass

    @abstractmethod
    def getUser(self, userId: str) -> UserItem:
        pass

    @abstractmethod
    def updateUser(self, userItem: UserItem) -> UserItem:
        pass

    @abstractmethod
    def deleteUser(self, userId: str) -> bool:
        pass


class DonationRepository(ABC):
    @abstractmethod
    def createDonation(self, donationItem: DonationItem) -> DonationItem:
        pass

    @abstractmethod
    def getAllDonations(self) -> list[DonationItemMeta]:
        pass

    @abstractmethod
    def getDonation(self, donationId: str) -> DonationItem:
        pass

    @abstractmethod
    def updateDonation(self, donationItem: DonationItem) -> DonationItem:
        pass

    @abstractmethod
    def deleteDonation(self, donationId: str) -> bool:
        pass


class CouponRepository(ABC):
    @abstractmethod
    def createCoupon(self, couponItem: CouponItem) -> CouponItem:
        pass

    @abstractmethod
    def getAllCoupons(self) -> list[CouponItemMeta]:
        pass

    @abstractmethod
    def getCoupon(self, couponId: str) -> CouponItem:
        pass

    @abstractmethod
    def updateCoupon(self, couponItem: CouponItem) -> CouponItem:
        pass

    @abstractmethod
    def deleteCoupon(self, couponId: str) -> bool:
        pass


class ChallengeRepository(ABC):
    @abstractmethod
    def createChallenge(self, challengeItem: ChallengeItem) -> ChallengeItem:
        pass

    @abstractmethod
    def getAllChallenges(self) -> list[ChallengeItemMeta]:
        pass

    @abstractmethod
    def getChallenge(self, challengeId: str) -> ChallengeItem:
        pass

    @abstractmethod
    def updateChallenge(self, challengeItem: ChallengeItem) -> ChallengeItem:
        pass

    @abstractmethod
    def deleteChallenge(self, challengeId: str) -> bool:
        pass


class RewardRepository(ABC):
    @abstractmethod
    def createReward(self, rewardItem: RewardItem) -> RewardItem:
        pass

    @abstractmethod
    def getAllRewards(self) -> list[RewardItemMeta]:
        pass

    @abstractmethod
    def getReward(self, rewardId: str) -> RewardItem:
        pass

    @abstractmethod
    def updateReward(self, rewardItem: RewardItem) -> RewardItem:
        pass

    @abstractmethod
    def deleteReward(self, rewardId: str) -> bool:
        pass


class FileRepository(ABC):
    @abstractmethod
    def createFile(self, file: UploadFile) -> FileData:
        pass

    @abstractmethod
    def getFile(self, fileId: str) -> FileData:
        pass

    @abstractmethod
    def updateFile(self, file: UploadFile, fileData: FileData) -> FileData:
        pass

    @abstractmethod
    def deleteFile(self, fileId: str) -> bool:
        pass
