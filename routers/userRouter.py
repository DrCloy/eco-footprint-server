from fastapi import APIRouter
from core.repo import UserRepository


def create_user_router(repo: UserRepository):
    router = APIRouter(prefix="/user", tags=["User"])

    @router.get("/{user_id}")
    def get_user(user_id: str):
        return repo.get_user(user_id)

    return router
