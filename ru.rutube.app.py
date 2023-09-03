import hashlib
import requests

# Signature: "captcha" value in post data / params
# Method: SHA-256

"""
Request screenshot from fiddler - https://i.ibb.co/hWLmR02/Fiddler-Ay-ZLt-QMbj-F.png

Original encoding in APK, Java: 

java.lang.String r5 = (java.lang.String) r5
java.lang.String r1 = "Va1sYMmXX0LIaPLNyxVs74bvmsut1IUM12xbwu93" // salt
java.lang.String r5 = androidx.constraintlayout.widget.a.a(r1, r5) // time
java.lang.String r1 = "SHA-256" // method
java.security.MessageDigest r1 = java.security.MessageDigest.getInstance(r1)
java.nio.charset.Charset r2 = kotlin.text.Charsets.UTF_8
byte[] r5 = r5.getBytes(r2)
java.lang.String r2 = "this as java.lang.String).getBytes(charset)"
kotlin.jvm.internal.Intrinsics.checkNotNullExpressionValue(r5, r2)
byte[] r5 = r1.digest(r5) // get hash from salt + time
java.lang.String r1 = "getInstance(HASH_ALGORIT…chaMessage.toByteArray())"
kotlin.jvm.internal.Intrinsics.checkNotNullExpressionValue(r5, r1)
r0.getClass()
ru.rutube.captcha.CaptchaGeneratorImpl$toHexString$1 r0 = ru.rutube.captcha.CaptchaGeneratorImpl$toHexString$1.INSTANCE
r1 = 30
java.lang.String r2 = ""
java.lang.String r5 = kotlin.collections.ArraysKt.o(r5, r2, r0, r1)
java.lang.String r0 = "kc" // prefix
java.lang.String r5 = androidx.constraintlayout.widget.a.a(r0, r5) // prefix + hash
return r5

Frida log:
[*] MessageDigest.digest called
algorithm: SHA-256
input: Va1sYMmXX0LIaPLNyxVs74bvmsut1IUM12xbwu932023-08-31T18:05:11.069883
output: 00aadd4da733d945e8a12cb0741b06e31d241ba7096a4e6522e32af306009312

"""


def SignRequest(salt: str = "Va1sYMmXX0LIaPLNyxVs74bvmsut1IUM12xbwu93", prefix: str = "kc"):
    timestamp = requests.get("https://rutube.ru/multipass/api/v3/accounts/timestamp?client=android").json()["datetime"]
    sign = prefix + hashlib.sha256(f"{salt}{timestamp}".encode()).hexdigest()
    return sign


print(SignRequest())