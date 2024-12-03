from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database

from core.model import RewardItem, RewardItemMeta
from core.repo import RewardRepository


class RewardMongoRepo(RewardRepository):
    """
    Implementation of RewardRepository using MongoDB
    """

    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        if self._db.get_collection("rewards") is None:
            self._db.create_collection("rewards")

        self._collection = self._db["rewards"]

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
        rewardItem.id = str(ObjectId())

        self._collection.insert_one(rewardItem.model_dump())

        reward = self._collection.find_one({"id": rewardItem.id})
        if reward:
            return RewardItem(**reward)
        else:
            raise HTTPException(status_code=500, detail="Failed to create reward")

    def getAllRewards(self) -> list[RewardItemMeta]:
        """
        Get all reward items

        Returns:
            list[RewardItemMeta]: List of reward items
        """
        rewards = self._collection.find()
        return [RewardItemMeta(**reward) for reward in rewards]

    def getReward(self, rewardId: str) -> RewardItem:
        """
        Get a reward item by ID

        Args:
            rewardId (str): Reward ID

        Returns:
            RewardItem: Reward item, or None if not found
        """
        reward = self._collection.find_one({"id": rewardId})
        if reward:
            return RewardItem(**reward)
        else:
            return None

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
        self._collection.update_one({"id": rewardItem.id}, {"$set": rewardItem.model_dump()})

        reward = self._collection.find_one({"id": rewardItem.id})
        if rewardItem == reward:
            return RewardItem(**reward)
        else:
            raise HTTPException(status_code=500, detail="Failed to update reward")

    def deleteReward(self, rewardId: str) -> bool:
        """
        Delete a reward item by ID

        Args:
            rewardId (str): Reward ID

        Returns:
            bool: True if deleted, False if not found
        """
        result = self._collection.delete_one({"id": rewardId})
        return result.deleted_count > 0
