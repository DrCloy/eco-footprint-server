from fastapi import APIRouter, Request, HTTPException

from core.repo import UserRepository
from util import adVerifier


class AdRouter(APIRouter):
    def __init__(self, userRepo: UserRepository, adVerifier: adVerifier):
        super().__init__(prefix="/ssv")
        self._userRepo = userRepo
        self._adVerifier = adVerifier

        self.add_api_route(path="/verify", endpoint=self._verifySSV, methods=["POST"])

    async def _verifySSV(self, request: Request) -> bool:
        """
        Verify the AdMob SSV
        This is a route for Google Admob Server-Side Verification (SSV) callback.
        """
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

        message = "&".join([f"{k}={v}" for k, v in sorted(query_params.items(), key=lambda x: x[0]) if k not in ["key_id", "signature"]])

        if not self._adVerifier.verify_admob_ssv(message, key_id, signature):
            raise HTTPException(status_code=401, detail="Unauthorized")

        # TODO: Add log
        log = dict(
            user_id=query_params.get("user_id"),
            reward_amount=query_params.get("reward_amount"),
            timestamp=query_params.get("timestamp"),
        )
        await self._adVerifier.add_log(log)

        return {"status": "success"}
