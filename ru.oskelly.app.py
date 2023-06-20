import hashlib

# Signature: "password" value in post data
# Method: HMAC SHA-512

"""
Request screenshot from fiddler - https://i.ibb.co/MNLkXN8/2023-06-20-231242642.png

Original encoding in APK, cotlin: 
{
    String str = dVar.f27026a;  // email value
    String str2 = dVar.f27027b;  // not hashed password value
    m.e(str, "email");
    m.e(str2, SettingsReader.PASSWORD);
    MessageDigest instance = MessageDigest.getInstance("SHA-512");
    byte[] bytes = i2.a(str2, "{", str, "}").getBytes(ln.a.f16187b); // password{email}
    m.d(bytes, "this as java.lang.String).getBytes(charset)");
    byte[] digest = instance.digest(bytes);
    StringBuilder sb2 = new StringBuilder();
    m.d(digest, "bytes");
    int length = digest.length;
    int i11 = 0;
    while (i11 < length) { // calculate hex
        byte b11 = digest[i11];
        i11++;
        String hexString = Integer.toHexString(b11 & 255);
        if (hexString.length() == 1) {
            sb2.append('0');
        }
        sb2.append(hexString);
    }
    String sb3 = sb2.toString();
    m.d(sb3, "hexString.toString()");
    c cVar = this.f16304a;
    Objects.requireNonNull(cVar);
    gl.i<z<h0>> logIn = cVar.f16299a.logIn(str, sb3);
    es.a aVar = es.a.B;
    Objects.requireNonNull(logIn);
    y yVar = new y(new v(logIn, aVar), new a());
    s sVar = new s(this, str, sb3);
    d<? super Throwable> dVar2 = nl.a.f18035d;
    ll.a aVar2 = nl.a.f18034c;
    return yVar.m(sVar, dVar2, aVar2, aVar2);
}
"""


def encode(string: str) -> str:
    hashed_value = hashlib.sha512(string.encode())
    return hashed_value.hexdigest()


def SignRequest(email: str = "bluesky@bk.ru", password: str = "9055760090"):
    hashed_password = encode(password + "{" + email + "}")
    return hashed_password


print("Sign:", SignRequest())
# output: da15307a1d923cbcc569f17aa11ffd0b9d00b7c101ff73a2bb1dd7b09bfc417eb8cb08fa4929913752160e67d8e4a8338dfa7e49bd08155176ac317d578a0d47
# it is the same sha512 hash as password in screenshot
