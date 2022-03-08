# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
import requests, time
from lxml import html
from selenium.webdriver import Firefox, FirefoxOptions
import re


opt = FirefoxOptions()
opt.headless = True
driver = Firefox(executable_path='geckodriver.exe', options=opt)

def get_urls():
        headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-cn",
                "Connection": "keep-alive",
                # "Cookie": cookie,
                "Host": "www.smzdm.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
        }
        r = requests.get("https://www.smzdm.com/p/39432999/", headers=headers, allow_redirects=False)
        cookie = requests.utils.dict_from_cookiejar(r.cookies)
        headers.update({"Cookie": str(cookie)})
        time.sleep(1)
        res = requests.get(r.url, headers=headers, allow_redirects=False)
        tree = html.fromstring(res.text)
        shop_list = tree.xpath('/html/body/div[1]/div/section[1]/article/div[1]/div[3]/article/div[3]/table/tbody/tr')
        return shop_list
try:
        shop_list = get_urls()
except:
        try:
                time.sleep(3)
                shop_list = get_urls()
        except:
                try:
                        time.sleep(5)
                        shop_list = get_urls()
                except:
                        exit(3)


shop_urls = []
shop_title = []
for i in shop_list[1:]:
        shop_urls.append(i.xpath("./td[1]/a/@href")[0])
        shop_title.append(i.xpath("./td//text()")[1])
shopId = []
for i, j in zip(shop_urls, shop_title):
        driver.get(i)
        time.sleep(3)
        real_url = str(driver.current_url)
        driver.delete_all_cookies()
        Id = re.findall(r"https://shop.m.jd.com/\?shopId=(.*?)&", real_url)
        print(real_url)
        shopId.append(Id)
        print(i)
        print(j)
        print(Id)
        print("---------------------")


