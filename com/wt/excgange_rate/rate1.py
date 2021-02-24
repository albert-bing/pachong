# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')


# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
from com.wt.config import config
# 导入selenium的驱动接口
from selenium import webdriver
# 导入键盘操作的keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from pyvirtualdisplay import Display
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


import json

from com.wt.common import MysqlUtil

import requests
from bs4 import BeautifulSoup
import urllib3
import time

# 忽略https的安全警告
urllib3.disable_warnings()

# 创建driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # capabilities = DesiredCapabilities.CHROME.copy()
    # capabilities['acceptSslCerts'] = True
    # capabilities['acceptInsecureCerts'] = True
    driver = webdriver.Chrome(executable_path=config._CHROME_DRIVER_LINUX, options=chrome_options)
    # driver = webdriver.PhantomJS(executable_path="D:/softTools/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    return driver

def save(driver):
    driver.get("http://www.chinamoney.com.cn/chinese/bkccpr/")
    print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    date_text = soup.find_all("span",attrs={"class":"text-date"})
    date = date_text[0].text.split(" ")[0]
    source_data = soup.find_all("table", attrs={"class": "san-sheet-hover san-sheet-alternating"})

    trs = source_data[1].find_all("tr")

    all_list = []

    for i in range(1,len(trs),1):
        one_list = []
        spans = trs[i].find_all("span")
        # 货币对
        currency = spans[0].text
        # 汇率
        middle_price = spans[1].text
        # 涨跌幅
        ups_downs = spans[2].text
        # 涨跌类型
        ups_downs_tmp = spans[3]['class'][3]
        if ups_downs_tmp == 'text-down':
            ups_downs_type = '1'
        else:
            ups_downs_type = '0'
        type = '0'
        # 日期
        ymd = date
        # 货币转化顺序
        convert = '1'

        one_list.append(currency)
        one_list.append(middle_price)
        one_list.append(ups_downs)
        one_list.append(ups_downs_type)
        one_list.append(convert)
        one_list.append(type)
        one_list.append(ymd)

        all_list.append(one_list)

    for j in range(0, len(all_list), 1):
       if "美元" in  all_list[j][0] or "欧元" in all_list[j][0] or "英镑" in all_list[j][0] or "瑞士法郎" in all_list[j][0] \
           or "澳元" in all_list[j][0] or "港元" in all_list[j][0] or "日元" in all_list[j][0] or "韩元" in all_list[j][0] \
           or "新加坡元" in all_list[j][0] or "加元" in all_list[j][0] or "泰铢" in all_list[j][0]:\
        all_list[j][5] = '1'
       if "韩元" in all_list[j][0] or "泰铢" in all_list[j][0]:
           all_list[j][4] = '2'


    MysqlUtil.insert_exchange_rate_info(all_list)






if __name__ == '__main__':
    driver = create_driver()
    save(driver)

    driver.close()