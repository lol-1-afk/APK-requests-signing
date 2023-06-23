import hashlib

# Signature: "hash" value in post data
# Method: MD5

"""
Request data screenshot - https://i.ibb.co/XyzWGLw/2023-06-23-144127603.png
So, it was reall hard for me. Salt from strings.xml is something new. 

Original encoding in APK, Kotlin:
{
    String str5;  // string for future login value
    n.g(str, "login");  // str - login (email (email@gmail.com) or phone (79101231231))
    n.g(str2, "password");  // str2 - password
    String b10 = this.stringsProvider.b(R.string.login_secret_key, new Object[0]); // get secret key (salt)
    // stringsProvider.b returns string from strings.xml by its name. 
    // R.string.login_secret_key - name of srting that stores salt - login_secret_key
    // <string name="login_secret_key">F9gfSpP94g3rtVBfd</string> here is salt. I decompiled apk to get it
    
    if (kotlin.text.w.J(str, '@', false, 2, null)) {  
        // if login contains "@" = login is email
        str5 = str.toLowerCase();  // str5 = lower value of email. Ex: EMAIL@GMAIL.COM -> email@gmail.com
        
    } else {
        // if login doesnt contain "@" = login is phone number
        StringBuilder sb2 = new StringBuilder();  // new sb
        int length = str.length();  // length of phone number
        for (int i10 = 0; i10 < length; i10++) { 
            // for index in range(length)
            char charAt = str.charAt(i10);
            // select char from phone number by index
            if (Character.isDigit(charAt)) {
                // if char is digit (1-9): append to sb
                sb2.append(charAt);
            }
        }
        String sb3 = sb2.toString(); // convert sb to single string
        str5 = y.P0(sb3, 10); // y.P0 returns substring of last 10 chars. Ex:  79101231231 -> 9101231231 
    }
    // some code idk. But we need only a(n.n(str5, b10)). 
    // n.n joins login with salt. Ex: n(9101231231, F9gfSpP94g3rtVBfd) -> 9101231231F9gfSpP94g3rtVBfd
    // n(email@gmail.com, F9gfSpP94g3rtVBfd) -> email@gmail.comF9gfSpP94g3rtVBfd
    // 'a' returns hexed md5 bytes of n.n(..). Here we go!
    w k10 = this.authTokenRetriever.getToken().k(new i(str, str2, str3, str4, kj.d.f16327b.a().a(n.n(str5, b10))){...}
}
"""


def encode(string: str) -> str:
    hashed_value = hashlib.md5(string.encode())
    return hashed_value.hexdigest()


def GetLength(num1, num2):
    return num2 if num1 > num2 else num1


def GetSubstring(phone: str, numbers: int):
    if numbers >= 0:
        length = len(phone)
        sub_string = phone[length - GetLength(numbers, length):]
        return sub_string
    raise ValueError("Requested character count " + str(numbers) + " is less than zero.")


def SignRequest(login: str = "79101231231", salt: str = "F9gfSpP94g3rtVBfd"):
    if "@" in login:
        login = login.lower()
    else:
        login = GetSubstring(login, 10)
    hashed = encode(f"{login}{salt}")
    return hashed


print("Sign:", SignRequest())
# output: d98686ff5c90e89004732309984b787b
# always different, depens on login value
