import pymongo

from fastapi import HTTPException
import pymongo.database

from core.model import UserData
from core.repo import UserRepository


class UserMongoRepo(UserRepository):
    def __init__(self, db: pymongo.database.Database):
        super().__init__()
        self.db = db
        self.collection = self.db.users

    def getUserInfo(self, userId: str) -> UserData:
        user = self.collection.find_one({"id": userId})
        if user:
            return UserData(**user)
        raise HTTPException(status_code=404, detail="User not found")

    def createUser(self, user: UserData) -> UserData:
        if self.collection.find_one({"id": user.id}):
            raise HTTPException(status_code=400, detail="User already exists")
        self.collection.insert_one(user.model_dump())

        return self.getUserInfo(user.id)
