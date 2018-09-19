#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import requests 
import time
import json
import hashlib
import base64

f = open("b1535599778054.wav", 'rb')
file_content = f.read()
base64_audio = base64.b64encode(file_content)
body = urllib.parse.urlencode({'audio': base64_audio})
# body = {'audio': base64_audio}
# body = {'audio': "base64_audio"}
url = 'http://api.xfyun.cn/v1/service/v1/iat'
api_key = '2f3608b36304454bf898d73123ab99c8'
param = {"engine_type": "sms8k", "aue": "raw"}

x_appid = '5b863283'
x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode(encoding='utf_8', errors='strict'))
x_time = int(int(round(time.time() * 1000)) / 1000)
hash = hashlib.md5()
hashstr = (api_key + str(x_time) + str(x_param, encoding='utf-8'))
hash.update(hashstr.encode('utf-8'))
x_checksum = hash.hexdigest()
# x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
x_header = {'X-Appid': x_appid,
            'X-CurTime': str(x_time),
            'X-Param': x_param,
            'X-CheckSum': x_checksum,
            'Content-Type':'application/x-www-form-urlencoded; charset=utf-8'
            }
result = requests.post(url=url,data=body,headers=x_header);

page = result.content.decode('utf-8')

print (page)


