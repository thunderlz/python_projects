# 先安装两个python包，然后直接运行这个文件就可以了
# pip install aliyun-python-sdk-core
# pip install aliyun-python-sdk-alidns

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
import urllib
import json

class Leizddns():
    def __init__(self,rr):
        self.rr=rr
        self.base='thunderlz.com'
        self.subdomain=self.rr+'.'+self.base
        self.ip=self.get_internet_ip()
        self.client=AcsClient('LTAI4FkuABR3tFbivPUKmMXs', 'aW7qXNiaWkuRREQuNJ2buogBtCEAOj', 'thunderlz@1599093817530509.onaliyun.com')
        self.des_relsult=self.Describe_SubDomain_Records('A',self.subdomain)
        

    def refresh_ip(self):
        if self.des_relsult["TotalCount"] == 0:
            add_relsult = self.add_record("5","600","A",self.ip,self.rr,self.base)
            record_id = add_relsult["RecordId"]
            print("域名解析新增成功！{}".format(self.rr+':'+self.ip))
        #判断子域名解析记录查询结果，TotalCount为1表示存在这个子域名的解析记录，需要更新解析记录，更新记录需要用到RecordId，这个在查询函数中有返回des_relsult["DomainRecords"]["Record"][0]["RecordId"]
        elif self.des_relsult["TotalCount"] == 1:
            self.old_ip=self.des_relsult["DomainRecords"]["Record"][0]['Value']
            if self.ip == self.old_ip:
                print("noupdate"+"\nnew_ip:"+self.ip+"\nold_ip:"+self.old_ip)
            else:
                record_id = self.des_relsult["DomainRecords"]["Record"][0]["RecordId"]
                self.update_record("5","600","A",self.ip,self.rr,record_id)
                print("域名解析更新成功！{}".format(self.rr+':'+self.ip))
        else:
            record_id = 0
            print("存在两个子域名解析记录值，请核查删除后再操作！")


    def get_internet_ip(self):
        with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
            html = response.read()
            ip = str(html, encoding='utf-8').replace("\n", "")
        return ip

    
    #以下是函数调用以及说明
    # des_relsult = Describe_SubDomain_Records(client,"A","sz.huangwx.cn")
    # des_relsult["TotalCount"]：解析记录的数量，0表示解析记录不存在，1表示有一条解析记录
    # des_relsult["DomainRecords"]["Record"][0]["RecordId"]：当des_relsult["TotalCount"]为1时，会返回这个RecordId，后续的修改域名解析记录中需要用到
    def Describe_SubDomain_Records(self,record_type,subdomain):
        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')

        request.set_Type(record_type)
        request.set_SubDomain(subdomain)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        relsult = json.loads(response)
        return relsult
    
    #函数调用
    # add_relsult = add_record(self,"5","600","A",self.ip,self.rr,self.base)
    # record_id = add_relsult["RecordId"]#同样会返回一个RecordId，修改的时候也可以直接调用
    def add_record(self,priority,ttl,record_type,value,rr,domainname):
        request = AddDomainRecordRequest()
        request.set_accept_format('json')

        request.set_Priority(priority)
        request.set_TTL(ttl)
        request.set_Value(value)
        request.set_Type(record_type)
        request.set_RR(rr)
        request.set_DomainName(domainname)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        relsult = json.loads(response)
        return relsult

    #函数调用
    # record_id = des_relsult["DomainRecords"]["Record"][0]["RecordId"]
    # update_record(client,"5","600","A",ip,"sz",record_id)
    def update_record(self,priority,ttl,record_type,value,rr,record_id):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')

        request.set_Priority(priority)
        request.set_TTL(ttl)
        request.set_Value(value)
        request.set_Type(record_type)
        request.set_RR(rr)
        request.set_RecordId(record_id)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        return response

if __name__ == '__main__':
    leizddns=Leizddns('new')
    leizddns.refresh_ip()