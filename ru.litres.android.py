import hashlib
import datetime


# Signature: "sha" value in post data
# Method: SHA-256

"""
Request data screenshot - https://i.ibb.co/mtZ7Y1Y/2023-06-21-163434133.png 

Original encoding in APK, cotlin: 

String _dateToString = _dateToString(currentTime); // get time in format %Y-%m-%dT%H:%M:%S%z
StringBuilder d = h.d(_dateToString);  // create new StringVuilder
d.append(f37900t.isSchool() ? "2vHzgxMKjz0cs2CVR2SdF9RGqbmYmuCOY71KATei" : "AsAAfdV000-1kksn6591x:[}A{}<><DO#Brn`BnB6E`^s\"ivP:RY'4|v\"h/r^]");  // different salt for school and not school apps
HashMap d10 = androidx.lifecycle.h.d("time", _dateToString, "sha", CryptoUtils.getSHA256(d.toString()))  // add "time" and "sha" to hashmap
"""


def GetTime() -> str:
    current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
    time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S%z').replace("+0300", "+03:00")
    return time_str


def encode(string: str) -> str:
    hashed_value = hashlib.sha256(string.encode())
    return hashed_value.hexdigest()


def SignRequest(is_school: bool = False):
    keys = {
        True: "2vHzgxMKjz0cs2CVR2SdF9RGqbmYmuCOY71KATei",
        False: "AsAAfdV000-1kksn6591x:[}A{}<><DO#Brn`BnB6E`^s\"ivP:RY'4|v\"h/r^]"
    }

    time_now = GetTime()
    salt = keys[is_school]
    sha_string = encode(f"{time_now}{salt}")
    return sha_string


print("Sign:", SignRequest())
# otput: 2a0ce5534c891061a75a2fe314ea0468983ed6cbe499f2c6b893de377c4770ff
# # depends on date, always different
