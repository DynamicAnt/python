'''
Created on 2018年8月8日

@author: qiumingsheng
'''
#coding:utf-8
import urllib
from urllib import request
import requests 
from bs4 import BeautifulSoup
import re
import time
import openpyxl

url = "http://www.baidu.com/s"
arr = []

global pageIndex
pageIndex = 0

index_pattern = re.compile('http(s)?://(\w)*.cn.made-in-china.com(/)?')
prod_list_pattern = re.compile('.*/showroom/(\w)*-product-list-(\d)*.html')
prod_detail_pattern = re.compile('.*/gongying/.*')
video_pattern = re.compile('.*/video/.*')
gif_pattern = re.compile('.*/gif/.*')
tupian_pattern = re.compile('.*/tupian/.*')

def regtest():
    txt = '  <script type="text/javascript">    _WWW_SRV_T =173.33;    </script>'
#     txt = re_script.sub('',txt)
    print('txt:%s' %(txt))
    
def createUrl(logusername,num):
    command = "site:cn.made-in-china.com inurl:"+logusername
    search = [('wd',command),('pn',num)]
    searchUrl = url + "?" + urllib.parse.urlencode(search)
    print("searchUrl:%s" %(searchUrl))
    return searchUrl

def getPageContent(url):
    response = request.urlopen(url)
    page = response.read()
    page = page.decode('utf-8')
    return page
    

def createFile(url): 
    log(getPageContent(url))
    print('file created')
    
def readFile():
    file = open("test.html","r+",encoding="utf-8")   
    return [file,0]

def log(msg):
    file_object = open("test.html","w",-1,"utf-8")
    file_object.write(msg)
    file_object.close()  

def getUrlType(url):    
    urlType = 'index'
    if index_pattern.match(url):
        urlType = 'index'
    elif prod_list_pattern.match(url):
        urlType = 'prod_list'
    elif prod_detail_pattern.match(url):
        urlType = 'prod_detail'
    elif tupian_pattern.match(url):
        urlType = 'tupian'   
    elif video_pattern.match(url):
        urlType = 'video'
    elif gif_pattern.match(url):
        urlType = 'gif' 
    return urlType    

def getInfo(page):
    soup = BeautifulSoup(page,"html.parser")   
    tagh3 = soup.find_all('h3')
    div = soup.find_all('a',string = re.compile('下一页'))
    print('div content: %s' %(str(div)))
    hasNext = 1 if div else 0
    print('hasNext: %d' %(hasNext))
    
    for h3 in tagh3:
        href = h3.find('a').get('href')
        text = h3.get_text()
        res = requests.get(url=href)
        targetPage = res.content
        soup1 = BeautifulSoup(targetPage,"html.parser")   
        title = soup1.find_all('title')[0].get_text()
        real_url = res.request.url  #得到网页原始地址
        urlType = getUrlType(real_url)
        info = {
            'baidu_title':text,
            'real_title':title,
            'url':real_url,
            'url_type':urlType
        }
        arr.append(info)
    print("finish getInfo")    
    return [arr,hasNext]

def fetchRank(keyword,hasNext=1):
    global pageIndex
    print("fetch %d" %(hasNext))
    if hasNext:
#         searchUrl = createUrl(keyword,pageIndex)
#         page = getPageContent(searchUrl)
        data = readFile()
        
        getInfo(data[0])
        pageIndex = pageIndex + 10
        fetchRank(keyword,data[1])
    else:
        print("finished")
        
def write_to_excel(data,keyword): 
    excelArr = [['用户名','链接类型',' 收录链接 ',' 收录词 ' ,'实际title',' 收录数量 ']] 
    
    excelArr.append([keyword,data[0]['url_type'],data[0]['url'],data[0]['baidu_title'],data[0]['real_title'],len(data)])
    for i in range(1,len(arr)):        
        excelArr.append([keyword,data[i]['url_type'],data[i]['url'],data[i]['baidu_title'],data[i]['real_title'],''])
        
    book = openpyxl.Workbook()#新建一个excel
    sheet = book.active
    sheet.title = 'url_text'
    row = 1#控制行
    for stu in excelArr:
        col = 1#控制列
        for s in stu:#再循环里面list的值，每一列
            sheet.cell(row,col,s)
            col+=1
        row+=1
    book.save('links.xlsx')#保存到当前目录下      
    print("finish write_to_excel")

startTime = time.clock()     
logUsername = 'fulaitong'
fetchRank(logUsername)  
write_to_excel(arr,logUsername)
finishTime = time.clock()


    
print("共耗时%f s"  %(finishTime-startTime))