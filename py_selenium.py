from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://www.naver.com")
soup = BeautifulSoup(browser.page_source, "html.parser")