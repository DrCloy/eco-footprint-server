from fastapi import HTTPException

from pymongo.database import Database

from core.model import RewardItem, RewardItemMeta
from core.repo import RewardRepository


class RewardMongoRepo(RewardRepository):
    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self._collection = db["rewards"]

    def createReward(self, rewardItem: RewardItem) -> RewardItem:
        self._collection.insert_one(rewardItem.model_dump())

        reward = self._collection.find_one({"id": rewardItem.id})
        if reward:
            return RewardItem(**reward)
        else:
            raise HTTPException(status_code=500, detail="Failed to create reward")

    def getAllRewards(self) -> list[RewardItemMeta]:
        rewards = self._collection.find()
        return [RewardItemMeta(**reward) for reward in rewards]

    def getReward(self, rewardId: str) -> RewardItem:
        reward = self._collection.find_one({"id": rewardId})
        if reward:
            return RewardItem(**reward)
        else:
            raise HTTPException(status_code=404, detail="Reward not found")

    def updateReward(self, rewardItem: RewardItem) -> RewardItem:
        self._collection.update_one({"id": rewardItem.id}, {"$set": rewardItem.model_dump()})

        reward = self._collection.find_one({"id": rewardItem.id})
        if rewardItem == reward:
            return RewardItem(**reward)
        else:
            raise HTTPException(status_code=500, detail="Failed to update reward")

    def deleteReward(self, rewardId: str) -> bool:
        result = self._collection.delete_one({"id": rewardId})
        return result.deleted_count > 0
