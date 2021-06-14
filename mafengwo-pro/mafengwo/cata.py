import os
import glob
from bs4 import BeautifulSoup
import json
import shutil
import re
import requests

print(os.path.abspath('.'))
path='/Volumes/My Passport/'

if not os.path.exists(path+'目的地分类/'):
    os.mkdir(path+'目的地分类/')

for i in range(1,106):
    dirlist=os.listdir('./目的地/{}/'.format(i))
    for dir in dirlist:
        if dir[-3:]=='马蜂窝':
            file=glob.glob('./目的地/{}/{}/*.html'.format(i,dir))
            if len(file)!=0:
               with open(file[0],'rt') as f:
                   bs=BeautifulSoup(f.read(),'lxml')
                   j = json.loads(bs.script.string[14:-2])


                   # print(dir,j)
                   try:
                       if bs.find('a', {'href': re.compile('/gonglve/ziyouxing/.*')}):
                           print(bs.find('a', {'href': re.compile('/gonglve/ziyouxing/.*')}).string)
                           target = bs.find('a', {'href': re.compile('/gonglve/ziyouxing/.*')}).string+'/自由行攻略'
                       else:
                           print(bs.find('a', {'class': '_j_mdd_stas'}).string)
                           target = bs.find('a', {'class': '_j_mdd_stas'}).string+'/游记'
                       # print(j['mddid'])
                       # try:
                       # rq=requests.get('http://www.mafengwo.cn/travel-scenic-spot/mafengwo/{}.html'.format(j['mddid']))
                       # print(rq.status_code)
                       # bstitle=BeautifulSoup(rq.text,'lxml')
                       # target=bstitle.find('div',{'class':'title'}).h1.string
                       # except:
                       # target=j['mddid']
                       # print(target)
                       try:
                           if not os.path.exists(path+'目的地分类/{}/'.format(target)):
                               os.mkdir(path+'目的地分类/{}/'.format(target))
                           shutil.copytree('./目的地/{}/{}/'.format(i,dir),path+'目的地分类/{}/{}/'.format(target,dir))
                       except:
                           print('复制错误')
                   except:
                       print('error', dir, j)



