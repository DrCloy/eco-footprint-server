from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database

from core.model import ChallengeItem, ChallengeItemMeta, ItemState, UserItemMeta
from core.repo import ChallengeRepository


class ChallengeMongoRepo(ChallengeRepository):
    """
    Implementation of ChallengeRepository using MongoDB
    """

    def __init__(self, db: Database):
        super().__init__()
        self._db = db

        if self._db.get_collection("challenges") is None:
            self._db.create_collection("challenges")
        self._collection = self._db["challenges"]

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
        challengeItem.id = str(ObjectId())
        challengeItem.state = ItemState.ACTIVE
        self._collection.insert_one(challengeItem.model_dump())

        challenge = self._collection.find_one({"id": challengeItem.id})
        if challenge:
            return ChallengeItem(**challenge)
        else:
            raise HTTPException(
                status_code=500, detail="Failed to create challenge")

    def getAllChallenges(self) -> list[ChallengeItemMeta]:
        """
        Get all challenges

        Returns:
            list[ChallengeItemMeta]: List of ChallengeItemMeta objects
        """
        challenges = self._collection.find()
        return [ChallengeItemMeta(**challenge) for challenge in challenges]

    def getChallenge(self, challengeId: str) -> ChallengeItem:
        """
        Get a challenge by id

        Args:
            challengeId (str): Challenge id

        Returns:
            ChallengeItem: ChallengeItem object if found, None otherwise
        """
        challenge = self._collection.find_one({"id": challengeId})
        participants = [UserItemMeta(**participant) for participant in challenge.pop("participants")]
        if challenge:
            return ChallengeItem(participants=participants, **challenge)
        else:
            return None

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
        self._collection.update_one({"id": challengeItem.id}, {
                                    "$set": challengeItem.model_dump()})

        challenge = self._collection.find_one({"id": challengeItem.id})
        if challengeItem == challenge:
            return ChallengeItem(**challenge)
        else:
            raise HTTPException(
                status_code=500, detail="Failed to update challenge")

    def deleteChallenge(self, challengeId: str) -> bool:
        """
        Delete a challenge by id

        Args:
            challengeId (str): Challenge id

        Returns:
            bool: True if challenge is deleted, False otherwise
        """
        result = self._collection.delete_one({"id": challengeId})
        return result.deleted_count > 0
