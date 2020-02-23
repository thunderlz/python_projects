#单一文件的下载和存储
import requests
from bs4 import BeautifulSoup
import json
import re
import datetime 
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
engine=create_engine('mysql+pymysql://root:751982leizhen@192.168.31.200:3306/lungsdata')
#获取数据
url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34106118062347481377_1580545627633&_=1580545627634'
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}
session=requests.session()
html=session.get(url,headers=headers)
#解析数据
bsobj=BeautifulSoup(html.content,'lxml')
data=json.loads(json.loads(re.findall('\{.*\}',bsobj.p.string)[0])['data'])
dfchinaDayList=pd.DataFrame(data['chinaDayList'])
dfpvcdata=pd.DataFrame(data['areaTree'][0]['children'])
dfpvcdata['querytime']=datetime.now().strftime('%Y%m%d%H%M%S')
#存入数据库
#dfpvcdata.astype('str').to_sql(name='pvcdata',con=engine,if_exists='append')
#dfchinaDayList.to_sql('chinaday',engine,if_exists='replace')
engine.execute('insert into jsondata values(%s,%s)',(str(data),datetime.now().strftime('%Y%m%d%H%M%S')))
