from fastapi import UploadFile

from abc import ABC, abstractmethod
from core.model import *


class UserRepository(ABC):
    """
    Repository interface for user operations
    """

    @abstractmethod
    def createUser(self, userItem: UserItem) -> UserItem:
        """
        Create a new user

        Args:
            userItem (UserItem): UserItem object

        Raises:
            HTTPException(status_code=500): If failed to create user

        Returns:
            UserItem: UserItem object
        """
        pass

    @abstractmethod
    def getUser(self, userId: str) -> UserItem:
        """
        Get a user by id

        Args:
            userId (str): User id

        Returns:
            UserItem: UserItem object
        """
        pass

    @abstractmethod
    def updateUser(self, userItem: UserItem) -> UserItem:
        """
        Update a user

        Args:
            userItem (UserItem): UserItem object

        Raises:
            HTTPException(status_code=500): If failed to update

        Returns:
            UserItem: UserItem object
        """
        pass

    @abstractmethod
    def deleteUser(self, userId: str) -> bool:
        """
        Delete a user by id

        Args:
            userId (str): User id

        Returns:
            bool: True if user is deleted, False otherwise
        """
        pass


class DonationRepository(ABC):
    """
    Repository interface for donation operations
    """

    @abstractmethod
    def createDonation(self, donationItem: DonationItem) -> DonationItem:
        """
        Create a new donation item

        Args:
            donationItem (DonationItem): The donation item to create

        Raises:
            HTTPException(status_code=500): If the donation item cannot be created

        Returns:
            DonationItem: The created donation item
        """
        pass

    @abstractmethod
    def getAllDonations(self) -> list[DonationItemMeta]:
        """
        Get all donation items

        Returns:
            list[DonationItemMeta]: A list of donation items
        """
        pass

    @abstractmethod
    def getDonation(self, donationId: str) -> DonationItem:
        """
        Get a donation item by ID

        Args:
            donationId (str): The ID of the donation item to get

        Returns:
            DonationItem: The donation item if found, None otherwise
        """
        pass

    @abstractmethod
    def updateDonation(self, donationItem: DonationItem) -> DonationItem:
        """
        Update a donation item

        Args:
            donationItem (DonationItem): The donation item to update

        Raises:
            HTTPException(status_code=500): If the donation item cannot be updated

        Returns:
            DonationItem: The updated donation item
        """
        pass

    @abstractmethod
    def deleteDonation(self, donationId: str) -> bool:
        """
        Delete a donation item by ID

        Args:
            donationId (str): The ID of the donation item to delete

        Returns:
            bool: True if the donation item was deleted, False otherwise
        """
        pass


class CouponRepository(ABC):
    """
    Repository interface for coupon operations
    """

    @abstractmethod
    def createCoupon(self, couponItem: CouponItem) -> CouponItem:
        """
        Create a new coupon item

        Args:
            couponItem (CouponItem): Coupon item to be created

        Raises:
            HTTPException(status_code=500): If the coupon item cannot be created

        Returns:
            CouponItem: Created coupon item
        """
        pass

    @abstractmethod
    def getCoupon(self, couponId: str) -> CouponItem:
        """
        Get a coupon item by id

        Args:
            couponId (str): Coupon id

        Returns:
            CouponItem: Coupon item
        """
        pass

    @abstractmethod
    def updateCoupon(self, couponItem: CouponItem) -> CouponItem:
        """
        Update a coupon item

        Args:
            couponItem (CouponItem): Coupon item to be updated

        Raises:
            HTTPException(status_code=500): Failed to update coupon

        Returns:
            CouponItem: Updated coupon item
        """
        pass

    @abstractmethod
    def deleteCoupon(self, couponId: str) -> bool:
        """
        Delete a coupon item by id

        Args:
            couponId (str): Coupon id

        Returns:
            bool: True if coupon is deleted, False otherwise
        """
        pass


