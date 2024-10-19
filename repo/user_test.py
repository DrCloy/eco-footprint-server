from core.model import UserData
from core.repo import UserRepository
from fastapi import HTTPException


class User1(UserData):
    id: str = "1"
    username: str = "user1"
    point: int = 100
    thumbnailURL: str = ""


class User2(UserData):
    id: str = "2"
    username: str = "user2"
    point: int = 200
    thumbnailURL: str = ""


class User3(UserData):
    id: str = "3"
    username: str = "user3"
    point: int = 300
    thumbnailURL: str = ""


class User4(UserData):
    id: str = "4"
    username: str = "user4"
    point: int = 400
    thumbnailURL: str = ""


class UserTestRepo(UserRepository):
    def __init__(self):
        self.user = [User1(), User2(), User3(), User4()]

    def get_user(self, user_id: str) -> UserData:
        for u in self.user:
            if u.id == user_id:
                return u
        raise HTTPException(status_code=404, detail="User not found")
