from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request

from core.model import ChallengeItem, ChallengeRecordItem, UserItemMeta
from core.repo import ChallengeRepository, FileRepository, UserRepository


class ChallengeRouter(APIRouter):
    """
    ChallengeRouter class

    This class is a router class for challenge-related API endpoints.
    """

    # Class constarnts
    CHALLENGE_PARTICIPATE_POINT = 50
    CHALLENGE_REWARD_ADDITIONAL_POINT = 100

    def __init__(self, userRepo: UserRepository, challengeRepo: ChallengeRepository, fileRepo: FileRepository):
        super().__init__(prefix="/challenge")
        self._userRepo = userRepo
        self._challengeRepo = challengeRepo
        self._fileRepo = fileRepo

        self.add_api_route(path="/create", endpoint=self._createChallenge, methods=["POST"])
        self.add_api_route(path="/all", endpoint=self._getAllChallenges, methods=["GET"])
        self.add_api_route(path="/{challengeId}", endpoint=self._getChallenge, methods=["GET"])
        self.add_api_route(path="/{challengeId}/participate", endpoint=self._participateChallenge, methods=["POST"])
        self.add_api_route(path="/{challengeId}/add/{imageId}", endpoint=self._addChallengeRecord, methods=["POST"])
        self.add_api_route(path="/{challengeId}/record/{recordId}/approve", endpoint=self._changeRecordState, methods=["PUT"])

    def _createChallenge(self, challengeItem: ChallengeItem, request: Request) -> ChallengeItem:
        """
        Create a new challenge

        Args:
            challengeItem (ChallengeItem): The challengeItem to create
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found

        Returns:
            ChallengeItem: The created challengeItem
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] is None:
            raise HTTPException(status_code=404, detail="User not found")

        userId = request.state.auth["sub"]
        user = self._userRepo.getUser(userId)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user.point < self.CHALLENGE_PARTICIPATE_POINT:
            raise HTTPException(status_code=400, detail="Not enough point to create the challenge")
        user.point -= self.CHALLENGE_PARTICIPATE_POINT
        self._userRepo.updateUser(user)

        challengeItem.participants = UserItemMeta(id=userId, username=user.username, thumbnailId=user.thumbnailId)
        challengeItem.currentParticipants = 1
        challengeItem = self._challengeRepo.createChallenge(challengeItem)

        return challengeItem

    def _getAllChallenges(self):
        """
        Get all challenges

        Returns:
            list[ChallengeItemMeta]: The list of all challenges
        """
        return self._challengeRepo.getAllChallenges()

    def _getChallenge(self, challengeId: str):
        """
        Get the challenge with challengeId

        Args:
            challengeId (str): The challengeId to get the challenge

        Raises:
            HTTPException(status_code=404): If the challenge is not found

        Returns:
            ChallengeItem: The challenge
        """
        challenge = self._challengeRepo.getChallenge(challengeId)
        if challenge is None:
            raise HTTPException(status_code=404, detail="Challenge not found")

        return challenge

    def _participateChallenge(self, challengeId: str, request: Request) -> ChallengeItem:
        """
        Participate the challenge with challengeId

        Args:
            challengeId (str): The challengeId to participate
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If the user already participated in the challenge
            HTTPException(status_code=400): If the user does not have enough point to participate in the challenge
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found
            HTTPException(status_code=404): If the challenge is not found

        Returns:
            ChallengeItem: The participated challenge
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] is None:
            raise HTTPException(status_code=404, detail="User not found")

        userId = request.state.auth["sub"]
        user = self._userRepo.getUser(userId)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        challenge = self._challengeRepo.getChallenge(challengeId)
        if challenge is None:
            raise HTTPException(status_code=404, detail="Challenge not found")

        if userId in challenge.participants:
            raise HTTPException(status_code=400, detail="Already participated in the challenge")

        if user.point < self.CHALLENGE_PARTICIPATE_POINT:
            raise HTTPException(status_code=400, detail="Not enough point to participate in the challenge")
        user.point -= self.CHALLENGE_PARTICIPATE_POINT

        challenge.currentParticipants += 1
        challenge.participants.append(UserItemMeta(id=userId, username=user.username, thumbnailId=user.thumbnailId))
        self._userRepo.updateUser(user)
        self._challengeRepo.updateChallenge(challenge)

        return challenge

    def _addChallengeRecord(self, challengeId: str, imageId: str, request: Request) -> ChallengeItem:
        """
        Approve the challenge record with challengeId and imageId

        Args:
            challengeId (str): The challengeId to approve the record
            imageId (str): The imageId to approve the record
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the challenge is not found
            HTTPException(status_code=404): If the image is not found

        Returns:
            ChallengeItem: The approved challenge
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] is None:
            raise HTTPException(status_code=404, detail="User not found")

        userId = request.state.auth["sub"]
        user = self._userRepo.getUser(userId)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        challenge = self._challengeRepo.getChallenge(challengeId)
        if challenge is None:
            raise HTTPException(status_code=404, detail="Challenge not found")

        file = self._fileRepo.getFile(imageId)
        if file is None:
            raise HTTPException(status_code=404, detail="Image not found")

        challengeRecord = ChallengeRecordItem(id=str(ObjectId()), userId=userId, imageId=imageId, date=str(datetime.now()))
        challenge.records.append(challengeRecord)
        challenge = self._challengeRepo.updateChallenge(challenge)

        return challenge

    def _changeRecordState(self, challengeId: str, recordId: str, request: Request, approve: bool = True) -> ChallengeItem:
        """
        Change the record state with challengeId and recordId

        Args:
            challengeId (str): The challengeId to change the record state
            recordId (str): The recordId to change the record state
            request (Request): The request object
            approve (bool): The approve flag

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the challenge is not found
            HTTPException(status_code=404): If the record is not found

        Returns:
            ChallengeItem: The updated challenge
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] is None:
            raise HTTPException(status_code=404, detail="User not found")

        userId = request.state.auth["sub"]
        user = self._userRepo.getUser(userId)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        challenge = self._challengeRepo.getChallenge(challengeId)
        if challenge is None:
            raise HTTPException(status_code=404, detail="Challenge not found")
        if userId not in challenge.participants:
            raise HTTPException(status_code=401, detail="Unauthorized")

        record = next((record for record in challenge.records if record.id == recordId), None)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")

        record.approved = approve
        challenge = self._challengeRepo.updateChallenge(challenge)

        return challenge
