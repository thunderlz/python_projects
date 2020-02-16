#马蜂窝获取旅游信息遍历目的地页面上的所有地方，获取攻略，没有获取游记。
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

ffoptions=Options()
ffoptions.add_argument('--headless')
driver=webdriver.Firefox(options=ffoptions)
urlhead='http://www.mafengwo.cn'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
           'host': 'www.mafengwo.cn'
           }
ss=requests.session()
ss.headers=headers
urlmdds=urlhead+'/mdd/'
#访问目的地主页
rq=ss.get(urlmdds,headers=headers)
htmlmdds=BeautifulSoup(rq.text,'html5lib')
mdddic={mddlink.text:mddlink['href'] for mddlink in htmlmdds.find_all('a',{'href':re.compile('/travel-scenic-spot/mafengwo/*')})}

driver=webdriver.Firefox(options=ffoptions)
for mddkey in mdddic.keys():
    try:
        print(urlhead+mdddic[mddkey])
        driver.get(urlhead+mdddic[mddkey])
        time.sleep(random.randint(5,10))
        bsobj=BeautifulSoup(driver.page_source)
        glinks=[[mddkey,a['href']] for a in bsobj.find_all('a',{'href':re.compile('https://m.mafengwo.cn/gonglve/ziyouxing/.*')})]
        with open('glinks.csv','at') as f:
            csvwriter=csv.writer(f)
            csvwriter.writerows(glinks)
    except:
        print(mddkey)