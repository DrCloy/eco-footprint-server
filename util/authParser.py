import json
import os

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwcrypto import common, jwk, jwt

google_public_keys = [
    {
        "kid": "e863fe292fa2a2967cd7551c42a1211bcac55071",
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": "wf1QrSd3mb3vX2ntibkz-lyQ67UeNJ_q44U-VzJIv9ysj2fM_tOplcS3zPG1nQ0_o85LmP_ivM6svoUwZ4PPizDaE6-Ahk6Cngv9FtN98GbsFDuou3aLNuwA6cvR_TCMXyfAO69oDjph9wviHH0WSyV-jqXjvzt8fVOiARhYN5BsH25YgnGRKW3r5RUxLYEamDWQ8UMCy8x1OPrY6LioKR5lXchjUAGLjx-dBUw6sj6fA8LJKt4XaQ62bGQrs93jlIKir_hRUPeEhrNSFLCr3W0yVjlCh5a9dIcgSkaa5oIJYQTFQq6jHznrsKC4i4POa601TcjMsjBc_6n5Qof8iQ",
        "e": "AQAB"
    },
    {
        "kid": "1dc0f172e8d6ef382d6d3a231f6c197dd68ce5ef",
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": "3zWQqZ_EHrbvwfuq3H7TCBDeanfgxcPxno8GuNQwo5vZQG6hVPqB_NfKNejm2PQG6icoueswY1x-TXdYhn7zuVRrbdiz1Cn2AsUFHhD-FyUipbeXxJPe7dTSQaYwPyzQKNWU_Uj359lXdqXQ_iT-M_QknGTXsf4181r1FTaRMb-89Koj2ZHSHZx-uaPKNzrS92XHoxFXqlMMZYivqEAUE_kAJp-jQ5I5AAQf318zVGPVJX7BxkbcPaM46SZNJaD0ya7uhKWwluqgSjHkOObI5bbq9LmV3N51jzPgxGrH2OEeQBCXzggYzjMVlNuUnfQbNKvF3Xqc4HHWXulDsszGRQ",
        "e": "AQAB"
    }
]

kakao_public_keys = [
    {
        "kid": "3f96980381e451efad0d2ddd30e3d3",
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": "q8zZ0b_MNaLd6Ny8wd4cjFomilLfFIZcmhNSc1ttx_oQdJJZt5CDHB8WWwPGBUDUyY8AmfglS9Y1qA0_fxxs-ZUWdt45jSbUxghKNYgEwSutfM5sROh3srm5TiLW4YfOvKytGW1r9TQEdLe98ork8-rNRYPybRI3SKoqpci1m1QOcvUg4xEYRvbZIWku24DNMSeheytKUz6Ni4kKOVkzfGN11rUj1IrlRR-LNA9V9ZYmeoywy3k066rD5TaZHor5bM5gIzt1B4FmUuFITpXKGQZS5Hn_Ck8Bgc8kLWGAU8TzmOzLeROosqKE0eZJ4ESLMImTb2XSEZuN1wFyL0VtJw",
        "e": "AQAB"
    },
    {
        "kid": "9f252dadd5f233f93d2fa528d12fea",
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": "qGWf6RVzV2pM8YqJ6by5exoixIlTvdXDfYj2v7E6xkoYmesAjp_1IYL7rzhpUYqIkWX0P4wOwAsg-Ud8PcMHggfwUNPOcqgSk1hAIHr63zSlG8xatQb17q9LrWny2HWkUVEU30PxxHsLcuzmfhbRx8kOrNfJEirIuqSyWF_OBHeEgBgYjydd_c8vPo7IiH-pijZn4ZouPsEg7wtdIX3-0ZcXXDbFkaDaqClfqmVCLNBhg3DKYDQOoyWXrpFKUXUFuk2FTCqWaQJ0GniO4p_ppkYIf4zhlwUYfXZEhm8cBo6H2EgukntDbTgnoha8kNunTPekxWTDhE5wGAt6YpT4Yw",
        "e": "AQAB"
    }
]

google_jwkset = jwk.JWKSet()
for key in google_public_keys:
    google_jwkset.add(jwk.JWK(**key))

kakao_jwkset = jwk.JWKSet()
for key in kakao_public_keys:
    kakao_jwkset.add(jwk.JWK(**key))


class AuthParser(HTTPBearer):
    def __init__(self):
        super().__init__()

    async def __call__(self, request: Request):
        try:
            auth_header = request.headers.get("Authorization")

            if os.getenv("ENV_MODE") == "test":
                request.state.auth = {
                    "sub": auth_header.split(" ")[1],
                }
            else:
                auth_type, auth_token = auth_header.split(" ")
                if auth_type == "Bearer":
                    payload_encoded = auth_token.split(".")[1]
                    payload_byte = common.base64url_decode(payload_encoded)
                    payload = json.loads(payload_byte)

                    if payload.get('iss') == "https://accounts.google.com" or payload["iss"] == "accounts.google.com":
                        kid = payload["kid"]
                        key = google_jwkset.get_key(kid)
                    elif payload.get('iss') == "https://kauth.kakao.com":
                        kid = payload["kid"]
                        key = kakao_jwkset.get_key(kid)

                    token = jwt.JWT(key=key, jwt=auth_token)
                    payload: dict = json.loads(token.claims)

                    if payload.get("iss") == "https://accounts.google.com" or payload.get("iss") == "accounts.google.com":
                        if payload.get("aud") != os.getenv("GOOGLE_CLIENT_ID"):
                            raise HTTPException(
                                status_code=401, detail="Token invalid")
                    elif payload.get("iss") == "https://kauth.kakao.com":
                        if payload.get("aud") != os.getenv("KAKAO_CLIENT_ID"):
                            raise HTTPException(
                                status_code=401, detail="Token invalid")

                    request.state.auth = payload

        except Exception as e:
            request.state.auth = None
