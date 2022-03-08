# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树查脚本网络链接');
'''

import time
import json
import re
import os

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")

requests.packages.urllib3.disable_warnings()


def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path, file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                list.append(h[1])
        return list


def read_ex(or_list):
    # 加载远程依赖剔除依赖文件的检索
    try:
        res1 = requests.get("https://jihulab.com/spiritlhl/dependence_scripts/-/raw/master/contents.json").json()
        time.sleep(5)
        res2 = requests.get("https://jihulab.com/spiritlhl/dependence_scripts/-/raw/master/utils.json").json()
        time.sleep(4)
        res3 = requests.get("https://jihulab.com/spiritlhl/dependence_scripts/-/raw/master/function.json").json()
        try:
            res1["documentation_url"]
            return
        except:
            try:
                res2["documentation_url"]
                return
            except:
                try:
                    res3["documentation_url"]
                    return
                except:
                    pass


    except:
        print("网络波动，稍后尝试")
        time.sleep(5)
        try:
            res1 = requests.get("https://jihulab.com/spiritlhl/dependence_scripts/-/raw/master/contents.json").json()
            time.sleep(5)
            res2 = requests.get("https://jihulab.com/spiritlhl/dependence_scripts/-/raw/master/utils.json").json()
            time.sleep(4)
            res3 = requests.get("https://jihulab.com/spiritlhl/dependence_scripts/-/raw/master/function.json").json()
            try:
                res1["documentation_url"]
                return
            except:
                try:
                    res2["documentation_url"]
                    return
                except:
                    try:
                        res3["documentation_url"]
                        return
                    except:
                        pass
        except:
            print("网络问题无法获取仓库文件列表，停止加载远程文件剔除依赖文件，直接本地检索")

    for i in res1:
        or_list.append(i["name"])
    for i in res2:
        or_list.append(i["name"])
    for i in res3:
        or_list.append(i["name"])
    or_list = list(set(or_list))
    return or_list


if __name__ == '__main__':
    # 获取主青龙任务

    # script根目录默认存在的文件夹，放入其中的文件夹不再检索
    or_list_o = ['node_modules', '__pycache__', 'utils', '.pnpm-store', 'function', 'tools', 'backUp', '.git', '.idea',
                 'fake_keys.txt', 'ec_config.txt']
    try:
        if os.environ["ec_read_dep"] == "true":
            print("已配置远程加载依赖文件名不查询\n")
            or_list = read_ex(or_list_o)
            if or_list == None:
                or_list = or_list_o
    except:
        print("#未配置远程加载依赖文件名不查询，有需要可添加配置")
        print("export ec_read_dep=\"true\"\n")
        or_list = or_list_o

    # 白名单
    try:
        expect_list = os.environ["ec_white_list"].split("@")
        print("已配置白名单\n")
    except:
        print("#未配置白名单，默认查询所有链接，有需要可添加配置")
        print("export ec_white_list=\"各种白名单关键词，用@分隔\"\n")
        expect_list = ["http://xxxx.xxxx.xxx/"]

    # 黑名单(屏蔽词)
    try:
        keys = os.environ["ec_black_keys"].split("@")
        print("已配置黑名单(屏蔽词)\n")
    except:
        print("#未配置黑名单，默认查询所有链接，有需要可添加配置")
        print("export ec_black_keys=\"各种黑名单屏蔽词，用@分隔\"\n")
        keys = ["http://xxxx.xxxx.xxx/"]
    keys = list(set(keys))

    print("============ 获取根目录脚本文件内容 ============\n")

    # 根目录
    dir_list = list(set(os.listdir("../") + os.listdir("./")) - set(or_list))
    data_script_list = []
    name_root = []
    if "db" not in os.listdir("../"):
        for i in dir_list:
            if i not in or_list and i[0:9] != "spiritLHL":
                try:
                    with open("../" + i, "r", encoding="utf-8") as f:
                        data_script_list.append(f.read())
                    name_root.append(i)
                except:
                    pass
    else:
        for i in dir_list:
            if i not in or_list and i[0:9] != "spiritLHL":
                try:
                    with open(i, "r", encoding="utf-8") as f:
                        data_script_list.append(f.read())
                    name_root.append(i)
                except:
                    pass

    # 筛出网址
    net_list = {}
    for i, k in zip(data_script_list, name_root):
        net_list[k] = []

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\"https://(.*?)\"", i)
        for j in temp:
            net_list[k].append("https://" + j)

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\"http://(.*?)\"", i)
        for j in temp:
            net_list[k].append("http://" + j)

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\'https://(.*?)\'", i)
        for j in temp:
            net_list[k].append("https://" + j)

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\'http://(.*?)\'", i)
        for j in temp:
            net_list[k].append("http://" + j)

    # 去重
    for i in net_list:
        net_list[i] = list(set(net_list[i]))
        for j in net_list[i]:
            if ".jd.com" in j or "." not in j or j in expect_list:
                net_list[i].remove(j)

    print()
    print("查询脚本，筛选网址中")
    print()

    # 输出找到的链接
    ## 根目录
    print("根目录文件\n")
    count_root = 0
    count_root_key = 0
    for k in net_list:
        if net_list[k] == []:
            print(k)
            print("无链接\n")
        else:
            print(k)
            for l in net_list[k]:
                print(l)
                count_root += 1
            print()
            for l in net_list[k]:
                for j in keys:
                    if j in l:
                        count_root_key += 1

    print()
    print("查到链接个数： {}".format(count_root))

    print()
    print("包含屏蔽词链接个数： {}".format(count_root_key))

    print("============ 根目录查询完毕 ============\n\n\n")

    ###################################################################################################

    # 仓库文件夹
    # 获取副青龙仓库目录脚本名字典
    tp_list = traversalDir_FirstDir("../")
    if "config" not in tp_list and "db" not in tp_list:
        zpath_list = traversalDir_FirstDir("../")
        try:
            zpath_list.remove("spiritLHL_qinglong_auto_tools")
        except:
            pass
        zpath_list = list(set(zpath_list) - set(or_list))
        dict_name = {}
        for i in zpath_list:
            dict_name[i] = []
            for j in list(set(os.listdir("../" + i)) - set(or_list)):
                if str(i)[0:9] != "spiritLHL":
                    dict_name[i].append(j)
    else:
        zpath_list = traversalDir_FirstDir("./")
        try:
            zpath_list.remove("spiritLHL_qinglong_auto_tools")
        except:
            pass
        zpath_list = list(set(zpath_list) - set(or_list))
        dict_name = {}
        for i in zpath_list:
            dict_name[i] = []
            for j in list(set(os.listdir("./" + i)) - set(or_list)):
                if str(i)[0:9] != "spiritLHL":
                    dict_name[i].append(j)

    # 查询
    if "config" not in tp_list and "db" not in tp_list:
        dict_net_list = {}
        for i in dict_name:
            dict_net_list[i] = {}
            for j in dict_name[i]:
                dict_net_list[i][j] = []
                with open("../" + i + "/" + j, "r", encoding="utf-8") as fp:
                    k = fp.read()
                    temp = re.findall(r"\"https://(.*?)\"", k)
                    for l in temp:
                        dict_net_list[i][j].append("https://" + l)

                    temp = re.findall(r"\"http://(.*?)\"", k)
                    for l in temp:
                        dict_net_list[i][j].append("http://" + l)

                    temp = re.findall(r"\'https://(.*?)\'", k)
                    for l in temp:
                        dict_net_list[i][j].append("https://" + l)

                    temp = re.findall(r"\'http://(.*?)\'", k)
                    for l in temp:
                        dict_net_list[i][j].append("http://" + l)

                    # 去重
                    dict_net_list[i][j] = list(set(dict_net_list[i][j]))
                    for m in dict_net_list[i][j]:
                        if ".jd.com" in m or "." not in m or m in expect_list:
                            dict_net_list[i][j].remove(m)
    else:
        dict_net_list = {}
        for i in dict_name:
            dict_net_list[i] = {}
            for j in dict_name[i]:
                dict_net_list[i][j] = []
                with open("./" + i + "/" + j, "r", encoding="utf-8") as fp:
                    k = fp.read()
                    temp = re.findall(r"\"https://(.*?)\"", k)
                    for l in temp:
                        dict_net_list[i][j].append("https://" + l)

                    temp = re.findall(r"\"http://(.*?)\"", k)
                    for l in temp:
                        dict_net_list[i][j].append("http://" + l)

                    temp = re.findall(r"\'https://(.*?)\'", k)
                    for l in temp:
                        dict_net_list[i][j].append("https://" + l)

                    temp = re.findall(r"\'http://(.*?)\'", k)
                    for l in temp:
                        dict_net_list[i][j].append("http://" + l)

                    # 去重
                    dict_net_list[i][j] = list(set(dict_net_list[i][j]))
                    for m in dict_net_list[i][j]:
                        if ".jd.com" in m or "." not in m or m in expect_list:
                            dict_net_list[i][j].remove(m)

    # 输出找到的链接
    count_dict = 0
    count_dict_key = 0
    for i in dict_net_list:
        print("====== 查询 {} 对应文件夹 =========\n".format(i))
        print("{}文件夹文件\n".format(i))
        for j in dict_net_list[i]:
            if dict_net_list[i][j] == []:
                print(j)
                print("无链接\n")
            else:
                print(j)
                for k in dict_net_list[i][j]:
                    print(k)
                    count_dict += 1
                print()
                for k in dict_net_list[i][j]:
                    for l in keys:
                        if l in k:
                            count_dict_key += 1

        print("{}文件夹内查到链接个数： {}\n".format(i, count_dict))

        print("{}文件夹内包含屏蔽词链接个数： {}\n".format(i, count_dict_key))

        print("====== {}对应文件夹查询完毕 =========\n".format(i))

    print()
    print("查询结束")













