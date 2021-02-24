# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
import sys
sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
from crawler.com.wt.config import config
# 导入selenium的驱动接口
from selenium import webdriver
# 导入chrome选项
from selenium.webdriver.chrome.options import Options
import json
from crawler.com.wt.common import MysqlUtil
import requests
from bs4 import BeautifulSoup
import urllib3
import time
# 忽略https的安全警告
urllib3.disable_warnings()



def save():
    headers = {
        "Origin": "http://www.chinamoney.com.cn",
        "Referer": "http://www.chinamoney.com.cn/chinese/bkccpr/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Host": "www.chinamoney.com.cn"}
    data = requests.get("http://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/ccpr.json?t=1614073351666",verify=False,headers=headers)

    dick_data = json.loads(data.text)
    # 获取日期
    date = dick_data['data']['lastDate'].split(" ")[0]
    records = dick_data['records']
    all_list = []
    for i in range(0,len(records),1):
        one_list = []
        currency_name = records[i]['vrtName']
        middle_price = records[i]['price']
        ups_downs = records[i]['bp']
        if  records[i]['bpDouble'] > 0:
            ups_downs_type = 0
        else:
            ups_downs_type = 1
        # 货币转化顺序
        convert = '1'
        type= '0'

        one_list.append(currency_name)
        one_list.append(middle_price)
        one_list.append(ups_downs)
        one_list.append(ups_downs_type)
        one_list.append(convert)
        one_list.append(type)
        one_list.append(date)
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
    save()

