import csv
import glob
import os
from bs4 import BeautifulSoup
# import numpy as np
# import pandas as pd

with open('mdd.csv','wt') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(['目的地','类别','文章名称','日期','收藏','分享'])
    path='./目的地/'
    # path = './目的地/'
    # 我又在这里加上一句话6
    #这边也加了呢（win）、
    # aaaaaaa
    mdd_list=os.listdir(path)
    print('一共有{}个目的地:'.format(len(mdd_list)),mdd_list)
    for mdd in mdd_list:

        #自由行
        if os.path.exists(path+mdd+'/自由行攻略'):
            path_mdd_ziyouxing=path+mdd+'/自由行攻略'
            for ziyouxing in os.listdir(path_mdd_ziyouxing):
                with open(path_mdd_ziyouxing+'/'+ziyouxing+'/'+ziyouxing+'.html') as ziyouxing_file:
                    bs = BeautifulSoup(ziyouxing_file.read(),'html5lib')
                print(path_mdd_ziyouxing+'/'+ziyouxing)
                if bs.find_all('span', {'class': 'time'}):
                    ziyouxing_date = bs.find_all('span',{'class':'time'})[1].em.string
                else:
                    ziyouxing_date=''
                #收藏
                if bs.find_all('em',{'class':'favorite_num'}):
                    ziyouxing_favorite=bs.find_all('em',{'class':'favorite_num'})[0].string
                else:
                    ziyouxing_favorite=''
                #分享
                if bs.find_all('a',{'title':'分享'}):
                    ziyouxing_share=bs.find_all('a',{'title':'分享'})[0].em.string
                else:
                    ziyouxing_share=''

                csvwriter.writerow([mdd,'自由行',ziyouxing,ziyouxing_date,ziyouxing_favorite,ziyouxing_share])

        # 自由行
        if os.path.exists(path+mdd+'/游记'):
            path_mdd_youji = path + mdd + '/游记'
            for youji in os.listdir(path_mdd_youji):
                with open(path_mdd_youji+'/'+youji+'/'+youji+'.html') as youji_file:
                    bs = BeautifulSoup(youji_file.read(),'html5lib')
                print(path_mdd_youji+'/'+youji)
                # print(bs)
                if bs.find('li', {'class': 'time'}):
                    youji_date = bs.find('li',{'class':'time'}).get_text()[-10:]
                    # print(youji_date)
                else:
                    youji_date=''
                csvwriter.writerow([mdd,'游记',youji,youji_date])