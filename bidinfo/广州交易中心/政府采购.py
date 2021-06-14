import requests
from bs4 import BeautifulSoup
import csv
h='http://www.gzzb.gd.cn'
with open('gonggao.csv','wt') as f:
    csvout=csv.writer(f)
    for i in range(1,864):
        url='http://www.gzzb.gd.cn/cms/wz/view/index/layout2/zfcglist.jsp?page={}&siteId=1&channelId=456'.format(i)
        # url='http://www.gzzb.gd.cn/cms/wz/view/index/layout3/index.jsp?siteId=1&infoId=565774&channelId=456'
        rq=requests.get(url)
        bsObj=BeautifulSoup(rq.text,'lxml')
        links=bsObj.table.find_all('a')
        print('页码：',i)
        for link in links:
            print(link)
            prj=link.parent.parent.find_all('td')
            rqmx=requests.get(h+link['href'])
            bsObjmx=BeautifulSoup(rqmx.text,'lxml')
            csvout.writerow([prj[0].string,prj[1].string,prj[2].string,bsObjmx.body.text.strip()])
            f.flush()


