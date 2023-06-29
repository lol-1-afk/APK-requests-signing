import hashlib

# Signature: "sign" value in post data
# Method: MD5

"""
Request screenshot from fiddler - https://i.ibb.co/5BQNvXs/2023-06-29-133211814.png
Easiest one

Original encoding in APK, Java:
public r(String str, String str2, String str3) {
    // f0.f27776a.a - returns sign
    super(h0.i(q.a("sip", str), q.a("pass", str2), q.a("sign", f0.f27776a.a(str)), q.a("device_uniqid", str3)));
    o.f(str, "number");
    o.f(str2, "password");
    o.f(str3, "installationId");
}

public final String a(String str) {
    // q.i - returns hash of sip + "DS5ZSWTwxf" 
    o.f(str, "number");
    return q.i(str + "DS5ZSWTwxf");
}
"""


def encode(string: str):
    hashed = hashlib.md5(string.encode()).hexdigest()
    return hashed


def SignRequest(sip: int = 121212, salt: str = "DS5ZSWTwxf"):
    sign = encode(str(sip) + salt)
    return sign


print("Sign: ", SignRequest())
# Ouput: 976c09b50ad89e3e7af2bc45c4c91467
# The same MD5 hash, depends on sip
