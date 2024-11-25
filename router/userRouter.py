from fastapi import APIRouter, Request, HTTPException

from core.model import UserItem
from core.repo import UserRepository


class UserRouter(APIRouter):
    """
    UserRouter class

    This class is a router class for user-related API endpoints.
    """

    def __init__(self, userRepo: UserRepository):
        super().__init__(prefix="/user")
        self._userRepo = userRepo

        self.add_api_route(path="/register", endpoint=self._register, methods=["POST"])
        self.add_api_route(path="/profile/{userId}", endpoint=self._getProfile, methods=["GET"])
        self.add_api_route(path="/profile", endpoint=self._updateProfile, methods=["PUT"])
        self.add_api_route(path="/delete/{userId}", endpoint=self._deleteUser, methods=["DELETE"])

    def _register(self, userItem: UserItem, request: Request) -> UserItem:
        """
        Register a new user

        Args:
            userItem (UserItem): The userItem to register
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=409): If the user already exists

        Returns:
            UserItem: The registered userItem
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        userId = request.state.auth["sub"]
        if self._userRepo.getUser(userId):
            raise HTTPException(status_code=409, detail="User already exists")

        userItem.id = userId
        user = self._userRepo.createUser(userItem)

        return user

    def _getProfile(self, userId: str, request: Request) -> UserItem:
        """
        Get the user profile with userId

        Args:
            userId (str): The userId to get the profile
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found

        Returns:
            UserItem: The user profile
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._userRepo.getUser(userId)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def _updateProfile(self, userItem: UserItem, request: Request) -> UserItem:
        """
        Update the user profile with userItem

        Args:
            userItem (UserItem): The userItem to update
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If the userItem is invalid
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found

        Returns:
            UserItem: The updated user profile
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self._getProfile(request.state.auth["sub"], request)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.couponList == userItem.couponList:
            raise HTTPException(status_code=400, detail="Bad Request")
        if not user.challengeList == userItem.challengeList:
            raise HTTPException(status_code=400, detail="Bad Request")

        user = self._userRepo.updateUser(userItem)

        return user

    # TODO: Implement the following methods
    def _addPoint(self, request: Request) -> UserItem:
        """
        Add point to the user
        This route is callback route for Google AdMob reward video ad.
        """
        pass

    def _deleteUser(self, userId: str, request: Request) -> bool:
        """
        Delete the user with userId

        Args:
            userId (str): The userId to delete
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found

        Returns:
            bool: True if the user is successfully deleted, False otherwise
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not self._getProfile(request.state.auth["sub"], request):
            raise HTTPException(status_code=404, detail="User not found")
        if request.state.auth["sub"] != userId:
            raise HTTPException(status_code=401, detail="Unauthorized")

        result = self._userRepo.deleteUser(userId)

        return result
