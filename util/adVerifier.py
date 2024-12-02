import json
import urllib
import base64
import hashlib
from ecdsa.util import sigdecode_der
from ecdsa.keys import VerifyingKey, BadSignatureError


class AdVerifier:
    ADMOBKEYURL = "https://www.gstatic.com/admob/reward/verifier-keys.json"
    ADMOBKEY = dict()

    def __init__(self):
        self.get_admob_key()

    def get_admob_key(self):
        self.ADMOBKEY = dict()
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
            self.ADMOBKEY[key['keyId']] = dict(
                pem=key['pem'],
                base64=key['base64']
            )

    def verify_admob_ssv(self, message: str, key_id: str, signature: str):
        if key_id not in self.ADMOBKEY:
            return False

        key = self.ADMOBKEY[key_id]
        vk = VerifyingKey.from_pem(key['pem'])
        signature = base64.urlsafe_b64decode(signature + '=' * (4 - len(signature) % 4))
        message = message.encode("utf-8")
        try:
            vk.verify(signature, message, hashfunc=hashlib.sha256, sigdecode=sigdecode_der)
            return True
        except BadSignatureError:
            return False
