import math
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request

from core.model import ChallengeItem, ChallengeRecordItem, UserItemMeta, ItemState
from core.repo import ChallengeRepository, FileRepository, UserRepository


class ChallengeRouter(APIRouter):
    """
    ChallengeRouter class

    This class is a router class for challenge-related API endpoints.
    """

    # Class constarnts
    CHALLENGE_PARTICIPATE_POINT = 500
    CHALLENGE_REWARD_BASE_POINT = CHALLENGE_PARTICIPATE_POINT + 100
    CHALLENGE_REWARD_ADDITIONAL_POINT = 2000

    def __init__(self, userRepo: UserRepository, challengeRepo: ChallengeRepository, fileRepo: FileRepository):
        super().__init__(prefix="/challenge")
        self._userRepo = userRepo
        self._challengeRepo = challengeRepo
        self._fileRepo = fileRepo

        self.add_api_route(
            path="/create", endpoint=self._createChallenge, methods=["POST"])
        self.add_api_route(
            path="/all", endpoint=self._getAllChallenges, methods=["GET"])
        self.add_api_route(path="/{challengeId}",
                           endpoint=self._getChallenge, methods=["GET"])
        self.add_api_route(path="/{challengeId}/participate",
                           endpoint=self._participateChallenge, methods=["POST"])
        self.add_api_route(path="/{challengeId}/add/{imageId}",
                           endpoint=self._addChallengeRecord, methods=["POST"])
        self.add_api_route(path="/{challengeId}/record/{recordId}/approve",
                           endpoint=self._changeRecordState, methods=["PUT"])
        self.add_api_route(path="/{challengeId}/clear", endpoint=self._getChallengePoint, methods=["GET"])

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
            raise HTTPException(
                status_code=400, detail="Not enough point to create the challenge")
        user.point -= self.CHALLENGE_PARTICIPATE_POINT
        self._userRepo.updateUser(user)

        challengeItem.participants = [UserItemMeta(
            id=userId, username=user.username, thumbnailId=user.thumbnailId)]
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
        if challenge.currentParticipants >= challenge.totalParticipants:
            raise HTTPException(
                status_code=400, detail="Challenge is already full")
        if not challenge.state == ItemState.ACTIVE:
            raise HTTPException(
                status_code=400, detail="Challenge is not active")

        if userId in challenge.participants:
            raise HTTPException(
                status_code=400, detail="Already participated in the challenge")

        if user.point < self.CHALLENGE_PARTICIPATE_POINT:
            raise HTTPException(
                status_code=400, detail="Not enough point to participate in the challenge")
        user.point -= self.CHALLENGE_PARTICIPATE_POINT

        challenge.currentParticipants += 1
        challenge.participants.append(UserItemMeta(
            id=userId, username=user.username, thumbnailId=user.thumbnailId))
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

        isParticipant = False
        for participant in challenge.participants:
            if participant.id == userId:
                isParticipant = True
                break
        if not isParticipant:
            raise HTTPException(status_code=401, detail="Unauthorized")

        file = self._fileRepo.getFile(imageId)
        if file is None:
            raise HTTPException(status_code=404, detail="Image not found")

        recordId = str(0 if not challenge.participantRecords else int(challenge.participantRecords[-1].id) + 1)
        challengeRecord = ChallengeRecordItem(
            id=str(recordId), userId=userId, imageId=imageId, date=str(datetime.now()))
        challenge.participantRecords.append(challengeRecord)
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
        isParticipant = False
        for participant in challenge.participants:
            if participant.id == userId:
                isParticipant = True
                break
        if not isParticipant:
            raise HTTPException(status_code=401, detail="Unauthorized")

        record = next(
            (record for record in challenge.participantRecords if record.id == recordId), None)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")

        record.approved = approve
        challenge = self._challengeRepo.updateChallenge(challenge)

        return challenge

    def _getChallengePoint(self, challengeId: str, userId: str, request: Request) -> ChallengeItem:
        """
        Get the challenge point with challengeId and userId

        Args:
            challengeId (str): The challengeId to get the point
            userId (str): The userId to get the point
            request (Request): The request object

        Raises:
            HTTPException(status_code=401): If the user is not authenticated
            HTTPException(status_code=404): If the user is not found
            HTTPException(status_code=404): If the challenge is not found

        Returns:
            ChallengeItem: The challenge with the point
        """
        if request.state.auth is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if request.state.auth["sub"] is None:
            raise HTTPException(status_code=404, detail="User not found")

        user = self._userRepo.getUser(userId)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        challenge = self._challengeRepo.getChallenge(challengeId)
        if challenge is None:
            raise HTTPException(status_code=404, detail="Challenge not found")
        if not challenge.state == ItemState.FINISHED:
            raise HTTPException(
                status_code=400, detail="Challenge is not finished yet")

        isParticipant = False
        for participant in challenge.participants:
            if participant.id == userId:
                isParticipant = True
                break
        if not isParticipant:
            raise HTTPException(status_code=401, detail="Unauthorized")

        totalPoint = self.CHALLENGE_REWARD_BASE_POINT
        userRecordCount = len(list(filter(lambda record: record.userId == userId, challenge.participantRecords)))
        totalPoint += math.floor(self.CHALLENGE_REWARD_ADDITIONAL_POINT * (userRecordCount / len(challenge.participantRecords)))

        user.point += totalPoint
        self._userRepo.updateUser(user)

        challenge.currentParticipants -= 1
        if challenge.currentParticipants == 0:
            challenge.state = ItemState.INACTIVE

        return challenge
