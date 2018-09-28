from utils import baidu
from domain import LinkInfo
from db import mongodb


db_tool = mongodb.DB()
word_count = db_tool.get_total_num()
spider = baidu.BaiduSpider()
analyzer = baidu.Analyzer()


# keyword = "山东淄泵泵业有限公司"
# keyword = "个人用户(树中小鬼)"
def fetch(keyword):
    spider.setKeyword(keyword)
    result = LinkInfo.SearchResult(keyword)
    print("init")
    for i in range(0, 5):
        spider.setPageIndex(i * 10)
        content = spider.getPageContent()
        temp, is_continue = analyzer.get_result(content, i * 10, 5)
        if len(temp.com_dict) != 0:
            result.appends(temp.com_dict)
        if not is_continue:
            break
    print("keyword:" + keyword)
    print("搜索数量：%d" % result.num)
    db_tool.write_to_link(result)
    for link in result.links:
        link.console()


start = 1
offset = 1
while start < 2 + offset:
    words = db_tool.find_words(start, offset)
    for keyword in words:
        fetch(keyword)
    start = start + offset



