import hashlib
import hmac

# Signature: "x-request-sign" header
# Method: HMAC SHA-512

"""
Request screenshot from fiddler - https://i.ibb.co/KD4n6ZD/Fiddler-l-Tmz-Csty-ZE.png
Jadx + Frida. Log will be here soon
"""


import hashlib
import hmac
import json


MASTER_KEY = "D3SVT7pbXn8bnA7T"


class MagnitSigner:
    def __init__(self, device_platform: str, app_version: str, device_id: str, phone: str, token: str = ""):
        self.__device_platform = device_platform
        self.__app_version = app_version
        self.__device_id = device_id
        self.__phone = phone
        self.__token = token
        self.__hmac_key = self.generate_hmac_key()

    def generate_hmac_key(self) -> bytes:
        key = MASTER_KEY.encode()

        for data in [self.__device_platform, self.__app_version, self.__device_id, self.__phone]:
            key = hmac.new(key, data.lower().encode(), hashlib.sha512).digest()

        return key

    def update_token(self, token: str) -> None:
        self.__token = token

    def sign(self, path: str, payload: dict = None) -> str:
        path_key = hmac.new(
            key=self.__hmac_key,
            msg=path.lower().encode(),
            digestmod=hashlib.sha512
        ).digest()

        token_key = hmac.new(
            key=path_key,
            msg=self.__token.lower().encode(),  # token!
            digestmod=hashlib.sha512
        ).digest()

        if not payload:  # GET request
            return token_key.hex()

        # POST / PATCH / PUT..
        stringified_payload = json.dumps(payload, separators=(",", ":"))
        hashed_payload = hashlib.md5(stringified_payload.encode()).hexdigest()

        payload_key = hmac.new(
            key=token_key,
            msg=hashed_payload.encode(),
            digestmod=hashlib.sha512
        ).hexdigest()

        return payload_key


if __name__ == "__main__":
    mc = MagnitSigner(
        device_platform="android",
        app_version="6.112.1",
        device_id="b0ec3446-6f81-3be3-b29b-8a01b7b7e283",
        phone="79698266375",
    )

    print(mc.sign(
        path="/v1/auth/otp",
        payload={"aud": "loyalty-mobile", "phone": "79698266375", "captcha-token": "captcha-token", "forceSMS": True}
    ))


