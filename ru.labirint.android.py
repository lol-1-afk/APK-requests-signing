import hashlib
import urllib.parse

# Signature: "sig" value in post data
# Method: MD5

"""
Request data screenshot - https://i.ibb.co/z6SmGzT/2023-06-21-185300389.png

Original encoding in APK, cotlin:

{
    n.e(httpUrl, "url");
    d dVar = new d();
    if ((requestBody != null ? requestBody.contentType() : null) != null && n.a(requestBody.contentType(), j.a())) {
        Object fromJson = this.f30684a.fromJson(a(requestBody), (Class<Object>) d.class);
        n.d(fromJson, "gson.fromJson(body, RequestBodyMap::class.java)");
        dVar = (d) fromJson;  // dict from post data
    }
    ArrayList arrayList = new ArrayList(httpUrl.queryParameterNames());  // list with params
    Set<String> keySet = dVar.keySet();
    n.d(keySet, "requestBodyMap.keys");
    arrayList.addAll(keySet);  // add post data
    s.w(arrayList, a.f30685a);
    StringBuilder sb = new StringBuilder();
    if (str != null) {
        sb.append(str);  // str - auth token
    }
    Iterator it = arrayList.iterator();
    while (true) {
        boolean z = false;
        if (it.hasNext()) {  // parsing key-value from array with params and data and appending to string
            String str2 = (String) it.next();
            if (httpUrl.queryParameterValues(str2).size() == 0) {
                sb.append(str2);
                String str3 = dVar.get(str2);
                boolean z2 = str3 != null && (w.L(str3, "[", false, 2, null)) && (w.x(str3, "]", false, 2, null));
                boolean z3 = str3 != null && (w.L(str3, "{", false, 2, null)) && (w.x(str3, "}", false, 2, null));
                if (str3 != null && (x.Q(str3, "https", false, 2, null))) {
                    z = true;
                }
                if ((z2 || z3) && z) {
                    sb.append(str3 != null ? w.H(str3, "/", "\\/", false, 4, null) : null);
                } else {
                    sb.append(str3);
                }
            } else if (!(x.Q(str2, HttpUrl.PATH_SEGMENT_ENCODE_SET_URI, false, 2, null))) {
                for (String str4 : httpUrl.queryParameterValues(str2)) {
                    sb.append(str2);
                    if (str4 == null) {
                        str4 = "";
                    }
                    sb.append(str4);
                }
            } else {
                sb.append(w.H(str2, HttpUrl.PATH_SEGMENT_ENCODE_SET_URI, '[' + ((String) f.x(httpUrl.queryParameterValues(str2)).r(b.f30686a).c(f.b.a.b.f(","))) + ']', false, 4, null));
            }
        } else {
            sb.append("d21b9f04fc6acebbc984b896918f650b");  // salt int the end
            try {
                String sb2 = sb.toString();
                n.d(sb2, "rawSig.toString()");
                return d(sb2);  // d - md5 hashing function
            } catch (UnsupportedEncodingException e2) {
                k.b.a.i.b.e(e2, "can't calculate sig", new Object[0]);
                return null;
            } catch (NoSuchAlgorithmException e3) {
                k.b.a.i.b.e(e3, "can't calculate sig", new Object[0]);
                return null;
            }
        }
    }
}
"""


def GetParams(url: str) -> tuple[str, str]:
    """
    Note: Content MUSTNOT be urlencoded. "+3" and "%2B" will give different hash
    """
    token = ""
    params = url.split('?')[1]
    param_list = params.split('&')
    param_dict = {}

    for param in param_list:
        key, value = param.split('=')
        key = urllib.parse.unquote(key)  # urldecode param name
        value = urllib.parse.unquote(value)  # urldecode param value
        param_dict[key] = value

    sorted_keys = sorted(param_dict.keys())

    # Create a new dictionary with sorted keys by alphabet
    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict[key] = param_dict[key]
        if key == "token":
            token = sorted_dict[key]

    param_string = ""
    for key, value in sorted_dict.items():
        param_string += key + value
    return param_string, token


def GetData(post_data: dict) -> str:
    sorted_keys = sorted(post_data.keys())  # sort by alphabet
    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict[key] = post_data[key]

    data_string = ""
    for key, value in sorted_dict.items():
        data_string += key + value
    return data_string


def encode(string: str) -> str:
    hashed_value = hashlib.md5(string.encode())
    return hashed_value.hexdigest()


def SignRequest(
        data: dict,
        url: str = "https://api.labirint.ru/v4/user/login/validation?build=3888&version=3.7.1&bundleId=11532537&debug=false&timeZone=%2B3&imageSize=2&token=89f0e116f3c49bc03233bf620edc634c",
        salt: str = "d21b9f04fc6acebbc984b896918f650b"
):
    params_str, token = GetParams(url)
    data_str = GetData(data)

    to_hash = f"{token}{data_str}{params_str}{salt}"
    sig = encode(to_hash)
    return sig


print("Sign:", SignRequest(data={"authString": "email@gmail.com"}))
# output: 0aea672d643e9d74d90fe437ccad6a39
# it is the same md5 hash as sig in screenshot. depends on params and post data, always different
