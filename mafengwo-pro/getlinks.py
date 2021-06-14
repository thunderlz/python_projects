#马蜂窝获取旅游信息遍历目的地页面上的所有地方，获取攻略，获取游记的链接。
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
htmlmdds=BeautifulSoup(rq.text,'lxml')
#所有目的地的名称和链接
mdddic={mddlink.text:mddlink['href'] for mddlink in htmlmdds.find_all('a',{'href':re.compile('/travel-scenic-spot/mafengwo/*')})}

driver=webdriver.Firefox(options=ffoptions)
for mddkey in mdddic.keys():
    try:
        print('mdd:'+mddkey,urlhead+mdddic[mddkey])
        driver.get(urlhead+mdddic[mddkey])
        time.sleep(random.randint(5,10))
        #获取攻略的链接
        bsobj=BeautifulSoup(driver.page_source,'lxml')
        glinks=[[mddkey,a['href']] for a in bsobj.find_all('a',{'href':re.compile('mafengwo.cn/gonglve/ziyouxing/.*')})]
        with open('glinks.csv','at') as f:
            csvwriter=csv.writer(f)
            csvwriter.writerows(glinks)

        #这是下卷的语句  
        for i in range(2,90):   #也可以设置一个较大的数，一下到底
            js = "var q=document.documentElement.scrollTop={}".format(i*100)  #javascript语句
            driver.execute_script(js)
        #点击下一页
        while True:
            #游记的链接
            yjlinks=[[mddkey,'http://www.mafengwo.cn'+a['href']] for a in bsobj.find('div',{'class':"_notelist"}).find_all('a',{'href':re.compile('/i/.*')})][::3]
            print('yj:'+yjlinks[0][0])
            with open('yjlinks.csv','at') as f:
                csvwriter=csv.writer(f)
                csvwriter.writerows(yjlinks)
            try:
                driver.find_element_by_link_text('后一页').click()
                time.sleep(random.randint(5,10))
                bsobj=BeautifulSoup(driver.page_source,'lxml')
            except:
                break
    except:
        continue