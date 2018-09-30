#coding=utf-8
import re
import urllib.request
import requests
import ssl


def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    req = urllib.request.Request(url, None, headers, None, False)
    page = urllib.request.urlopen(req)
    html = page.read()

    # page = urllib.request.urlopen(url)
    # html = page.read()


    # res = requests.get(url=url)
    # html = res.content

    html = html.decode('utf-8')
    print(str(html))
    return html


def getImg(html):
    reg = r'<p class="img_title">(.*)</p>'
    img_title = re.compile(reg)
    imglist = re.findall(img_title, html)
    return imglist

def get_html_https():
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'

ssl._create_default_https_context = ssl._create_unverified_context
# url = "https://tieba.baidu.com"
url = "https://www.baidu.com/s?wd=led&pn=10"
html = getHtml(url)
imglist = getImg(html)

print(imglist)
