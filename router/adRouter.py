from fastapi import APIRouter, Request, HTTPException

from core.model import UserItem
from core.repo import UserRepository
from util import adVerifier


class AdRouter(APIRouter):
    def __init__(self, userRepo: UserRepository):
        super().__init__(prefix="/ssv")
        self._userRepo = userRepo

        self.add_api_route(path="/verify", endpoint=self._verifySSV, methods=["POST"])

    def _verifySSV(self, request: Request) -> bool:
        query_params = request.query_params
        key_id = query_params.get("key_id")
        signature = query_params.get("signature")

        if not key_id or not signature:
            raise HTTPException(status_code=400, detail="Bad Request")

        userId = query_params.get("user_id")
        if not userId:
            raise HTTPException(status_code=400, detail="Bad Request")
        if not self._userRepo.getUser(userId):
            raise HTTPException(status_code=404, detail="User not found")

        message = "&".join([f"{k}={v}" for k, v in query_params.items() if k not in ["key_id", "signature"]])

        if not adVerifier.verify_admob_ssv(message, key_id, signature):
            raise HTTPException(status_code=401, detail="Unauthorized")

        # TODO: Add log
        timestamp = query_params.get("timestamp")
        reward_amount = query_params.get("reward_amount")

        return {"status": "success"}
