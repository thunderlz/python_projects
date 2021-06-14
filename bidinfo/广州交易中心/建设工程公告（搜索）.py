import requests
from bs4 import BeautifulSoup
import re
import csv
from multiprocessing import Pool
import time
import os



# 获取单页项目列表
def getPrjList(url,headers):
    prjList=[]
    s=requests.Session()
    for i in range(3):
        try:
            resp=s.get(url,headers=headers,timeout=5+i*10)
            bsObj = BeautifulSoup(resp.content, 'html5lib')
            prjtable = bsObj.find('table', {'class': 'wsbs-table'})
            prjRows=prjtable.find_all('tr')
            for prjRow in prjRows:
                if prjRow.find_all('td') != None:
                    prjCells=prjRow.find_all('td')
                    if len(prjCells)>0:
                        tmp = [x.text.strip() for x in prjCells]
                        if prjCells[1].a['href'] != None:
                            tmp.append('http://www.gzggzy.cn' + prjCells[1].a['href'])
                        prjList.append(tmp)
            print('获取成功。')
            break

        except Exception as e:
            if i<2:
                print('准备重复第{}次尝试'.format(i+1))
            else:
                print('执行失败',url)
                prjList=[['执行失败',url]]
                break

    return prjList





def main(pNum):
    prjAllList=[]
    result=[x for x in range(0,pNum)]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        , 'Host': 'www.gzzb.cn'
        , 'Connection': 'keep-alive'
        , 'Cache-Control': 'max-age=0'}

    with open('项目清单.csv','wt') as f:

        csvwriter=csv.writer(f)

        for i in range(0,6740*15,15*pNum):
            tStart = time.time()
            print('第{}次执行'.format(i/15/pNum+1))
            p = Pool(pNum)
            for j in range(0,pNum):
                url = 'http://www.gzggzy.cn/cms/wz/view/tzygg/HistoryGSQueryServlet?keyWords=+&xmbh=&xmjdbmid=&method=queryZhaoBGS&siteId=1&pager.offset={}'.format(i+j*15)
                result[j]=p.apply_async(getPrjList,args=(url,headers))
            p.close()
            p.join()

            for k in range(0,pNum):
                csvwriter.writerows(result[k].get())
                # print(result[k].get())

            tEnd = time.time()
            print('用时：{}'.format(tEnd - tStart))
            f.flush()




if __name__ == '__main__':
    #进程数量
    pNum=4

    main(pNum)



