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
        print("searchUrl:%s" %(self.searchUrl))
        
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

    def get_result(self, page,limit):
        soup = BeautifulSoup(page, "html.parser")
        # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all-next-and-find-next
        # https://stackoverflow.com/questions/33654837/does-beautifulsoup-find-all-preserve-tag-order
        # find_next_sibling
        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(open('./mytable.html'), 'html.parser')
        # row = soup.find('tr', {'class': 'something', 'someattr': 'somevalue'})
        # myvalues = []
        # while True:
        #     cell = row.find('td', {'someattr': 'cellspecificvalue'})
        #     myvalues.append(cell.get_text())
        #     row = row.find_next_sibling('tr', {'class': 'something', 'someattr': 'somevalue'})
        #     if not row:
        #         break
        tagh3 = soup.find_all_next('h3')
        print("tagh3:"+str(tagh3))
        links = soup.find_all_next('a', {'class': 'c-showurl'})
        i = 0
        result = LinkInfo.SearchResult()
        for link in links:
            href = link.get_text()
            print("href:%s index:%d" % (href, i))
            if href.find('cn.made-') != -1:
                # print("href:%s index:%d" % (href, i))
                h3 = tagh3[i]
                url = h3.find('a').get('href')
                text = h3.get_text()
                res = requests.get(url=url)
                # 得到网页原始地址
                url = res.request.url
                link_item = LinkInfo.LinkItem(url, text, username='a', ranking=1)
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
