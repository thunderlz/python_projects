# 爬虫公共类
# -*- coding: utf-8 -*-
# code by leiz

import requests

class pachong():
    def __init__(self,host):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            , 'Accept-Language': 'zh-CN,zh;q=0.9'
            , 'Accept-Encoding': 'gzip, deflate'
            # ,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            ,'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
            , 'Host': host
            , 'Connection': 'keep-alive'
            , 'Cache-Control': 'max-age=0'
            , 'Upgrade-Insecure-Requests': '1'
            ,'Cookie': 'PHOENIX_ID=0a650c81-154a0633f47-a97843; _hc.v="\"e27e18eb-3a3d-4b40-b06a-cbe624c96048.1462979739\""; s_ViewType=10; JSESSI aburl=1; cy=2; cye=beijing'}

    def getHtml(self,url, params=''):
        s = requests.Session()
        for i in range(3):
            try:
                resp = s.get(url, headers=self.headers, params=params, timeout=10)
                if resp.status_code == 200:
                    return resp.content
                else:
                    print(resp.status_code)
                    return None
            except:
                print('timeout for {}'.format(i + 1))
            return  None

if __name__=='__main__':

    p=pachong('www.baidu.com')
    print(p.headers)