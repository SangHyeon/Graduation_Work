#-*- coding: utf-8 -*-

import os
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import datetime
import lxml
import usd_currency
from bs4 import BeautifulSoup
import sys
from imp import reload
import re

reload(sys)
sys.getdefaultencoding()
TARGET_URL = 'http://info.finance.naver.com'

#check total article amount, then set search range

#####
#하락세
#원 달러 환율 내린 #원 달러 환율 약보합 #원 달러 하향
#원 달러 약세 #원 달러 하락 #원화 가치 상승
pos = [0, 0, 0, 0, 0, 0]
cnt_pos = 0
#

####
#상승세
#원 달러 환율 오른 #원 달러 환율 강보합 #원 달러 상승
#원 달러 상향 #원 달러 강세 #원화 가치 하락
neg = [0, 0, 0, 0, 0, 0]
cnt_neg = 0
#

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', \
            '', cleaned_text)
    return cleaned_text

def get_user_info():
    f = open("user.txt", 'r')
    lines = f.readlines()
    f.close()

    ci = str(lines[0])
    cs = str(lines[1])

    client_id = ci.replace('"\\', '')
    client_secret = cs.replace('"\\', '')
    return client_id, client_secret

def get_date():
    date = datetime.datetime.now().strftime("%Y.%m.%d")
    #date = 20170310
    s_date = str(date)
    return s_date

def get_article(output_file, url):
    global pos, cnt_pos
    global neg, cnt_neg
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    text = ''
    for item in soup.find_all('ul', class_='type01') :
        text = text + str(item.find_all(text=True))
        text = clean_text(text)
        print (str(text))
        #원 달러 환율 내린 #원 달러 환율 약보합 #원 달러 하향
        #원 달러 약세 #원 달러 하락 #원화 가치 상승
        pos[0] = len(re.findall("원.+달러.+환율.+내린", text))
        pos[1] = len(re.findall("원.+달러.+환율.+약보합", text))
        pos[2] = len(re.findall("원.+달러.+하향", text))
        pos[3] = len(re.findall("원.+달러.+약세", text))
        pos[4] = len(re.findall("원.+달러.+하락", text))
        pos[5] = len(re.findall("원화.+가치.+상승", text))
        cnt_pos += sum(pos, 0.0)

        #원 달러 환율 오른 #원 달러 환율 강보합 #원 달러 상승
        #원 달러 상향 #원 달러 강세 #원화 가치 하락
        neg[0] = len(re.findall("원.+달러.+환율.+오른", text))
        neg[1] = len(re.findall("원.+달러.+환율.+강보합", text))
        neg[2] = len(re.findall("원.+달러.+상승", text))
        neg[3] = len(re.findall("원.+달러.+상향", text))
        neg[4] = len(re.findall("원.+달러.+강세", text))
        neg[5] = len(re.findall("원화.+가치.+하락", text))
        cnt_neg += sum(neg, 0.0)
        output_file.write(str(text))

def get_article_url(client_id, client_secret, output_file, url): #get articles' title url
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    t_pages = soup.find_all('div', class_='title_desc all_my')
    d_pages = str(t_pages).split('/')
    
    pages = d_pages[1]
    pages = clean_text(pages)
    pages = pages.strip()
    pages = pages[:-1]
    pages = int(pages)

    for find in soup.find_all('div', class_='paging') :
        n_page = find.select('a')
        t_url = "https:"+n_page[0]['href']
        s_url = t_url[:-2]
        #print(s_url)
        cnt = -9
        while cnt < pages :
            t_cnt = cnt+10
            cnt += 10
            url = s_url + str(t_cnt) +"&refresh_start=0"
            get_article(output_file, url)

def main():
    print(usd_currency.USD())
    client = get_user_info()
    day = datetime.datetime.today().weekday() 
    if(day == 5 or day == 6) :
        print("Today is weekend")
    else :
        encText = urllib.parse.quote(get_date())
        encText2 = urllib.parse.quote("원달러환율")
        url = "https://search.naver.com/search.naver?where=news&se=0&query="+encText2+"&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds="+encText+"&de="+encText+"&docid=&nso=so%3Ar%2Cp%3Afrom20170406to20170406%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0"
        #url = "https://search.naver.com/search.naver?where=news&se=0&query="+encText2+"&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2017.04.26&de=2017.04.26&docid=&nso=so%3Ar%2Cp%3Afrom20170406to20170406%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0"
        output_file = open('words_log.txt', 'w')
        get_article_url(client[0], client[1], output_file, url)
        print("=====> : ", cnt_pos)
        print("-----> : ", cnt_neg)
        print(cnt_pos - cnt_neg)
        output_file.close()

if __name__ == '__main__':
    main()
