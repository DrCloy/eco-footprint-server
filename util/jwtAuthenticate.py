import json
import urllib
import base64
from jwcrypto import jwk, jwt, common

admob_key = [
    {
        "keyId": 3335741209,
        "pem": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+nzvoGqvDeB9+SzE6igTl7TyK4JB\nbglwir9oTcQta8NuG26ZpZFxt+F2NDk7asTE6/2Yc8i1ATcGIqtuS5hv0Q==\n-----END PUBLIC KEY-----",
        "base64": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+nzvoGqvDeB9+SzE6igTl7TyK4JBbglwir9oTcQta8NuG26ZpZFxt+F2NDk7asTE6/2Yc8i1ATcGIqtuS5hv0Q=="
    }
]

admob_key_url = "https://www.gstatic.com/admob/reward/verifier-keys.json"

jwkset = jwk.JWKSet()
for key in admob_key:
    jwk_obj = jwk.JWK.from_pem(data=key["pem"].encode())
    jwk_obj.update({"kid": key["keyId"]})
    jwkset.add(jwk_obj)


def __parse_ssv(ssv: str) -> dict:
    ssv_dict = {}


def ssv_verify(ssv: str):
    pass
