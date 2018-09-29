# coding=utf-8
import re
import urllib.request
import ssl


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html


def getImg(html):
    reg = r'<p class="img_title">(.*)</p>'
    img_title = re.compile(reg)
    imglist = re.findall(img_title, html)
    return imglist

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://tieba.baidu.com"
html = getHtml(url)
imglist = getImg(html)

print(imglist)