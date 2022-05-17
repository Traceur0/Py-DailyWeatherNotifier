from bs4 import BeautifulSoup
import requests
import json


url = "https://kauth.kakao.com/oauth/token" 

with open("./plaintext/key.json", "r") as key_file:
    key_json = json.load(key_file)
key_K = key_json["kakaoTalk"]["kakao_key"]
authorization_code = key_json["kakaoTalk"]["authorization_code"]
# REFRESH TOKEN
rf_token = key_json["kakaoTalk"]["refresh_token"]

# code_issuing_URL = f"https://kauth.kakao.com/oauth/authorize?client_id={key_K}&redirect_uri={redirect_URI}&response_type=code" 

# basic variables
URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=1&acr=1&acq=오늘+서울+날씨&qdt=0&ie=utf8&query=오늘+서울+날씨"
city_name = "seoul"
lang_code = "kr"

with open("./plaintext/key.json", "r") as key_file:
    key_json = json.load(key_file)
key_O = key_json["openWeather"]["openWeather_key"]
open_wthr_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key_O}&lang={lang_code}&units=metric"

# Naver "오늘 서울 날씨" searchedInfo
basic_info = requests.get(URL)
parsing = BeautifulSoup(basic_info.text ,"html.parser")
wthr_today = parsing.select_one("div.temperature_text").text

# OpenWeather api weatherInfo
open_wthr = requests.get(open_wthr_URL).text
OW_json = json.loads(open_wthr)
OW_dic_main = OW_json["main"]
OW_dic_wthr = OW_json["weather"][0]


def Issue_token():
    data = {
        "grant_type" : "refresh_token",
        "client_id" : key_K,
        "redirect_URI" : "https://example.com/oauth",
        "code" : authorization_code,
        "refresh_token" : rf_token,
    }
    # request URL / data : additional requestInfo(parameter)
    rqst_URL = requests.post(url, data=data)
    token = rqst_URL.json()

    # save responseInfo in .json (allocating to variable)
    with open("./plaintext/k_token.json", "w") as token_json:
        json.dump(token, token_json, indent="\t")
    with open("./plaintext/k_token.json", "r") as token_json:
        token_read = json.load(token_json)

    # save issued value:refresh_token in key.json
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

def Send_message(access_token):
    msg_sending_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        'Authorization' : "Bearer " + access_token
    }

    data = { "template_object" : json.dumps({
            "object_type" : "text",
            "text" : "weatherForecast",
            "link" : {
                "web_url" : "https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=오늘+서울+날씨"
            }
        })
    }

    msg_rqst = requests.post(msg_sending_URL, headers=headers, data=data)
    return print(msg_rqst.content, access_token)