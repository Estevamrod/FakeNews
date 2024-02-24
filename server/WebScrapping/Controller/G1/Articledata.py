import requests
from bs4 import BeautifulSoup

class ArticleInfo:
    def __init__(self,link):
        self.link = link
    
    def GetDate(self):
        originalLink = ""
        reqdata = requests.get(f"https:{self.link}")
        content = reqdata.text
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find('script'):
            originalLink = link.format().rsplit('window.location.replace("')[1].rsplit('");')[0]
        data = requests.get(originalLink)
        htmlcontent = data.text
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        for date in soup.find('time'):
            # print(date.strip().rsplit(" ")[0])
            return date.strip().rsplit(" ")[0]


