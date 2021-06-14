import requests
from bs4 import BeautifulSoup
import csv

url='http://xygy.gzggzy.cn/OrderXinList.aspx'
paylord={'__EVENTTARGET':'Pager','__EVENTARGUMENT':121,'ScriptManager1':'UpdatePanel1|Pager'}
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}

rq=requests.post(url=url,headers=headers)

bsObj=BeautifulSoup(rq.text,'lxml')
viewstate=bsObj.find('input',{'id':'__VIEWSTATE'})


with open('xieyigonghuo.csv','wt') as f:
    csvout=csv.writer(f)
    for i in range(1,9172):
        paylord={'__EVENTTARGET':'Pager','__EVENTARGUMENT':i,'ScriptManager1':'UpdatePanel1|Pager','__ASYNCPOST': 'true','__VIEWSTATE':viewstate['value']}

        rq=requests.post(url=url,data=paylord,headers=headers)

        bsObj=BeautifulSoup(rq.text,'lxml')
        rows=bsObj.find('table',{'class':'table2'}).find_all('tr')
        print('页码：', i)
        for row in rows:

            cols=row.find_all('td')
            if len(cols)>=6:
                csvout.writerow([cols[0].string, cols[1].string, cols[2].string, cols[3].string, cols[4].string, cols[5].string, cols[6].string])

