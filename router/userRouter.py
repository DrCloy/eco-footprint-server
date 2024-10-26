from fastapi import APIRouter
from pymongo.database import Database

from core.model import UserData
from core.repo import UserRepository


class UserRouter(APIRouter):
    def __init__(self, db: Database, repo: UserRepository):
        super().__init__(prefix="/user", tags=["User"])
        self.db = db
        self.collection = self.db.users
        self.repo = repo

        self.add_api_route("/register", self.register_user, methods=["POST"])
        self.add_api_route("/{userId}", self.get_user, methods=["GET"])

    def get_user(self, userId: str):
        return self.repo.getUserInfo(userId)

    def register_user(self, user: UserData):
        return self.repo.createUser(user)
