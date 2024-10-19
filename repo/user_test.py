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
    def get_user(self, user_id: str) -> UserData:
        if user_id == "1":
            return User1()
        elif user_id == "2":
            return User2()
        elif user_id == "3":
            return User3()
        elif user_id == "4":
            return User4()
        else:
            raise HTTPException(status_code=404, detail="User not found")
