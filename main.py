from bs4 import BeautifulSoup
import requests
import json
from kakao_login import Issue_token


# basic variables
URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=1&acr=1&acq=오늘+서울+날씨&qdt=0&ie=utf8&query=오늘+서울+날씨"
city_name = "seoul"
lang_code = "kr"

with open('./plaintext/key.json', 'r') as key_file:
    key_json = json.load(key_file)
key_O = key_json["openWeather"]["openWeather_key"]
open_wthr_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key_O}&lang={lang_code}&units=metric"

# Naver "오늘 서울 날씨" searchedInfo
basic_info = requests.get(URL)
parsing = BeautifulSoup(basic_info.text ,"html.parser")
wthr_today = parsing.select_one('div.temperature_text').text

# OpenWeather api weatherInfo
open_wthr = requests.get(open_wthr_URL).text
OW_json = json.loads(open_wthr)
OW_dic_main = OW_json["main"]
OW_dic_wthr = OW_json["weather"][0]

"""
    print(
    str(OW_dic_main["temp"])+"°C",
    str(OW_dic_main["feels_like"])+"°C",
    str(OW_dic_main["temp_min"])+"°C",
    str(OW_dic_main["temp_max"])+"°C",
)
print(
    OW_dic_wthr["main"], # weather 
    OW_dic_wthr["description"] # weather described in Korean
)
"""

token = Issue_token()
print(token)