from utils import baidu
from domain import LinkInfo

keyword = "山东淄泵泵业有限公司"
spider = baidu.BaiduSpider()
spider.setKeyword(keyword)

analyzer = baidu.Analyzer()
result = LinkInfo.SearchResult(keyword)

print("init")
for i in range(0, 5):
    spider.setPageIndex(i*10)
    content = spider.getPageContent()
    temp, is_continue = analyzer.get_result(content, 5)
    result.appends(temp.links)
    if not is_continue:
        break
print("keyword:"+keyword)
print("搜索数量：%d" % (len(result.links)))
for link in result.links:
    link.console()