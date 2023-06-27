import hashlib
import base64

# Signature: "Authorization" header
# Method: Base64(<email>:SHA256(<salt><password><email>))

"""
Request data screenshot - https://i.ibb.co/t3DRkbJ/2023-06-27-153141956.png
Not really hard, just boring to convert Java code to Python. Thanks ChatGPT and google.
I spent ~2 hours doing it.
BTW, i dont fully undersntand how salt generation works, but it is always different.

Original encoding in APK, Java:
private b(Integer num, char c10, char c11) {
    this.f11049a = num;
    this.f11050b = c10;
    this.f11051c = c11;
}

public static String a(String str, String str2) {
    // str - email, str2 - password
    b bVar;
    if (str2 == null) {  // no password
        return null;
    }
    String lowerCase = str.toLowerCase();  //  lower email
    char[] cArr = new char[256];  // list with chars of long string
    int i10 = 0;
    "53534a377969656f6b6d5678584b7a70714752710cc3cfee33203af762af7fc4e04a826d3f14834dcc3e7165bcad2282cf081a9d707f762a710df73b4d466e9dc2e9bd420ef656c53534a377969656f6b6d5678584b7a70714752710cc3cfee33203af762af7fc4e04a826d3f14834dcc3e7165bcad2282cf081a9d707f762a7".getChars(0, 256, cArr, 0);
    String str3 = str2 + lowerCase;  // password + lower email
    int length = str3.length();  // len(str3)
    char[] cArr2 = new char[length];  // list with chars of str3
    str3.getChars(0, length, cArr2, 0);
    HashSet hashSet = new HashSet();
    ArrayList arrayList = new ArrayList();
    int i11 = 0;
    while (i11 < length) {  // for char in str3
        char c10 = cArr2[i11];  // select char by index
        if (hashSet.contains(Integer.valueOf(c10))) {  // if ord(c10) in hashSet | only uniq chars in hashSet
            i11++;
            if (Character.isHighSurrogate((char) c10)) {  // if utf-8 char
                i11++;
            }
        } else {
            hashSet.add(Integer.valueOf(c10));  // add ord(c10) to hashSet
            char c11 = (char) c10;  // c11 = c10
            if (Character.isHighSurrogate(c11)) {  // if utf-8 char
                int i12 = i11 + 1;  // idk
                char c12 = (char) cArr2[i12];  // select char from cArr2
                i11 = i12 + 1;
                arrayList.add(new b(Integer.valueOf(Character.toCodePoint(c11, c12) % 256), c11, c12));
            } else {
                cArr[c10 % 256] = c11;  // idk
            }
        }
    }
    
    // idk, salt gen
    int size = 256 + arrayList.size();
    char[] cArr3 = new char[size];
    int i13 = 0;
    while (i10 < size) {
        Iterator it = arrayList.iterator();
        while (true) {
            if (!it.hasNext()) {
                bVar = null;
                break;
            }
            bVar = (b) it.next();
            if (bVar.f11049a.equals(Integer.valueOf(i10))) {
                break;
            }
        }
        if (bVar != null) {
            cArr3[i10] = bVar.f11050b;
            i10++;
            cArr3[i10] = bVar.f11051c;
            i13++;
        } else {
            // only this part of code will be executed
            cArr3[i10] = cArr[i10 - i13];
        }
        i10++;
    }
    return b(String.valueOf(cArr3) + str2 + lowerCase);  // returns hash of salt + password + lower email
}

public static final String b(String str) {  
    // gen sha256 hash
    try {
        byte[] digest = MessageDigest.getInstance(Constants.SHA256).digest(str.getBytes(Constants.ENCODING));
        StringBuffer stringBuffer = new StringBuffer();
        for (byte b10 : digest) {
            String hexString = Integer.toHexString(b10 & 255);
            if (hexString.length() == 1) {
                stringBuffer.append('0');
            }
            stringBuffer.append(hexString);
        }
        return stringBuffer.toString();  // hexdigest() in python
    } catch (Exception e10) {
        f.c(e10);  // save error log
        return null;
    }
}
"""


