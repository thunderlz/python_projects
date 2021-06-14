# 广州市政府采购平台
# -*- coding: utf-8 -*-
# code by leiz

import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
from pub import pachong
import json




def Main():
    head='http://gzg2b.gzfinance.gov.cn'
    p = pachong('gzg2b.gzfinance.gov.cn')

    with open('./广州市政府采购平台/info.csv','wt') as f:
        csvWriter=csv.writer(f)
        csvWriter.writerow(['类型','网址','名称','创建时间'])

        url='http://gzg2b.gzfinance.gov.cn/gzgpimp/portalsys/portal.do?method=queryHomepageList&t_k=null'
        for i in range(1,1099):
            params={'current': i,'rowCount': 10,'searchPhrase':'' ,'title_name':'' ,'porid': 'gsgg','kwd':'' }
            print(i)
            j=json.loads(p.getChinabiddingHtml(url,p.headers,params))
            print(j)
            for row in range(10):
                csvWriter.writerow([j['rows'][row]['info_key'],j['rows'][row]['info_path'],j['rows'][row]['title'],j['rows'][row]['creation_time']])
            f.flush()
    return


if __name__=='__main__':

    Main()