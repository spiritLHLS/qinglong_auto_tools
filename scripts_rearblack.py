# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树后置黑号');
'''

# 谨慎配置！！！自测无问题但实际运行可能有bug！！！可能会打乱原有环境变量顺序！！！
# 禁用的ck自动后置，检索任务对应日志标注黑号后自动后置
# 默认任务定时自行修改

print("谨慎配置！！！自测无问题但实际运行可能有bug！！！可能会打乱原有环境变量顺序或丢失1个ck！！！")

import os
import time
import json
import re
import random

print(
    "查询的模板，黑号上方显示pin那一行的需要给出来，下方是日志以及对应需要填写的东西(jd_XXXXX是pin)\n\n\n==========检索的模板任务日志👇=========\n*********【账号 10】jd_EMgmYJMyrMHn*********\n黑号！\n*********【账号 11】jd_LjfgropqstnG*********\n黑号！\n==============模板日志👆=============\n\n此时需要的配置如下\n")

print(
    "export ec_remode=\"】(.*?)\*\*\*\*\*\*\*\*\*)\"\nexport ec_blackkey=\"黑号！\"\nexport ec_check_task_name=\"青龙中任务的中文名字\"\nexport ec_rear_back_ck=\"true\"\n")

print("配置中填完后就能运行脚本自动检索对应任务名字下的日志查询黑号标注黑号后置黑号了")

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

print("=================正式开始运行脚本，上述文字只是说明=========================")

try:
    os.environ["ec_check_task_name"]
except:
    os.environ["ec_check_task_name"] = ""

try:
    if os.environ["ec_check_task_name"] != "":
        check_task_name = os.environ["ec_check_task_name"]
        print("已配置开启日志检索标注黑号，检索日志任务名字为:\n{}\n".format(check_task_name))
    else:
        check_task_name = ""
        print("未配置日志检索标注黑号")
        pass
except:
    print("默认不开启日志检索标注黑号")
    print("有需要请在配置文件中配置\nexport ec_check_task_name=\"任务名字\"\n开启标注")
    print("开启标注后将检索日志中的黑号进行标注，但不会自动后置\n")
    check_task_name = ""

try:
    os.environ["ec_remode"]
except:
    remode = r"】(.*?)\*\*\*\*\*\*\*\*\*"
    pass

try:
    if os.environ["ec_remode"] != "】(.*?)\*\*\*\*\*\*\*\*\*" and os.environ["ec_check_task_name"] != "":
        remode = os.environ["ec_remode"]
        print("已配置自定义re模板\n")
    else:
        remode = r"】(.*?)\*\*\*\*\*\*\*\*\*"
        print("未配置自定义re模板")
        pass
except:
    if os.environ["ec_check_task_name"] != "":
        print("使用默认模板")
        print("有需要请在配置文件中配置\n export ec_remode=\"re模板\" 自定义模板")

try:
    os.environ["ec_blackkey"]
except:
    ec_blackkey = "黑号"
    pass

try:
    if os.environ["ec_blackkey"] != "黑号" and os.environ["ec_blackkey"] != "":
        ec_blackkey = os.environ["ec_blackkey"]
        print("已配置自定义黑号关键词\n")
    else:
        print("未配置自定义黑号关键词，使用默认关键词：黑号")
        pass
except:
    try:
        os.environ["ec_blackkey"]
    except:
        ec_blackkey = "黑号"
        print("使用默认黑号关键词：黑号")
        print("有需要请在配置文件中配置\n export ec_blackkey=\"黑号关键词\" 自定义黑号关键词")

try:
    head = int(os.environ["ec_head_cks"])
    print("已配置保留前{}位ck不检索是否黑号".format(head))
except:
    head = 6
    print("#默认只保留前6位不检索是否黑号，有需求")
    print("#请在配置文件中配置\nexport ec_head_cks=\"具体几个\" \n#更改不检索是否黑号的个数\n")

try:
    if os.environ["ec_rear_back_ck"] == "true":
        ec_rear_back_ck = True
        print("已配置自动后置标注的黑号\n")
    else:
        ec_rear_back_ck = False
        print("未配置自动后置标注的黑号，默认自动后置")
except:
    print("默认不后置标注的黑号")
    print("有需要请在配置文件中配置\n export ec_rear_back_ck=\"true\" 开启自动后置")
    print("开启后将自动后置标注的黑号\n")
    ec_rear_back_ck = False

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

requests.packages.urllib3.disable_warnings()

ql_auth_path = '/ql/config/auth.json'


def __get_token() -> str or None:
    with open(ql_auth_path, 'r', encoding='utf-8') as f:
        j_data = json.load(f)
    return j_data.get('token')


def __get__headers() -> dict:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + __get_token()
    }
    return headers


# 查询环境变量
def get_envs(name: str = None) -> list:
    params = {
        't': int(time.time() * 1000)
    }
    if name is not None:
        params['searchValue'] = name
    res = requests.get(ql_url + '/api/envs', headers=__get__headers(), params=params)
    j_data = res.json()
    if j_data['code'] == 200:
        return j_data['data']
    return []


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self):
    self.headers.update({"Authorization": "Bearer " + __get_token()})


def login(self):
    gettoken(self)


def getallenv(self, baseurl, typ):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()  # JD_COOKIE为默认的环境变量名，该变量里的值默认含pt_pin和pt_key，其他类似默认按照下面注释改
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []


def gettaskitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getlogcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/" + data[0] + "/log?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def delete(self, baseurl, typ, data):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.delete(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def insert(self, baseurl, typ, name, value, remarks):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = []
    if remarks == None:
        data_json = {
            "value": value,
            "name": name
        }
    else:
        data_json = {
            "value": value,
            "name": name,
            'remarks': remarks
        }
    data.append(data_json)
    r = self.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.json()['data']
    else:
        return False


def disable(self, baseurl, typ, ids):
    url = baseurl + typ + "/envs/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(ids))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    print("============================================")

    # 无配置时执行
    if os.environ["ec_check_task_name"] == "" and ec_rear_back_ck == True:
        exit(3)

    # 有配置时执行
    tasks = gettaskitem(s, ql_url, "api")
    for i in tasks:
        if i["name"] == check_task_name:
            log_path = i["log_path"]
            try:
                log_id = i["_id"]
            except:
                log_id = i["id"]
        elif check_task_name == "":
            exit(3)

    log = json.loads(getlogcron(s, ql_url, "api", [log_id]))["data"]
    data = log.split("\n")
    count = 0
    interval = [0]
    for i in data:
        if ec_blackkey in i:
            interval.append(count)
        count += 1

    black_pin = []
    for i in range(0, len(interval) - 1):
        x1 = interval[i]
        x2 = interval[i + 1]
        count = 0
        data1 = []
        for j in data:
            if count >= x1 and count <= x2:
                data1.append(j)
            count += 1
        data2 = ""
        for j in data1:
            data2 = data2 + j
        temp = []
        if re.findall(remode, data2) != []:
            temp.extend(re.findall(remode, data2))
        black_pin.extend(temp)

    for i in black_pin:
        print("{} {}".format(ec_blackkey, i))

    allenv = getallenv(s, ql_url, "api")

    # 备份
    tt = "备份.json"
    try:
        os.environ['ec_backup_ck']
        ec_backup_ck = os.environ['ec_backup_ck']
    except:
        ec_backup_ck = 'true'
    if ec_backup_ck == 'true' and os.path.exists('./' + tt) != True:
        with open(tt, "w", encoding="utf-8") as fp:
            json.dump(allenv, fp)
        print("已备份原有环境变量至{},有需要还原请使用二叉树还原环境变量脚本还原".format(tt))
        print("如果不需要备份，请设置export ec_backup_ck=\"false\"")
    else:
        print("上次备份文件{}还存在或已配置无需备份，本次运行不进行备份".format(tt))

    allenv = getallenv(s, ql_url, "api")
    jdcount = 0
    result_list = []
    disable_list = []
    black_list = []
    head_list = []
    he_list = []
    white_list = []
    status_black = 0
    for i in allenv:
        if "JD_COOKIE" == i["name"]:
            jdcount += 1
        else:
            he_list.append(i)
            continue
        if jdcount <= head:
            head_list.append(i)
            continue
        if i["status"] != 0:
            disable_list.append(i)
            continue
        for j in black_pin:
            black = "pt_pin=" + j + ";"
            if black in i["value"]:
                i['remarks'] = ec_blackkey
                black_list.append(i)
                status_black = 1
                continue
        if status_black == 0:
            white_list.append(i)
        else:
            status_black = 0
    he_count = len(he_list)
    result_list.extend(head_list)
    result_list.extend(white_list)

    # 去重
    tp1 = []
    value_tp = []
    for i in black_list:
        if i['value'] not in value_tp:
            tp1.append(i)
            value_tp.append(i['value'])
    black_list = tp1

    result_list.extend(black_list)
    result_list.extend(disable_list)

    # 去重
    tp1 = []
    value_tp = []
    for i in result_list:
        if i['value'] not in value_tp:
            tp1.append(i)
            value_tp.append(i['value'])
    result_list = tp1

    he_list.extend(result_list)
    result_list = he_list
    for i in allenv:
        try:
            c = delete(s, ql_url, "api", [i['_id']])
        except:
            c = delete(s, ql_url, "api", [i['id']])
    time.sleep(2)
    print(len(result_list))
    for i in result_list:
        try:
            i['remarks']
            c = insert(s, ql_url, "api", i['name'], i['value'], i['remarks'])
            if i["status"] != 0:
                try:
                    disable(s, ql_url, 'api', [c[0]['_id']])
                except:
                    disable(s, ql_url, 'api', [c[0]['id']])
        except:
            c = insert(s, ql_url, "api", i['name'], i['value'], None)
            if i["status"] != 0:
                try:
                    disable(s, ql_url, 'api', [c[0]['_id']])
                except:
                    disable(s, ql_url, 'api', [c[0]['id']])
    print("已前置非ck变量共{}个，车头ck共{}个，后置含关键词ck共{}个，后置禁用ck共{}个".format(he_count, len(head_list), len(black_list),
                                                                 len(disable_list)))
    print("============================================")
    print("脚本执行完毕")