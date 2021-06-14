import requests
from bs4 import BeautifulSoup
import csv

head='http://wj.gzggzy.cn/'
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
with open('wangshangjingjia.csv','wt') as f:
    csvout=csv.writer(f)
    csvout.writerow(['编号','项目名称','公告日期','公告内容'])
    for i in range(1,851):

        url='http://wj.gzggzy.cn/NoticeList.aspx?type=0&page={}'.format(i)

        rq=requests.get(url)
        bsObj=BeautifulSoup(rq.text,'lxml')
        rows=bsObj.find('table',{'id':'test'}).find_all('tr')
        for row in rows:
            # print(row)
            cols=row.find_all('td')
            if len(cols)>=3 and cols[0].string!='项目编号':


                print(cols[1].text.strip())
                urlmx=head+cols[1].a['href']
                rqmx=requests.get(urlmx,headers=headers)
                rqmx.encoding='utf-8'
                bsObjmx=BeautifulSoup(rqmx.text,'lxml')
                # print(bsObjmx)
                bsObjmx.find('div',{'class':'note_content'}).text.strip()
                csvout.writerow([cols[0].string, cols[1].text.strip(), cols[2].string,bsObjmx.find('div',{'class':'note_content'}).text.strip()])