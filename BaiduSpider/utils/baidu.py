import urllib
import requests 
from bs4 import BeautifulSoup
from domain import LinkInfo
import re


class BaiduSpider:
    def __init__(self, keyword="", page_index=0):
        self.keyword = keyword
        self.page_index = page_index
        self.searchUrl = ""
        self.pageContent = ""
        self.prefix = "http://www.baidu.com/s"
        pass
    
    def createUrl(self):
        command = self.keyword
        search = [('wd', command), ('pn', self.page_index)]
        self.searchUrl = self.prefix + "?" + urllib.parse.urlencode(search)
        print("searchUrl:%s" % self.searchUrl)
        
    def getPageContent(self):
        self.createUrl()
        response = requests.get(url=self.searchUrl)
        self.pageContent = response.content
        return self.pageContent
    
    def setPageIndex(self, page_index):
        self.page_index = page_index
        
    def setKeyword(self, keyword):
        self.keyword = keyword   


class Analyzer:
    def __init__(self):
        pass

    def get_result(self, page, index, limit):
        soup = BeautifulSoup(page, "html.parser")
        # if index == 20:
        #     print("\n")
        #     print("\n")
        #     print("soup:"+str(soup))
        #     print("\n")
        #     print("\n")
        divs = soup.find_all('div', {'class': 'c-container'})
        i = 1
        result = LinkInfo.SearchResult()
        for div in divs:
            link = div.find('a', {'class': 'c-showurl'})
            if not link:
                link = div.find('span', {'class': 'c-showurl'})
            # print('link:'+str(link))
            if not link:
                i = i + 1
                continue
            href = link.get_text()
            # print("href:%s index:%d" % (href, i))
            if href.find('cn.made-') != -1:
                # print("href:%s index:%d" % (href, i))
                h3 = div.find('h3')
                url = h3.find('a').get('href')
                text = h3.get_text()
                print('link:' + str(link))
                print("href:%s index:%d" % (href, index+i))
                print("h3:%s index:%d" % (text, index+i))
                res = requests.get(url=url)
                # 得到网页原始地址
                url = res.request.url
                link_item = LinkInfo.LinkItem(url, text, username='a', ranking=index+i)
                result.append(link_item)
            i = i + 1
        is_continue = self.is_continue_loop(soup, limit)
        return result, is_continue

    @staticmethod
    def is_continue_loop(content, limit=5):
        page_div = content.find('div', {'id': 'page'})
        # print("page_div:"+str(page_div))
        if not page_div:
            return False
        else:
            span = page_div.find('span', {'class': 'pc'})
            num = span.get_text()
            if num == limit:
                return False
            elif span.length == num:
                return False
            else:
                return True
