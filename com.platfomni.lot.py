import hashlib
import hmac
import json

# Signature: "token" header
# Method: Upper(HMAC SHA-256)

"""
Request screenshot from fiddler - https://i.ibb.co/yY6sxyv/2023-06-26-144137300.png
Frida log screenshot - https://i.ibb.co/L0L5XCT/2023-06-26-144234826.png

Unfortunately, i dont know how it works and i dont have source code of "token" generation
But i used frida-server and found secret key - "dgCHIXFPx15nbjIceRT2Btcpjrfj2cKo8wbL9Q06iaUArCUqgEHAbkEDUK0941fn"
So, i can make generation myself
"""


def encode(key: str, string: str) -> str:
    secret_key = key.encode()
    mac = hmac.new(secret_key, msg=bytes(string.lower().encode()), digestmod=hashlib.sha256)
    return mac.hexdigest()


def GetParams(url: str) -> dict:
    if "?" not in url:  # no params
        return {}

    params = url.split('?')[1]
    param_list = params.split('&')
    param_dict = {}

    for param in param_list:
        key, value = param.split('=')
        param_dict[key] = value

    return param_dict


def SignRequest(
        post_data: dict,
        url: str = "https://api.lekopttorg.ru/v1/auth",
        key: str = "dgCHIXFPx15nbjIceRT2Btcpjrfj2cKo8wbL9Q06iaUArCUqgEHAbkEDUK0941fn"
):
    gen_data = {}
    params = GetParams(url=url)
    gen_data.update(params)
    gen_data.update(post_data)

    json_string = json.dumps(gen_data)
    formatted_string = json_string.replace(": ", ":").replace(", ", ",")

    token = encode(key=key, string=formatted_string)
    return token.upper()


print("Sign: ", SignRequest(post_data={"phone":"+7 (910) 123-12-31","password":"password123","device_token":"e5555cdf-7715-4976-a1d4-27b7b29a8172"}))
# output: A8121F14C731F58BC7DC36E08A1B14C716D0A26D94F75A6E15F2C5F48F1337BD
# the same hash, depends on post data and params
