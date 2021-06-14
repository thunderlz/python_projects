import requests
from bs4 import BeautifulSoup
import csv




with open('dianzishangcheng2017.csv','wt') as f:
    csvout=csv.writer(f)
    csvout.writerow(['序号','订单号','订单价格','采购单位','供应商名称','成交时间'])
    for i in range(0,2464):
        url='http://mall.gzggzy.cn/frontDealDynamic/dealDynamicHtml?pageNo={}&startDate=2017-01-01&endDate=2017-12-31&content=&queryType=1'.format(i)
        print('页码：',i)
        rq=requests.get(url)
        bsObj=BeautifulSoup(rq.text,'lxml')
        rows=bsObj.tbody.find_all('tr')
        for row in rows:
            cols=row.find_all('td')
            if len(cols)>=6:
                print(cols[3].string)
                csvout.writerow([cols[0].string,cols[1].string,cols[2].string,cols[3].string,cols[4].string,cols[5].string])

