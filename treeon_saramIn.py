import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('mongodb://skylark:skylark@54.180.94.231', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.projectTreeon                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
saramIn_url = f"http://www.saramin.co.kr/zf_user/search?cat_cd=119&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y"

data = requests.get(saramIn_url,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

# # 크롤링 명칭
# saramIn_startdate = soup.select("")
saramIn_title = soup.select("#recruit_info_list > div.content > div > div.area_job > h2 > a > span")
saramIn_position = soup.select("#recruit_info_list > div.content > div > div.area_job > div.job_sector")
saramIn_name = soup.select("#recruit_info_list > div.content > div > div.area_corp > strong > a > span")
saramIn_region = soup.select("#recruit_info_list > div.content > div > div.area_job > div.job_condition > span > a")
saramIn_enddate = soup.select("#recruit_info_list > div.content > div > div.area_job > div.job_date > span")


for item in zip(saramIn_title, saramIn_position, saramIn_name, saramIn_region, saramIn_enddate):
    if db.information.find_one({"title" : item[0].text.strip()}, {'_id:0'}) == None:
        db.information.insert_one({
            "title": item[0].text.strip(), 
            "position": item[1].text.strip(), 
            "name": item[2].text.strip(), 
            "region": item[3].text.strip(), 
            "enddate": item[4].text.strip()
            })