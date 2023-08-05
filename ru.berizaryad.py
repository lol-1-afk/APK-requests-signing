import hashlib
import hmac

# Signature: "signature" header
# Method: HMAC SHA-256

"""
Login Request screenshot from fiddler - https://i.ibb.co/j58xY67/Fiddler-GJm4gm-Sv0h.png
Confirm Request screenshot from fiddler - https://i.ibb.co/BrPj1L5/Fiddler-UT1-Bg-T150-A.png
Jadx wasnt used, only frida. Best tool ever
Hash is hust post body encoded with secet key
Frida log:

[*] secretKeySpec.init called
algorithm: HmacSHA256
key: 9e02b971-344c-4b94-bbc6-cc7fab18429f
keyH: 39653032623937312d333434632d346239342d626263362d636337666162313834323966
[*] Mac.init called
algorithm: HmacSHA256
key: 9e02b971-344c-4b94-bbc6-cc7fab18429f
keyH: 39653032623937312d3334346..
[*] Mac.doFinal called
algorithm: HmacSHA256
input: {"app_version":"5.2.8","os_version":"28","phone":"79101231231","platform":"Android","udid":"44ae56daf7a252ff"}
outputH: 20bbb37ea19e7a336f5ca70a086b04443bbb0148fd20b8c2f7371d9efc4308d2
"""


def encode(secret_key: str, string: str):
    mac = hmac.new(key=secret_key.encode(), msg=string.encode(), digestmod=hashlib.sha256)
    return mac.hexdigest()


def SignLoginRequest(
        app_version: str = "5.2.8",
        os_version: str = "28",
        phone: str = "79101231231",
        platform: str = "Android",
        udid: str = "44ae56daf7a252ff",
        key: str = "9e02b971-344c-4b94-bbc6-cc7fab18429f"
):
    to_encode = {
        "app_version": app_version,
        "os_version": os_version,
        "phone": phone,
        "platform": platform,
        "udid": udid
    }

    to_encode = str(to_encode).replace("\'", "\"").replace(" ", "")
    return encode(key, to_encode)


def SignConfirmRequest(
        app_version: str = "5.2.8",
        code: str = "1111",
        os_version: str = "28",
        phone: str = "79101231231",
        platform: str = "Android",
        udid: str = "44ae56daf7a252ff",
        key: str = "9e02b971-344c-4b94-bbc6-cc7fab18429f"
):
    to_encode = {
        "app_version": app_version,
        "code": code,
        "os_version": os_version,
        "phone": phone,
        "platform": platform,
        "udid": udid
    }

    to_encode = str(to_encode).replace("\'", "\"").replace(" ", "")
    return encode(key, to_encode)


print("Sign:", SignLoginRequest())
# output: 20bbb37ea19e7a336f5ca70a086b04443bbb0148fd20b8c2f7371d9efc4308d2
# it is the same sha256 hash as signature in 1 screenshot

print("Sign:", SignConfirmRequest())
# output: e78ea146369f1b32503a030e806002f1494c99e5d2b91953fb406bbdc76c14f0
# it is the same sha256 hash as signature in 2 screenshot
