# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code
import pymysql

host = 'localhost'
password = '123456'
port = 3306
import paramiko
import time
from urllib.parse import quote


def test1():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("120.26.146.183", "6143", "czsqauser", "#UIOP2wsxcde45", timeout=5)
    sftp_client = client.open_sftp()
    print(sftp_client.listdir('./fm02'))
    date_str = time.strftime('%Y%m%d', time.localtime(time.time()))
    remote_file = sftp_client.open("/fm02/DMS-FM-DFM02-" + date_str + "-01.csv", 'r')
    # 读取一行数据，并且去掉换行符，读两次是因为可以去掉表头
    line = remote_file.readline().strip()
    line = remote_file.readline().strip()
    data = []
    # 循环读取文件信息--按行读取
    while line:
        one_data = line.split(",")
        data.append(one_data)
        line = remote_file.readline().strip()

    for i in range(0, 20):
        print(data[i])


def select_demo():
    db = pymysql.connect(host=host, user='root', password=password, port=port, db='test1')
    cursor = db.cursor()
    # 省名称、境外输入、日期、确诊(累计)人数、治愈人数、死亡人数、新增人数
    sql = "SELECT t1.lunar_calendar,t1.y_day from date_yellow_calendar t1 left JOIN date_calendar_full_scale t2 on t1.y_day = t2.date_id where t1.y_day >= '20300101' and t1.y_day <= '20301231' and t2.date_id  >= '20300101'  and t2.date_id <= '20301231';"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return result

def update_demo(data):
    db = pymysql.connect(host=host, user='root', password=password, port=port, db='test1')
    cursor = db.cursor()
    sql = "update date_calendar_full_scale set lunar = %s where date_id = %s"
    cursor.execute(sql,data)
    # cursor.close()
    db.commit()
    db.close()

if __name__ == '__main__':
    # print(time.strftime('%Y%m%d', time.localtime(time.time())))
    #
    # pro_text = quote("北京")
    # print(pro_text)
    # create_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    # print(create_time)

    result = select_demo()

    for i in range(0,len(result),1):
        update_demo(result[i])

    print(result)
