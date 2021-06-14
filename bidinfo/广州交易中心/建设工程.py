import requests
from bs4 import BeautifulSoup
import re
import csv


url='http://www.gzzb.gd.cn/cms/wz/view/index/layout2/szlist.jsp'
# url='http://www.gzzb.gd.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=503&channelids=15&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=1'
# url='http://www.gzzb.gd.cn/cms/html/wz/view/index/layout2/fwzq_zbdl.html?channelId=34'

# srcUrl='http://www.gzzb.gd.cn/cms/html/wz/view/index/layout2/fwzq_zbdl.html?channelId=34'

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
         ,'Host':'www.gzzb.cn'
         ,'Connection':'keep-alive'
         ,'Cache-Control':'max-age=0'}

initParams={'siteId': '1',
'channelId': '504',
'channelids': '16',
'pchannelid': '466',
'curgclb': '01,02,14',
'curxmlb': '01,02,03,04,05,14',
'curIndex': '2',
'pcurIndex': '1'}



# 转换参数成字典格式
def paramsTransform(srcParams):
    tmpList = srcParams.split('(')
    tmpList = tmpList[1].split(')')
    paramsList = tmpList[0].split(',')
    # print(paramsList)
    if len(paramsList)==7:
        if (paramsList[2] == '466'):
            curgclb="01,02,14"
        elif (paramsList[2] == '467'):
            curgclb="03"
        elif (paramsList[2] == '468'):
            curgclb="05"
        elif (paramsList[2] == '469'):
            curgclb="06"
        elif (paramsList[2] == '470'):
            curgclb="04"
        elif (paramsList[2] == '471'):
            curgclb="07"
        elif (paramsList[2] == '47'):
            curgclb="08"
        elif (paramsList[2] == '473'):
            curgclb=""
        elif (paramsList[2] == '474'):
            curgclb="13"
        else:
            curgclb='0'

        fmtParams = {'siteId': '1',
                     'channelId': paramsList[0],
                     'channelids': paramsList[1],
                     'pchannelid': paramsList[2],
                     'curgclb': curgclb,
                     'curxmlb': '01,02,03,04,05,14',
                     'curIndex': paramsList[5],
                     'pcurIndex': paramsList[6]}

        return fmtParams

#获取各种工程的链接参数
def getParams(url,headers,initParams):
    s=requests.Session()
    rp=s.get(url,headers=headers,params=initParams)
    bsObj=BeautifulSoup(rp.content,'html5lib')
    # print(bsObj)
    paramsTable=bsObj.find('ul',{'class':'ad_cd_ul'})
    paramsList=paramsTable.find_all('li',{'class':re.compile('list_cdsmall.*')})
    Params=[x['onclick'] for x in paramsList]
    # print(Params)
    return [paramsTransform(Param) for Param in Params]


# 获取单个链接的文字列表
def getPrjlist(url,headers,param):

    if param == None:
        return '无效参数！'
    else:
        try:
            s = requests.Session()
            rq = s.post(url, headers=headers, params=param)
            print(rq.url)
            prjList=[]
            pagetext=re.findall('>共(.*)页<',rq.content.decode('gbk'))
            pagenumber=int(pagetext[0])

            for i in range(1,pagenumber+1):
                # print('页码：',i)
                payload={'page':i}
                rq=s.post(url,headers=headers,params=param,data=payload)
                # rq.encoding='gbk'
                bsObj=BeautifulSoup(rq.content,'lxml')
                prjtable=bsObj.find('table',{'class':'wsbs-table'})
                links=prjtable.find_all('a')
                prjList.extend([link.string for link in links])

            return prjList
        except:
            return param


Params=getParams(url,headers,initParams)
print(Params)

for Param in Params:
    results=getPrjlist(url,headers,Param)
    print('返回{}个结果'.format(len(results)))
    print(results)


