import urllib
import requests 
from bs4 import BeautifulSoup
from domain import LinkInfo


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
        # print("searchUrl:%s" % self.searchUrl)
        
    def getPageContent(self):
        self.createUrl()
        response = requests.get(url=self.searchUrl)
        self.pageContent = response.content
        return self.searchUrl, self.pageContent
    
    def setPageIndex(self, page_index):
        self.page_index = page_index
        
    def setKeyword(self, keyword):
        self.keyword = keyword   


class Analyzer:
    def __init__(self):
        pass

    def get_result(self, page, index, limit):
        soup = BeautifulSoup(page, "html.parser")
        divs = soup.find_all('div', {'class': 'c-container'})
        i = 1
        search_result = LinkInfo.SearchResult()
        for div in divs:
            link = div.find('a', {'class': 'c-showurl'})
            if not link:
                link = div.find('span', {'class': 'c-showurl'})
            if not link:
                i = i + 1
                continue
            href = link.get_text()
            if href.find('cn.made-') != -1:
                h3 = div.find('h3')
                url = h3.find('a').get('href')
                text = h3.get_text()
                res = requests.get(url=url)
                # 得到网页原始地址
                url = res.request.url
                link_item = LinkInfo.LinkItem(url, text, (index + i))

                target_page = res.content
                soup1 = BeautifulSoup(target_page, "html.parser")
                info = soup1.find('div', {'id': 'hidden_remote_user_info'})
                attrs = info.attrs
                search_result.append(attrs, link_item)
                search_result.num = search_result.num + 1

            i = i + 1
        is_continue = self.is_continue_loop(soup, limit)
        return search_result, is_continue

    def get_result_arr(self, keyword, search_url, page, index, limit):
        soup = BeautifulSoup(page, "html.parser")
        # print('\n')
        # print(str(soup))
        # print('\n')
        divs = soup.find_all('div', {'class': 'c-container'})
        div_i = 1
        search_result = []
        for div in divs:
            link = div.find('a', {'class': 'c-showurl'})
            if not link:
                link = div.find('span', {'class': 'c-showurl'})
            if not link:
                div_i = div_i + 1
                continue
            href = link.get_text()
            if href.find('cn.made-') != -1:
                ranking = index + div_i
                h3 = div.find('h3')
                url = h3.find('a').get('href')
                text = h3.get_text()
                res = requests.get(url=url)
                # 得到网页原始地址
                url = res.request.url

                target_page = res.content
                soup1 = BeautifulSoup(target_page, "html.parser")
                info = soup1.find('div', {'id': 'hidden_remote_user_info'})
                if info:
                    attrs = info.attrs
                    search_result.append({
                        "keyword": keyword,
                        "ranking": ranking,
                        "username": attrs['data-logusername'],
                        "com_name": attrs['data-comname'],
                        "cs_level": attrs['data-cslevel'],
                        "baidu_url": search_url,
                        "url": url,
                        "text": text
                    })
                else:
                    search_result.append({
                        "keyword": keyword,
                        "ranking": ranking,
                        "username": "",
                        "com_name": "",
                        "cs_level": "",
                        "baidu_url": search_url,
                        "url": url,
                        "text": text,

                    })

            div_i = div_i + 1
        # is_continue = self.is_continue_loop(soup, limit)
        return search_result

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
