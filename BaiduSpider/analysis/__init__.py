from utils import baidu

keyword = "山东淄泵泵业有限公司"
spider = baidu.BaiduSpider()
spider.setKeyword(keyword)
spider.setPageIndex(0)

content = spider.getPageContent()
    