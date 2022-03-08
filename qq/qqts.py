#qqts.py
# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
#觉得不错麻烦点个star谢谢 

'''
没有解决QQ风控问题，收不到我也没法子
使用方式：
与bot.py在同一文件夹下，读取data.txt文件轮询发送查询到的资产
建议bot.py和qqts.py文件都放到青龙script文件夹下，方便定时私聊推送
'''
import time,random
import requests,os,json
import json
import re

client_id=['']
client_secret=['']
urllist = ["http://IP:端口号/"]
requests.packages.urllib3.disable_warnings()
a = requests.session()

def gettimestamp():
    return str(int(time.time() * 1000))

def gettoken(self,url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer "+res})
    
def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []

def getitem(self, baseurl, key , typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def getlogs(self, baseurl, typ):
    url = baseurl + typ + "/logs"
    r = self.get(url)
    res = json.loads(r.text)["dirs"]
    return res

def getfiles(dirs, name):
    for i in dirs:
        if i['name'] == name:
            return i['files']
    return []

def getdetail(self,baseurl,files,filename):
    url = baseurl + "open/logs/"+files+'/'+filename+'/'
    r = a.get(url)
    return r.text

def push_QQ(userid,res_text,typ):
    data = {
    'user_id': userid,
    'message': res_text
    }
    requests.post('http://机器人的IP:推送的端口号/'+typ,data)

def check(a,msg):
    pin = msg.split(',')[1]
    name = msg.split(',')[2]
    ucount = 0
    url_token = urllist[ucount]+'open/auth/token?client_id='+client_id[ucount]+'&client_secret='+client_secret[ucount]
    gettoken(a, url_token)
    JDkeys = getitem(a, urllist[ucount], "JD_COOKIE" , "open")
    pin_list = []
    for i in JDkeys:
        tp = i['value']
        ptpin = re.findall(r"pt_pin=(.*?);", tp)[0]
        pin_list.append(ptpin)
    r = getlogs(a,urllist[ucount],'open')
    res = getfiles(r,'ccwav_QLScript_jd_bean_change')
    detail = getdetail(a,urllist[ucount],'ccwav_QLScript_jd_bean_change',res[0])
    pagetext = json.loads(detail)["data"]
    log1 = re.finditer('\u5065\u5eb7', pagetext)
    log1_list=[]
    for k in log1:
        log1_list.append(int(k.start()))
    log2 = re.finditer(name , pagetext)
    for j in log2:
        x = j.span()[1]-60
    y=log1_list[pin_list.index(pin)]
    result = pagetext[x:y+23]
    res_text = pagetext[10:30]+'查询的资产，定时每日18点更新当天资产\n'+result
    userid = msg.split(',')[0]
    push_type='send_private_msg'
    return res_text

print('开始推送')
with open('data.txt') as fp:
    tmps = fp.readlines()
tmpss = []
for o in tmps:
    tmpss.append(o.replace('\n',''))
for i in tmpss:
    try:
        re_text = check(a,i)
        push_QQ(i.split(',')[0],re_text,'send_private_msg')
        print('资产推送至QQ：{}成功'.format(i.split(',')[0]))
    except:
        print('资产推送至QQ：{}失败'.format(i.split(',')[0]))
print('推送结束')

