import requests
from bs4 import BeautifulSoup
import json
import os
import re


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|@#$%^&\ ]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
path='./'

if not os.path.exists(path+'目的地/'):
    os.mkdir(path+'目的地')

urlhead='https://www.mafengwo.cn'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
# url='https://www.mafengwo.cn/gonglve/ziyouxing/list/list_page?mddid=10035&page=2'
# url='https://www.mafengwo.cn/gonglve/ziyouxing/list/list_page?mddid=10091&page=1'

# url='http://www.mafengwo.cn/gonglve/ziyouxing/77110.html'
s=requests.session()

for p in range(1,5000):
    try:
        url='http://www.mafengwo.cn/gonglve/'
        params={'page':p}
        rq=s.post(url,headers=headers,data=params)
        bs=BeautifulSoup(rq.text,'html5lib')
        #创建目录

        # if not os.path.exists('./目的地/{}/'.format(p)):
        #     os.mkdir('./目的地/{}/'.format(p))
        #创建主页面
        # with open('./目的地/{}/{}.html'.format(p,p),'wt') as f:
        #     print(rq.text,file=f)

        for a in bs.find_all('a',{'href':re.compile('https*://www.mafengwo.cn/.*')}):
            # print(link)
            try:
                link=a.attrs['href']
                print(link)
                rq=requests.get(link)
                bs=BeautifulSoup(rq.text,'html5lib')
                title=validateTitle(bs.title.string)[0:10]#创建目录10位
                # 创建目录
                # j = json.loads(bs.script.string[14:-2])
                if bs.find('a', {'href': re.compile('/gonglve/ziyouxing/.*')}):
                    print(bs.find('a', {'href': re.compile('/gonglve/ziyouxing/.*')}).string)
                    target = bs.find('a', {'href': re.compile('/gonglve/ziyouxing/.*')}).string + '/自由行攻略'
                elif bs.find('a', {'class': '_j_mdd_stas'}):
                    print(bs.find('a', {'class': '_j_mdd_stas'}).string)
                    target = bs.find('a', {'class': '_j_mdd_stas'}).string + '/游记'
                else:
                    target='其他'

                print(path + '目的地/{}/'.format(target))

                if not os.path.exists(path + '目的地/{}/'.format(target)):
                    os.makedirs(path + '目的地/{}/'.format(target))

                if not os.path.exists(path+'目的地/{}/{}/'.format(target,title)):
                    os.mkdir(path+'目的地/{}/{}/'.format(target,title))
                    with open(path+'目的地/{}/{}/{}.html'.format(target,title,title), 'wb') as f:
                        # pass
                        rq.encoding='utf-8'
                        f.write(rq.content)
                        # print(bs.find_all('img'))

                    for img in bs.find_all('img'):
                        # print(re.match(re.compile('https*://.*'),img.attrs['src']),img.attrs['src'])
                        try:
                            if re.match(re.compile('https*://.*'),img.attrs['src']):
                                src=img.attrs['src']
                            else:
                                src=img.attrs['data-rt-src']

                            print(src)
                            ir = requests.get(src, stream=True)
                            if ir.status_code == 200:
                                with open(path+'目的地/{}/{}/{}'.format(target,title,src.split('/')[-1].split('?')[0]), 'wb') as f:
                                    for chunk in ir:
                                        f.write(chunk)
                        except:
                            print('错误图片链接{}'.format(img))
                else:
                    print('已经下载')
            except:
                print('错误目的地链接{}'.format(a))

    except:
        print('错误页码{}'.format(p))





# 单个地方的json
# rq=requests.get(url,headers=headers)
# j=rq.json()
# # print(j)
# bs=BeautifulSoup(j['html'],'lxml')
# links=[urlhead+href.attrs['href'] for href in bs.find_all('a')]
# print(links)
#
# for link in links:
#     print(link.split('/')[-1])
#     with open(link.split('/')[-1],'wt') as f:
#         f.write(requests.get(link).text)



