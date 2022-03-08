# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
#觉得不错麻烦点个star谢谢


from selenium import webdriver
import time
import random
import re

username = ''#用户名
password = ''#密码
address = ''#青龙2.8登陆地址：https：//xxxx：xxxx/
#ck形式，默认是形式一，有需要的自己注释掉形式一使用形式二

##形式一：ck.txt文件中一行一个ck
with open('ck.txt','rb') as fp:
    temp = fp.read().splitlines()
ck = []
for i in temp:
    ck.append(str(i).replace("b'","").replace("'",""))

'''
##形式二：ck1&ck2&ck3的形式
data = '这里填ck1&ck2的形式'
ck = data.split('&')
'''

driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')
driver.get(address)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="username"]').send_keys(f'{username}\n')
time.sleep(0.3)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(f'{password}')
time.sleep(0.3)
driver.find_element_by_xpath('/html/body/div/div/div/div[2]/form/div[3]/button').click()
driver.get(f'{address}env')
time.sleep(0.3)
for i in ck:
    driver.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/main/div/div[1]/div/div/span/button/span').click()
    time.sleep(0.6)
    driver.find_element_by_xpath('//*[@id="env_modal_name"]').send_keys("JD_COOKIE")
    driver.find_element_by_xpath('//*[@id="env_modal_value"]').send_keys(f"{i}")
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]').click()
    time.sleep(0.5)
print('Success')


