import hashlib
import hmac

# Signature: "x-request-sign" header
# Method: HMAC SHA-512

"""
Request screenshot from fiddler - https://i.ibb.co/KD4n6ZD/Fiddler-l-Tmz-Csty-ZE.png
Again no Jadx used, only frida. Best tool ever

[*] MessageDigest.getInstance (1) called
algorithm: MD5
[*] MessageDigest.digest called
algorithm: MD5
input: {"aud":"loyalty-mobile","phone":"79956341405","captcha-token":"captcha-token","forceSMS":true}
output: d66c73671b4d1a3b659b57d2010ee0ba
[*] secretKeySpec.init called
algorithm: HmacSHA512    
keyH: 2e26d2f0588a7147be4a37573b65135eb2edf5ca747a10c02f1b864dad962921e661db2f7551d14e35cd513f785716a4ea4eb8494e41b27ab84d12b834d24bab
[*] Mac.init called
algorithm: HmacSHA512   
keyH: 2e26d2f0588a7147be4a37573..
[*] Mac.doFinal called
algorithm: HmacSHA512
input: d66c73671b4d1a3b659b57d2010ee0ba
outputH: 63bc1ede4e60d0cb64e39d0b244a688ae669c9a2af877ed4d6e61b72ee93373feab52b979bb3b97b01ff333cbbfa86131183eed2f7fc15a34cf79434e86d3f5a
"""


def encode_md5(string: str):
    return hashlib.md5(string.encode()).hexdigest()


def encode_sha512(key: str, string: str):
    secret_key_bytes = bytes.fromhex(key)
    mac = hmac.new(secret_key_bytes, msg=string.encode(), digestmod=hashlib.sha512)
    return mac.hexdigest()


def SignRequest(
        aud: str = "loyalty-mobile",
        phone: str = "79956341405",
        captcha_token: str = "captcha-token",
        force_sms: bool = True,
        key_hex: str = "2e26d2f0588a7147be4a37573b65135eb2edf5ca747a10c02f1b864dad962921e661db2f7551d14e35cd513f785716a4ea4eb8494e41b27ab84d12b834d24bab"
):
    to_encode = {
        "aud": aud,
        "phone": phone,
        "captcha-token": captcha_token,
        "forceSMS": force_sms
    }

    to_encode = str(to_encode).replace("\'", "\"").replace(" ", "").replace("True", "true").replace("False", "false")
    encoded_md5 = encode_md5(to_encode)
    encoded_sha = encode_sha512(key=key_hex, string=encoded_md5)
    print(encoded_sha)


SignRequest()
# output: 63bc1ede4e60d0cb64e39d0b244a688ae669c9a2af877ed4d6e61b72ee93373feab52b979bb3b97b01ff333cbbfa86131183eed2f7fc15a34cf79434e86d3f5a
# it is the same sha512 hash as header 1 screenshot
