#-*- coding: utf-8 -*-

import os
import sys
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

def USD() :
    f = open("user.txt", 'r')
    f2 = open("usd.txt", 'w')
    lines = f.readlines()

    ci = str(lines[0])
    cs = str(lines[1])
    client_id = ci.replace('"\\', '')
    client_secret = cs.replace('"\\', '')

    url = "http://info.finance.naver.com/marketindex/?tabSel=exchange#tab_section" # json 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser", from_encoding="EUC-KR")

    editData = soup.find_all('option', {'class': "selectbox-default"})
    editDataStr = str(editData)
    editDataStr = editDataStr.replace('[<option class="selectbox-default" label="1" selected="selected" value="', '')
    editDataStr = editDataStr.replace('"> \\xb9\\xcc\\xb1\\xb9 \\xb4\\xde\\xb7\\xaf USD</option>, <option class="selectbox-default" label="1" value="1">\\xb4\\xeb\\xc7\\xd1\\xb9\\xce\\xb1\\xb9 \\xbf\\xf8 KRW</option>]', '')
    editDataStr = editDataStr.replace("\"> 미국 달러 USD</option>, <option class=\"selectbox-default\" label=\"1\" value=\"1\">대한민국 원 KRW</option>]" ,'')
    f2.write(editDataStr)
    f.close()
    f2.close()
    return  editDataStr
