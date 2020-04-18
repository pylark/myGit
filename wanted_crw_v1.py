import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

searchkeywords = input("키워드를 입력하세요: ")
url = f"https://www.peoplenjob.com/jobs?period=all&field=title&q={searchkeywords}"

data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

up_date = soup.select("#content-main > div > table > tbody > tr > td.date")
job_title = soup.select("#content-main > div > table > tbody > tr > td.job-title > a")
job_position = soup.select("#content-main > div > table > tbody > tr > td.job-title > span")
job_location = soup.select("#content-main > div > table > tbody > tr > td > a")
job_name = soup.select("#content-main > div > table > tbody > tr > td.name > a")

result = []

for item in zip(up_date, job_title, job_position, job_location, job_name) :
    result.append({"날짜": item[0].text, "제목": item[1].text.strip(), "직종": item[2].text.strip(), "위치": item[3].text.strip(), "이름": item[4].text.strip()})
    print(result)

#for item in zip(up_date, job_title, job_position, job_location, job_name) :
#    print(item[0].text)