import pandas as pd
from sqlalchemy import create_engine

#import matplotlib.pyplot as plt
engine=create_engine('mysql+pymysql://root:751982leizhen@192.168.31.200:3306/lungsdata')
#engine=create_engine('mysql+pymysql://root:751982leizhen@192.168.31.200:3306/lungsdata')
#df=pd.read_sql('select * from jsondata order by time desc limit 1',con=engine)
df=pd.read_sql('select * from chinaday',con=engine)
print(df)
dfjson=pd.read_sql('select * from jsondata',con=engine)
querytime=dfjson.iat[-1,1]
print('获取时间：'+querytime[0:4]+'年'+querytime[4:6]+'月'+querytime[6:8]+'日'+querytime[8:10]+'时')

