from fastapi import APIRouter, Request, HTTPException

from core.model import UserItem
from core.repo import UserRepository


class UserRouter(APIRouter):
    def __init__(self, userRepo: UserRepository):
        super().__init__()
        self._userRepo = userRepo

        self.add_api_route(path="/register", endpoint=self.register, methods=["POST"])
        self.add_api_route(path="/profile/{userId}", endpoint=self.getProfile, methods=["GET"])
        self.add_api_route(path="/profile", endpoint=self.updateProfile, methods=["Put"])
        self.add_api_route(path="/delete/{userId}", endpoint=self.deleteUser, methods=["DELETE"])

    def register(self, userItem: UserItem, request: Request):
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if request.state.auth["role"] == "test":
            userId = request.state.auth["userId"]
        else:
            userId = request.state.auth["sub"]
            if self.getProfile(userId, request):
                raise HTTPException(status_code=409, detail="User already exists")

        userItem.userId = userId
        user = self._userRepo.createUser(userItem)

        return user

    def getProfile(self, userId: str, request: Request):
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if request.state.auth["role"] == "test":
            pass
        else:
            if request.state.auth["sub"] != userId:
                raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(userId)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def updateProfile(self, userItem: UserItem, request: Request):
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if request.state.auth["role"] == "test":
            pass
        else:
            if not self.getProfile(request.state.auth["sub"], request):
                raise HTTPException(status_code=404, detail="User not found")
        userItem.userId = request.state.auth["sub"]

        user = self._userRepo.updateUser(userItem)

        return user

    def deleteUser(self, userId: str, request: Request):
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
