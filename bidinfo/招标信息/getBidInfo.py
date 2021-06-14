# 中国招标采购网
# -*- coding: utf-8 -*-
# code by leiz

import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

def getChinabiddingHtml(url,headers,params=''):
    s=requests.Session()
    for i in range(3):
        try:
            resp=s.get(url,headers=headers,params=params,timeout=10)
            break
        except:
            print('timeout for {}'.format(i+1))

    print(resp.status_code)
    if resp.status_code==200:
        return BeautifulSoup(resp.content,'html5lib')
    else:
        return None


def getTable(bsObj,head):
    tb=[]
    table=bsObj.find('table',{'class':'table_body'})
    Rows=table.find_all('tr',{'class':('listrow2','listrow1')})
    for Row in Rows:
        Cells=Row.find_all('td')
        link=Cells[1].find('a')['href']
        Line=[x.get_text().strip() for x in Cells]
        Line.extend([head + link])
        tb.append(Line)
    return tb

def Main(keyword):
    # url='https://www.chinabidding.cn/search/Searchgj/zbcg?table_type=&text_x=%E8%BE%93%E5%85%A5%E6%82%A8%E6%83%B3%E6%9F%A5%E6%89%BE%E7%9A%84%E5%85%B3%E9%94%AE%E8%AF%8D+%E5%A4%9A%E4%B8%AA%E8%AF%8D%E5%8F%AF%E4%BB%A5%E8%BE%93%E5%85%A5%E7%A9%BA%E6%A0%BC%E9%9A%94%E5%BC%80%EF%BC%81&keywords=%E6%8B%9B%E6%A0%87%E4%BB%A3%E7%90%86%E6%9C%8D%E5%8A%A1&search_type=TITLE&areaid=&categoryid=&b_date=month&time_start=2018-11-05&time_end=2018-11-05'
    # url='https://www.chinabidding.cn/search/searchzbw/search2?keywords=&table_type=&areaid=&categoryid=&b_date='
    # url='https://www.chinabidding.cn/search/searchzbw/search2?keywords=招标代理服务&areaid=&categoryid=&b_date=month'
    # url='https://www.chinabidding.cn/search/searchzbw/search2?keywords={}&areaid=&categoryid=&b_date=month'


    head='https://www.chinabidding.cn'

    with open('./中国招标采购网/{}.csv'.format(keyword),'wt') as f:
        csvWriter=csv.writer(f)
        csvWriter.writerow(['','项目名称','是否收藏','类型','省份','行业','时间','网址'])
        print(keyword)
        url='https://www.chinabidding.cn/search/searchzbw/search2?keywords={}&areaid=&categoryid=&b_date=month'.format(keyword)
        # print(url)
        bsObj=getChinabiddingHtml(url,headers)
        # print(getTable(bsObj,head),111)
        # csvWriter.writerows(getTable(bsObj,head))
        # print(bsObj.find('a',text='后一页'))
        while bsObj.find('a',text='后一页'):
            link=bsObj.find('a',text='后一页')['href']
            print(link)
            bsObj=getChinabiddingHtml(head+link,headers=headers)
            csvWriter.writerows(getTable(bsObj,head))
            f.flush()
    print('{} Complete'.format(keyword))
    return


headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        ,'Accept-Language': 'zh-CN,zh;q=0.9'
        ,'Accept-Encoding': 'gzip, deflate, br'
        ,'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        ,'Host': 'www.chinabidding.cn'
        , 'Connection': 'keep-alive'
        , 'Cache-Control': 'max-age=0'}

if __name__ == '__main__':
    p=Pool(2)
    for keyword in ['招标代理中介','招标代理机构','招标代理服务']:
        p.apply_async(Main,args=(keyword,))

    p.close()
    p.join()
    