import hashlib
import hmac
import random

# Signature: "xhoff" parametr
# Method: HMAC SHA-1

"""
Request screenshot from fiddler - https://i.ibb.co/SrgBXWP/2023-06-27-205144412.png
Thanks frida, much easier 

Original encoding in APK, Java:
private synchronized String getXHOFFkeyForAPI2(String str, String str2, String str3) {
    String str4;
    str4 = "";
    int random = GlobalVar.getRandom();  // random int (1-8888) + 1111
    if (str3 == null || str3.isEmpty()) {
        str3 = "";
    }
    String str5 = "" + str + GlobalVar.XHOFF_SECRET.toStrlng() + str2 + str3;  // salt - 2Dro0I1d7an
    try {
        StringBuilder sb = new StringBuilder();
        sb.append(calculateRFC2104HMAC(str5, "" + random));  // calculate hmac
        sb.append(":");
        sb.append(random);  // hash:random
        str4 = sb.toString();
    } catch (InvalidKeyException e2) {
        e2.printStackTrace();
    } catch (NoSuchAlgorithmException e3) {
        e3.printStackTrace();
    } catch (SignatureException e4) {
        e4.printStackTrace();
    }
    return str4;
}
"""


def encode(secret_key: str, string: str):
    mac = hmac.new(secret_key.encode(), msg=bytes(string.encode()), digestmod=hashlib.sha1)
    return mac.hexdigest()


def SignRequest(
    location: int = 3528,
    device_id: str = "468c47e501a2448c",
    salt: str = "2Dro0I1d7an"
):
    random_int = random.randint(0, 8888) + 1111
    to_encode = f"{device_id}{salt}location{location}"
    encoded = encode(secret_key=str(random_int), string=to_encode)
    xhoff = f"{encoded}:{random_int}"
    return xhoff


print("Sign:", SignRequest())
# output: 5de26927a39720c22284a9d2bcdf772d5818dbc1:6416
# always random
