import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('mongodb://skylark:skylark@54.180.94.231', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.projectTreeon                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
jobkorea_url = f"http://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10013"

data = requests.get(jobkorea_url,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

# 크롤링 명칭
jobkorea_startdate = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.odd > span.time.dotum")
jobkorea_title = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.tplTit > div > strong > a")
jobkorea_position = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.tplTit > div > p.dsc")
jobkorea_name = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.tplCo > a")
jobkorea_region = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.tplTit > div > p.etc > span:nth-child(3)")
jobkorea_enddate = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.odd > span.date.dotum > span")
jobkorea_link = soup.select("#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td.tplTit > div > strong > a")

# 크롤링 내용
result = []

for item in zip(jobkorea_startdate, jobkorea_title, jobkorea_position, jobkorea_name, jobkorea_region, jobkorea_enddate, jobkorea_link):
    if db.information.find_one({"title" : item[1].text.strip()}, {'_id': 0}) == None:
        db.information.insert_one({
            "startdate": item[0].text.strip(), 
            "title": item[1].text.strip(), 
            "position": item[2].text.strip(), 
            "name": item[3].text.strip(), 
            "region": item[4].text.strip(), 
            "enddate": item[5].text.strip(),
            "link": 'www.jobkorea.co.kr'+ item[6].attrs['href']
        })
