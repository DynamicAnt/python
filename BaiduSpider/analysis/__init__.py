from utils import baidu
from domain import LinkInfo
from db import mongodb


db_tool = mongodb.DB()
word_count = db_tool.get_total_num()
analyzer = baidu.Analyzer()
spider = baidu.BaiduSpider()


def fetch(keyword):
    spider.setKeyword(keyword)
    result = LinkInfo.SearchResult(keyword)
    for i in range(0, 5):
        spider.setPageIndex(i * 10)
        content = spider.getPageContent()
        temp, is_continue = analyzer.get_result(content, i * 10, 5)
        if temp.num != 0:
            result.appends(temp)
        if not is_continue:
            break

    db_tool.write_to_link(result)
    # result.console()


# fetch("山东淄泵泵业有限公司")
start = 1
offset = 1
while start < 1 + offset:
    words = db_tool.find_words(start, offset)
    print("index:%d keyword:%s" % (start, str(words)))
    for keyword in words:
        fetch(keyword)
    start = start + offset



