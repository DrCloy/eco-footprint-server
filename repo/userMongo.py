from fastapi import HTTPException
from pymongo.database import Database

from core.model import UserItem
from core.repo import UserRepository


class UserMongoRepo(UserRepository):
    """
    Implementation of UserRepository interface for MongoDB
    """

    def __init__(self, db: Database):
        super().__init__()
        self._db = db

        if self._db.get_collection("users") is None:
            self._db.create_collection("users")
        self._collection = db["users"]

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
        self._collection.insert_one(userItem.model_dump())

        user = self._collection.find_one({"id": userItem.id})
        if user:
            return UserItem(**user)
        else:
            raise HTTPException(
                status_code=500, detail="Failed to create user")

    def getUser(self, userId: str) -> UserItem:
        """
        Get a user by id

        Args:
            userId (str): User id

        Returns:
            UserItem: UserItem object
        """
        user = self._collection.find_one({"id": userId})
        if user:
            return UserItem(**user)
        else:
            return None

    def updateUser(self, userItem: UserItem) -> UserItem:
        """
        Update a user

        Args:
            userItem (UserItem): UserItem object

        Raises:
            HTTPException(status_code=500): If failed to update user

        Returns:
            UserItem: UserItem object
        """
        self._collection.update_one(
            {"id": userItem.id}, {"$set": userItem.model_dump()})

        user = self._collection.find_one({"id": userItem.id})
        if not user:
            raise HTTPException(
                status_code=500, detail="Failed to update user")

        newUser = UserItem(**user)
        if newUser == userItem:
            return newUser
        else:
            raise HTTPException(
                status_code=500, detail="Failed to update user")

    def deleteUser(self, userId: str) -> bool:
        """
        Delete a user by id

        Args:
            userId (str): User id

        Returns:
            bool: True if user is deleted, False otherwise
        """
        result = self._collection.delete_one({"id": userId})
        return result.deleted_count > 0
