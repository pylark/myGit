import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('mongodb://skylark:skylark@54.180.94.231', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.projectTreeon                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
peoplenjob_url = f"https://www.peoplenjob.com/jobs?period=all&field=all&q=%EB%A7%88%EC%BC%80%ED%8C%85"

data = requests.get(peoplenjob_url,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

# 크롤링 명칭
peoplenjob_startdate = soup.select("#content-main > div > table > tbody > tr > td.date")
peoplenjob_title = soup.select("#content-main > div > table > tbody > tr > td.job-title > a")
peoplenjob_position = soup.select("#content-main > div > table > tbody > tr > td.job_type > a")
peoplenjob_name = soup.select("#content-main > div > table > tbody > tr > td.name > a")
peoplenjob_region = soup.select("#content-main > div > table > tbody > tr > td:nth-child(5) > a")
peoplenjob_enddate = soup.select("#content-main > div > table > tbody > tr > td:nth-child(6) > span")


# 크롤링 내용
result = []

for item in zip(peoplenjob_startdate, peoplenjob_title, peoplenjob_position, peoplenjob_name, peoplenjob_region, peoplenjob_enddate):
    if db.information.find_one({'title':item[1].text.strip()},{'_id':0}) == None:
        db.information.insert_one({
            "startdate": item[0].text.strip(), 
            "title": item[1].text.strip(), 
            "position": item[2].text.strip(), 
            "name": item[3].text.strip(), 
            "region": item[4].text.strip(), 
            "enddate": item[5].text.strip()
            })