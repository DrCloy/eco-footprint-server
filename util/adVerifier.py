import asyncio
import base64
import hashlib
import json
import time
import urllib.request

from ecdsa.keys import BadSignatureError, VerifyingKey
from ecdsa.util import sigdecode_der


class AdVerifier:
    ADMOBKEYURL = "https://www.gstatic.com/admob/reward/verifier-keys.json"

    def __init__(self):
        self.admob_key = dict()
        self.ad_verify_log = []
        self.lock = asyncio.Lock()
        self.get_admob_key()

    def get_admob_key(self):
        self.admob_key = dict()
        response = urllib.request.urlopen(self.ADMOBKEYURL)
        if response.status != 200:
            return

        keys_data = response.read().decode("utf-8")
        if not keys_data:
            return

        keys = json.loads(keys_data)
        if not keys or 'keys' not in keys:
            return

        for key in keys['keys']:
            self.admob_key[key['keyId']] = dict(
                pem=key['pem'],
                base64=key['base64']
            )

    def verify_admob_ssv(self, message: str, key_id: str, signature: str):
        if key_id not in self.admob_key:
            return False

        key = self.admob_key[key_id]
        vk = VerifyingKey.from_pem(key['pem'])
        signature = base64.urlsafe_b64decode(signature + '=' * (4 - len(signature) % 4))
        message = message.encode("utf-8")
        try:
            vk.verify(signature, message, hashfunc=hashlib.sha256, sigdecode=sigdecode_der)
            return True
        except BadSignatureError:
            return False

    async def add_log(self, log: dict):
        try:
            async with self.lock:
                self.ad_verify_log.append(log)
            return True
        except Exception:
            return False

    def check_log(self, user_id: str):
        for log in self.ad_verify_log:
            if log['user_id'] == user_id:
                if time.time() - (int(log['timestamp']) / 1000) < 60 * 5:
                    return int(log['reward_amount'])
        return -1

    async def delete_log(self, user_id: str):
        try:
            async with self.lock:
                self.ad_verify_log = [log for log in self.ad_verify_log if log['user_id'] != user_id]
            return True
        except Exception:
            return False
