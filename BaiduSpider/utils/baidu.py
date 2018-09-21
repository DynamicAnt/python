import urllib
import requests 
from bs4 import BeautifulSoup
import re

class BaiduSpider():
    def __init__(self,keyword,pageIndex=0):
        self.keyword = keyword
        self.pageIndex = pageIndex
        self.searchUrl = ""
        self.pageContent = ""
        self.prefix = "http://www.baidu.com/s"
        pass
    
    def createUrl(self):
        command = self.keyword
        search = [('wd',command),('pn',self.pageIndex)]
        self.searchUrl = self.prefix + "?" + urllib.parse.urlencode(search)
        print("searchUrl:%s" %(self.searchUrl))
        
    def getPageContent(self):
        self.createUrl()
        response = requests.get(url=self.searchUrl)
        self.pageContent = response.content
        return self.pageContent
    
    def setPageIndex(self,pageIndex):
        self.pageIndex = pageIndex
        
    def setKeyword(self,keyword):
        self.keyword = keyword   
        
class Analyzer():
    def __init__(self):
        pass
    def getSeoInfo(self,page):
        soup = BeautifulSoup(page,"html.parser")   
        tagh3 = soup.find_all('h3')
        links = soup.find_all('a', {'class': 'c-showurl'})
        seoInfo = SeoInfo()
        i=0
        for link in links:
            href = h3.find('a').get('href')
            text = h3.get_text()
            res = requests.get(url=href)
            targetPage = res.content
            soup1 = BeautifulSoup(targetPage,"html.parser")   
            title = soup1.find_all('title')[0].get_text()
            real_url = res.request.url  #得到网页原始地址
            urlType = getUrlType(real_url)
            linkInfo = LinkInfo(real_url, text,title,urlType)
            seoInfo.addLink(linkInfo)
        return seoInfo        