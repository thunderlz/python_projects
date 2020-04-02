# 单一文件的下载和存储
import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
engine = create_engine(
    'mysql+pymysql://root:751982leizhen@localhost:3306/lungsdata')
# 获取数据
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34106118062347481377_1580545627633&_=1580545627634'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           }

session = requests.session()
html = session.get(url, headers=headers)
# 解析数据
bsobj = BeautifulSoup(html.content, 'lxml')
data = json.loads(json.loads(re.findall('\{.*\}', bsobj.p.string)[0])['data'])
# 获取国际的数据
url_global = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoContinentStatis,FAutoGlobalDailyList,FAutoCountryWeekCompRank,FAutoCountryConfirmAdd'
html_global = session.get(url_global, headers=headers)
bsobj_global = BeautifulSoup(html_global.content, 'lxml')

data_global = json.loads(re.findall('\{.*\}', bsobj_global.p.string)[0])
# print(data_global)
# print(data)

engine.execute('insert into jsondata values(time=%s,jsondata=%s)',
               (datetime.now().strftime('%Y%m%d%H%M%S')),str(data))
engine.execute('insert into jsondataglobal values(time=%s,jsondataglobal=%s)',
               (datetime.now().strftime('%Y%m%d%H%M%S')),str(data_global))
