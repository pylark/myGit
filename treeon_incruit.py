import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.projectTreeon                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
incruit_url = f"http://job.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=1&cd=102"

data = requests.get(incruit_url,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

# 크롤링 명칭
incruit_startdate = soup.select("#container > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr > td.lasts > div.mdays > p > span")
incruit_title = soup.select("#container > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr > td:nth-child(2) > div > span.accent > a")
incruit_position = soup.select("#container > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr > td:nth-child(2) > div > p.details_txts.firstChild > em")
incruit_name = soup.select("#container > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr > th > div > div.check_list_r > span > a")
incruit_region = soup.select("#container > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr > td:nth-child(3) > div > p > em")
incruit_enddate = soup.select("#container > div.n_job_list_default > div.n_job_list_table_a.list_full_default > table > tbody > tr > td.lasts > div.ddays > p:nth-child(2)")

# 크롤링 내용
result = []

for item in zip(incruit_startdate, incruit_title, incruit_position, incruit_name, incruit_region, incruit_enddate):
    if db.information.find_one({"title" : item[1].text.strip()}, {'_id':0}) == None:
        db.information.insert_one({
            "startdate": item[0].text.strip(), 
            "title": item[1].text.strip(), 
            "position": item[2].text.strip(), 
            "name": item[3].text.strip(), 
            "region": item[4].text.strip().split("\n")[0].split("\r")[0], 
            "enddate": item[5].text.strip()
            })