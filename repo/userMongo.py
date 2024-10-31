import pymongo

from fastapi import HTTPException

from pymongo.database import Database

from core.model import UserItem
from core.repo import UserRepository


class UserMongoRepo(UserRepository):
    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self._collection = db["users"]

    def createUser(self, userItem: UserItem) -> UserItem:
        self._collection.insert_one(userItem.model_dump())

        user = self._collection.find_one({"id": userItem.id})
        if user:
            return UserItem(**user)
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")

    def getUser(self, userId: str) -> UserItem:
        user = self._collection.find_one({"id": userId})
        if user:
            return UserItem(**user)
        else:
            raise HTTPException(status_code=404, detail="User not found")

    def updateUser(self, userItem: UserItem) -> UserItem:
        self._collection.update_one({"id": userItem.id}, {"$set": userItem.model_dump()})

        user = self._collection.find_one({"id": userItem.id})
        if userItem == user:
            return UserItem(**user)
        else:
            raise HTTPException(status_code=500, detail="Failed to update user")

    def deleteUser(self, userId: str) -> bool:
        result = self._collection.delete_one({"id": userId})
        return result.deleted_count > 0
