import hashlib
import hmac

# Signature: "X-Request-Sign" header
# Method: HMAC SHA-512

"""
Request screenshot from fiddler - https://i.ibb.co/JcPNQ7B/2023-06-20-225335050.png
X-Device-ID header - device_uuid value
X-App-Version header - version value
X-Device-Platform header - plarform value

Original encoding in APK, cotlin: 
{
            this.b.a();
            String a3 = gk2.a(this.a.a, "DEVICE_UUID"); // device_uuid from shared prefs
            if (a3 != null) {
                str3 = a3;
            }
            byte[] bytes = "?wAyIaDzG1MjYxIE".getBytes(qx.a); // salt
            ds2.g(bytes, "this as java.lang.String).getBytes(charset)");
            byte[] e = l72.e(l72.e(l72.e(l72.e(bytes, "Android"), str3), "0.4.0"), str2);  // all that wee need
            vu0 vu0 = vu0.a;
            StringBuilder sb2 = new StringBuilder();
            sb2.append((CharSequence) "");
            int i2 = 0;
            for (byte b : e) {  // now calculating hex
                i2++;
                if (i2 > 1) {
                    sb2.append((CharSequence) "");
                }
                sb2.append(vu0 != null ? (CharSequence) vu0.invoke(Byte.valueOf(b)) : String.valueOf((int) b));
            }
            sb2.append((CharSequence) "");
            String sb3 = sb2.toString();
            ds2.g(sb3, "joinTo(StringBuilder(), …ed, transform).toString()"); // joining to single string
            aVar2.a("X-Request-Sign", sb3);  // set header
        }


"""


def encode(bytes_arrayr: bytes, string: str) -> bytes:
    secret_key = bytes(bytes_arrayr)
    mac = hmac.new(secret_key, msg=bytes(string.lower().encode()), digestmod=hashlib.sha512)
    return mac.digest()


def SignRequest(
        salt: str = "?wAyIaDzG1MjYxIE",
        device_uuid: str = "b8a8ba92-6e5e-4295-bf34-a3a5bcd0432c",
        version: str = "0.4.0",
        phone: str = "79101231231",
        platform: str = "Android"
                ) -> str:

    platform_salt_ps = encode(salt.encode(), platform)  # encode(salt.encode(), platform)
    ps_uuid_pu = encode(platform_salt_ps, device_uuid)  # encode(encode(salt.encode(), platform), device_uuid)
    pu_version_pv = encode(ps_uuid_pu, version)  # encode(encode(encode(salt.encode(), platform), device_uuid), version)
    pv_phone_pp = encode(pu_version_pv, phone)  # encode(encode(encode(encode(salt.encode(), platform), device_uuid), version), phone)
    return pv_phone_pp.hex()


print("Sign:", SignRequest())
# output: 96ae8eb6d8714421adbd15ba4ffb77157c62c86bf1f9a8a638c34cc9e38fc1e434c80cc32f46dca3e948d9b3fc991c2b2c6a9ebfaae91849ad396896a5ea5ea9
# it is the same sha512 hash as X-Request-Sign in screenshot
