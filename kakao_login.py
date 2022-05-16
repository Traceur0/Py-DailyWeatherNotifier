import requests
import json


url = "https://kauth.kakao.com/oauth/token" 

with open('./plaintext/key.json', 'r') as key_file:
    key_json = json.load(key_file)
key_K = key_json["kakaoTalk"]["kakao_key"]
authorization_code = key_json["kakaoTalk"]["authorization_code"]
# REFRESH TOKEN
rf_token = key_json["kakaoTalk"]["refresh_token"]

# code_issuing_URL = f"https://kauth.kakao.com/oauth/authorize?client_id={key_K}&redirect_uri={redirect_URI}&response_type=code" 

# def Issue_auth_code():
    

def Issue_token():
    data = {
        'grant_type' : 'refresh_token',
        'client_id' : key_K,
        'redirect_URI' : "https://example.com/oauth",
        'code' : authorization_code,
        'refresh_token' : rf_token,
    }

    rqst_URL = requests.post(url, data=data)
    # request URL / data : additional requestInfo(parameter)
    token = rqst_URL.json()


    # save responseInfo in .json (allocating to variable)
    with open("./plaintext/k_token.json", "w") as token_json:
        json.dump(token, token_json, indent="\t")
    with open("./plaintext/k_token.json", "r") as token_json:
        token_read = json.load(token_json)
    # save issued value:xrefresh_token in key.json
    try: 
        refresh = token_read["refresh_token"]
    except KeyError: # if error occured
        print("notice:lastest refresh token is still valid.")
    else: # if error not occured
        with open("./plaintext/key.json", "r") as code_json:
            key_f_token_json = json.load(code_json)
        key_f_token_json["kakaoTalk"]["refresh_token"] = refresh

    result = token_read["access_token"]
    return result