class ChallengeRepository(ABC):
    """
    Repository interface for challenge operations
    """

    @abstractmethod
    def createChallenge(self, challengeItem: ChallengeItem) -> ChallengeItem:
        """
        Create a new challenge

        Args:
            challengeItem (ChallengeItem): ChallengeItem object

        Raises:
            HTTPException(status_code=500): If failed to create challenge

        Returns:
            ChallengeItem: Created ChallengeItem object
        """
        pass

    @abstractmethod
    def getAllChallenges(self) -> list[ChallengeItemMeta]:
        """
        Get all challenges

        Returns:
            list[ChallengeItemMeta]: List of ChallengeItemMeta objects
        """
        pass

    @abstractmethod
    def getChallenge(self, challengeId: str) -> ChallengeItem:
        """
        Get a challenge by id

        Args:
            challengeId (str): Challenge id

        Returns:
            ChallengeItem: ChallengeItem object if found, None otherwise
        """
        pass

    @abstractmethod
    def updateChallenge(self, challengeItem: ChallengeItem) -> ChallengeItem:
        """
        Update a challenge

        Args:
            challengeItem (ChallengeItem): ChallengeItem object

        Raises:
            HTTPException(status_code=500): If failed to update challenge

        Returns:
            ChallengeItem: Updated ChallengeItem object
        """
        pass

    @abstractmethod
    def deleteChallenge(self, challengeId: str) -> bool:
        """
        Delete a challenge by id

        Args:
            challengeId (str): Challenge id

        Returns:
            bool: True if challenge is deleted, False otherwise
        """
        pass


class RewardRepository(ABC):
    """
    Repository interface for reward operations
    """

    @abstractmethod
    def createReward(self, rewardItem: RewardItem) -> RewardItem:
        """
        Create a new reward item

        Args:
            rewardItem (RewardItem): Reward item to create

        Raises:
            HTTPException(status_code=500): If failed to create reward

        Returns:
            RewardItem: Created reward item
        """
        pass

    @abstractmethod
    def getAllRewards(self) -> list[RewardItemMeta]:
        """
        Get all reward items

        Returns:
            list[RewardItemMeta]: List of reward items
        """
        pass

    @abstractmethod
    def getReward(self, rewardId: str) -> RewardItem:
        """
        Get a reward item by ID

        Args:
            rewardId (str): Reward ID

        Returns:
            RewardItem: Reward item, or None if not found
        """
        pass

    @abstractmethod
    def updateReward(self, rewardItem: RewardItem) -> RewardItem:
        """
        Update a reward item

        Args:
            rewardItem (RewardItem): Reward item to update

        Raises:
            HTTPException(status_code=500): If failed to update reward

        Returns:
            RewardItem: Updated reward item
        """
        pass

    @abstractmethod
    def deleteReward(self, rewardId: str) -> bool:
        """
        Delete a reward item by ID

        Args:
            rewardId (str): Reward ID

        Returns:
            bool: True if deleted, False if not found
        """
        pass


class FileRepository(ABC):
    """
    Repository interface for file operations
    """

    @abstractmethod
    def createFile(self, file: UploadFile, userId: str, isPrivate: bool = False) -> FileData:
        """
        Create a new file

        Args:
            file (UploadFile): File to be uploaded
            userId (str): User ID of the owner of the file

        Raises:
            HTTPException(status_code=500): If failed to create file

        Returns:
            FileData: FileData object of the uploaded file
        """
        pass

    @abstractmethod
    def getFile(self, fileId: str) -> FileData:
        """
        Get file by ID

        Args:
            fileId (str): ID of the file

        Returns:
            FileData: FileData object of the file if found, None otherwise
        """
        pass

    @abstractmethod
    def updateFile(self, file: UploadFile, fileData: FileData) -> FileData:
        """
        Update file data with new file

        Args:
            file (UploadFile): New file to be uploaded
            fileData (FileData): FileData object to be updated

        Raises:
            HTTPException(status_code=500): If failed to update file

        Returns:
            FileData: Updated FileData object
        """
        pass

    @abstractmethod
    def deleteFile(self, fileId: str) -> bool:
        """
        Delete file by ID

        Args:
            fileId (str): ID of the file

        Returns:
            bool: True if file is deleted, False otherwise
        """
        pass
