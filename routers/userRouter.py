from fastapi import APIRouter
from core.repo import UserRepository


def create_user_router(repo: UserRepository):
    router = APIRouter(prefix="/user", tags=["User"])

    @router.get("/{userId}")
    def get_user(userId: str):
        return repo.getUserInfo(userId)

    return router
