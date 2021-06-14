import requests
from bs4 import BeautifulSoup
import re
import csv
import traceback
import logging
logging.basicConfig(level=logging.INFO)

jobnum=0


def getlink(link, head,csvout):
    global jobnum
    global keyword
    global headers
    url = head + link
    requestobj = requests.get(url,headers=headers)
    bsObj = BeautifulSoup(requestobj.text, "html.parser")
    nextlink = bsObj.find('a', string='下一页').attrs['href']
    print(nextlink)
    sets=bsObj.find('div',{'class':'sojob-result'}).find_all('li')


    for set in sets:
        # print(set)
        try:
            #公司名称
            lcompany=set.find('a',{'href':re.compile('https://www.liepin.com/company.*')}).string.strip()
        except:
            lcompany=''

        try:
            #行业
            lindustry=set.find('a',{'class':'industry-link'}).string.strip()
        except:
            lindustry=''

        try:
            #职位名称
            ljob=set.a.string.strip()
        except:
            ljob=''

        try:
            #简要说明
            lclearfix=set.find('p',{'class':'condition clearfix'}).attrs['title'].strip()
        except:
            lclearfix=''

        try:
            #处理简要说明的字符串
            lclearfixlist=lclearfix.split('_')
            lmoney=lclearfixlist[0]
            #处理薪水
            lmoney=lmoney.replace('万','')
            lmoneys=lmoney.split('-')

            if len(lmoneys)==2:
                lmoneymin=int(lmoneys[0])
                lmoneymax=int(lmoneys[1])
                lmoneymean=(int(lmoneys[0])+int(lmoneys[1]))/2
            else:
                lmoneymin = None
                lmoneymax = None
                lmoneymean = None


            laddress=lclearfixlist[1][0:2]
            lgrade=lclearfixlist[2]
            lexp=lclearfixlist[3]
        except:
            lmoneymin = ''
            lmoneymax = ''
            lmoneymean = ''
            laddress = ''
            lgrade = ''
            lexp = ''
        try:
            #发布和反馈时间
            ltime=set.find('p',{'class':'time-info clearfix'}).get_text().replace('\n',',').strip()
        except:
            ltime=''

        try:
            #职位吸引力
            ltemptation=set.find('p',{'class':'temptation clearfix'}).get_text().replace('\n',',').strip()
        except:
            ltemptation=''

        try:
            #处理详细页
            page = requests.get(set.a.attrs['href'], headers=headers).text
            pageobj = BeautifulSoup(page, "html.parser")
            #职位描述
            ljobdes=pageobj.find('div', {'class': 'content content-word'}).get_text().replace('\n',',').strip()
            lcompanydes=pageobj.find('div', {'class': 'info-word'}).get_text().replace('\n',',').strip()
        except:
            ljobdes=''
            lcompanydes=''


        finally:
            #录入CSV文件
            jobnum+=1
            l=[[jobnum,keyword,lcompany,lindustry,ljob,lmoneymin,lmoneymax,lmoneymean,laddress,lgrade,lexp,ltime,ltemptation,ljobdes,lcompanydes]]
            logging.info(l)
            csvout.writerows(l)

    # print(bsObj)

    # 迭代下一页
    try:
        getlink(nextlink, head,csvout)
    except:
        print('结束=======')
        return


keywords=['数据挖掘']
for keyword in keywords:
    with open('liepin({}).csv'.format(keyword),'wt') as fout:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}

        csvout=csv.writer(fout)
        csvout.writerows([['序号','搜索关键字','公司','行业','岗位名称','最低薪水','最高薪水','平均薪水','地点','学历','经验','发布时间','职位吸引力','职位描述','企业介绍']])
        head='https://www.liepin.com'
        # keywords = ['数据产品经理', '数据分析']

        link='/zhaopin/?industries=&dqs=&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=f56838ea9fb2841b&d_headId=29b8e9416c067c16ad3c2cdec6801ad9&d_ckId=29b8e9416c067c16ad3c2cdec6801ad9&d_sfrom=search_prime&d_curPage=0&d_pageSize=40&siTag=ZFDYQyfloRvvhTxLnVV_Qg~fA9rXquZc5IkJpXC-Ycixw&key={}'.format(keyword)
        getlink(link,head,csvout)


