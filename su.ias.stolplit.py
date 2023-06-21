import base64
import hashlib
import datetime
import requests

# Signature: "md5" and "expires" headers
# Method: Base64(MD5)

"""
Request screenshot from fiddler - https://i.ibb.co/r2C3R7N/2023-06-21-131230168.png, https://i.ibb.co/cvFBBYc/image.png

Original encoding in APK, cotlin: 

{
    try {
        SimpleDateFormat simpleDateFormat = dateFormat;
        String date_server = deviceIp.getDate_server();
        Intrinsics.checkNotNull(date_server);
        Date parse = simpleDateFormat.parse(date_server);  // parse unix time from "2023-06-21T11:48:31+03:00"
        Intrinsics.checkNotNull(parse);
        String valueOf = String.valueOf((parse.getTime() / ((long) 1000)) + ((long) 10800));  // calculate timestamp
        this.settingsRepository.setExpires(str, valueOf);
        String str2 = valueOf + str + ((Object) deviceIp.getIp()) + ' ' + BuildConfig.SECRET_HASH_KEY;  // calculate md5 hash f"{timestamp}{path}{ip} {salt}"
        MessageDigest instance = MessageDigest.getInstance("MD5");
        byte[] bytes = str2.getBytes(Charsets.UTF_8);
        Intrinsics.checkNotNullExpressionValue(bytes, "this as java.lang.String).getBytes(charset)");
        instance.update(bytes);
        String encodeToString = Base64.encodeToString(instance.digest(), 16);  // encode hash bytes to base64
        Intrinsics.checkNotNullExpressionValue(encodeToString, "encodeToString(messageDigest, 16)");
        this.settingsRepository.setHash(....);  // set value to shared prefs
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
    } catch (Exception e2) {
        e2.printStackTrace();
    }
}

"""


def StringToDate(date_str: str) -> int:  # 1687337311000
    dt_obj = datetime.datetime.fromisoformat(date_str)
    timestamp_ms = int(dt_obj.timestamp() + 10800)  # 10800 sec is 3 hours. Hash is alive for 3 hours
    return timestamp_ms


def encode(string: str) -> bytes:
    hashed_value = hashlib.md5(string.encode())
    return hashed_value.digest()


def SignRequest(path: str = "/s/api/v8/region/1/authorization/", salt: str = "EUdq8qfSj1EB0QLntgY2"):
    replacing = {
        "=": "",
        "+": "-",
        "/": "_"
    }

    response = requests.get("https://www.stolplit.ru/get_ip/").json()
    timestamp = StringToDate(date_str=response["date_server"])
    signing_ip = response["ip"]

    string = f"{timestamp}{path}{signing_ip} {salt}"
    hashed = hashlib.md5(string.encode()).digest()
    encoded = base64.b64encode(hashed).decode()
    for key, value in replacing.items():
        encoded = encoded.replace(key, value)
    data = {"md5": encoded, "expires": timestamp}
    return data


print(SignRequest())
# output: {'md5': 'wq9ZJS7Ttf4IMn3h6NKifQ', 'expires': 1687353847}
# depends on date and ip, always different
