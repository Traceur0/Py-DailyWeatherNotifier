from bs4 import BeautifulSoup
import requests
import json

URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=1&acr=1&acq=오늘+서울+날씨&qdt=0&ie=utf8&query=오늘+서울+날씨"
city_name = "seoul"
API_key = "ffb7b2aca905052aa3ad743c984b644d"
lang_code = "kr"
open_wthr_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&lang={lang_code}&units=metric"


basic_info = requests.get(URL)
parsing = BeautifulSoup(basic_info.text ,"html.parser")
wthr_today = parsing.select_one('div.temperature_text').text

OW_raw_data = requests.get(open_wthr_URL)

json_wthr = json.load(OW_raw_data.json())
# with open("./file_wthr.json", "w", encoding="utf-8") as f:
#     json.dump(file_wthr, f, indent=4, ensure_ascii=False)

print(json_wthr)