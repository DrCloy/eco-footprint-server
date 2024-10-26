from fastapi import APIRouter

from core.model import UserData
from core.repo import UserRepository


def create_user_router(repo: UserRepository):
    router = APIRouter(prefix="/user", tags=["User"])

    @router.get("/{userId}")
    def get_user(userId: str):
        return repo.getUserInfo(userId)

    @router.post("/register")
    def register_user(user: UserData):
        return repo.createUser(user)

    return router