def to_code_point(high_surrogate, low_surrogate):
    high = ord(high_surrogate)
    low = ord(low_surrogate)
    code_point = ((high - 0xD800) << 10) + (low - 0xDC00) + 0x10000
    return hex(code_point)


class B:
    def __init__(self, num: int, c10: str, c11: str):
        self.f11049a = num
        self.f11050b = c10
        self.f11051c = c11


def a(login: str, password: str):
    b_var = B
    if password is None:
        return None

    lower_case: str = login.lower()  # email@gmail.com"
    i10: int = 0

    s = "53534a377969656f6b6d5678584b7a70714752710cc3cfee33203af762af7fc4e04a826d3f14834dcc3e7165bcad2282cf081a9d707f762a710df73b4d466e9dc2e9bd420ef656c53534a377969656f6b6d5678584b7a70714752710cc3cfee33203af762af7fc4e04a826d3f14834dcc3e7165bcad2282cf081a9d707f762a7"
    c_arr = (list(s[:len(s)]))  # ['5', '3', '5', '3', '4', 'a'..]

    str3: str = password + lower_case  # passwordemail@gmail.com
    length: int = len(str3)  # 23

    c_arr2 = (list(str3))  # ['p', 'a', 's', 's', 'w', 'o', 'r', 'd', 'e', 'm'..]

    hash_set = set()
    array_list = []

    i11: int = 0
    while i11 < length:
        c10: str = c_arr2[i11]
        if ord(c10) in hash_set:
            i11 += 1
            if 0xD800 <= ord(c10) <= 0xDBFF:
                i11 += 1
        else:
            hash_set.add(ord(c10))
            c11: str = c10
            if 0xD800 <= ord(c11) <= 0xDBFF:
                i12: int = i11 + 1
                c12: str = c_arr2[i12]
                array_list.append(B(ord(to_code_point(c11, c12) % 256), c11, c12))
            else:
                c_arr[ord(c10) % 256] = c11  # 52 - 4

    size: int = 256 + len(array_list)
    c_arr3: list = [None] * size
    i13: int = 0

    while i10 < size:
        it = iter(array_list)
        while True:
            try:
                _ = next(it)
                b_var = b_var(_)  # error here, but this code won't ever be executed
                if b_var.f11049a == i10:
                    break

            except StopIteration:
                b_var = None
                break

        if b_var is not None:
            c_arr3[i10] = b_var.f11050b
            i10 += 1
            c_arr3[i10] = b_var.f11051c
            i13 += 1
        else:
            c_arr3[i10] = c_arr[i10 - i13]
        i10 += 1

    return b("".join(c_arr3) + password + lower_case)


def b(string: str):
    digest: bytes = hashlib.sha256(string.encode()).digest()
    string_buffer: list = []
    # better to use return digest.hexdigest(), but i converted fully copy  of source code

    for b10 in digest:
        hex_string: str = ''.join('{:02x}'.format(b10 & 255))

        if len(hex_string) == 1:
            string_buffer.append('0')
        string_buffer.append(hex_string)

    return "".join(string_buffer)


def SignRequest(email: str = "email@gmail.com", password: str = "password"):
    hash_strgin = a(email, password)
    auth_header = base64.b64encode(f"{email}:{hash_strgin}".encode()).decode()
    return {"Authorization": f"Basic {auth_header}"}


print("Sign: ", SignRequest())
# output: ZW1haWxAZ21haWwuY29tOmI4MDU4MjM0OTVjZDhiMjMxM2JjMTA4ZjU3YzQzYmUzZDJmODI0YjY4ZWQzNzAzN2NjMDZkNDUwYjA1Yjk0NjU=
# the same sha256 hash
