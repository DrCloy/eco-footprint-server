from fastapi import APIRouter, Request, HTTPException

from core.model import UserItem
from core.repo import UserRepository


class UserRouter(APIRouter):
    def __init__(self, userRepo: UserRepository):
        super().__init__(prefix="/user")
        self._userRepo = userRepo

        self.add_api_route(path="/register", endpoint=self.register, methods=["POST"])
        self.add_api_route(path="/profile/{userId}", endpoint=self.getProfile, methods=["GET"])
        self.add_api_route(path="/profile", endpoint=self.updateProfile, methods=["PUT"])
        self.add_api_route(path="/delete/{userId}", endpoint=self.deleteUser, methods=["DELETE"])

    def register(self, userItem: UserItem, request: Request) -> UserItem:
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth["sub"]
        if self._userRepo.getUser(userId):
            raise HTTPException(status_code=409, detail="User already exists")

        userItem.id = userId
        user = self._userRepo.createUser(userItem)

        return user

    def getProfile(self, userId: str, request: Request) -> UserItem:
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if request.state.auth["sub"] != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(userId)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    # TODO: 사용자의 권한으로는 수정할 수 없는 정보들에 대해서 어떻게 수정할 지 해결해야 함(point)
    def updateProfile(self, userItem: UserItem, request: Request) -> UserItem:
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self.getProfile(request.state.auth["sub"], request)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.couponList == userItem.couponList:
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not user.challengeList == userItem.challengeList:
            raise HTTPException(status_code=403, detail="Unauthorized")

        user = self._userRepo.updateUser(userItem)

        return user

    def deleteUser(self, userId: str, request: Request) -> bool:
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if request.state.auth["role"] == "test":
            pass
        else:
            if not self.getProfile(request.state.auth["sub"], request):
                raise HTTPException(status_code=404, detail="User not found")
            if request.state.auth["sub"] != userId:
                raise HTTPException(status_code=401, detail="Unauthorized")

        result = self._userRepo.deleteUser(userId)

        return result
