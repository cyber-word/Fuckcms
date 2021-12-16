#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: jeremy
# github: https://github.com/cyber-word
# 公众号： 剑南道极客
import re
import sqlite3
import time


cms1 = "未识别出cms"


def Match_rule_for_tide(key, title, header, body):
    re_header = re.compile(r'header="(.*)"')
    re_body = re.compile(r'body="(.*)"')
    re_title = re.compile(r'title="(.*)"')
    global cms1
    if "title=" in key:
        if re.findall(re_title, key)[0].lower() in title.lower():
            cms1 = re.findall(re_title, key)[0]
    if "header=" in key:
        if re.findall(re_header, key)[0].lower() in header.lower():
            cms1 = re.findall(re_header, key)[0]
    if "body=" in key:
        if re.findall(re_body, key)[0].lower() in body.lower():
            cms1 = re.findall(re_body, key)[0]
    if cms1 !="未识别出cms":
        return cms1


def Get_rule_from_tide(url, title, header, body):
    start_time = time.time()
    conn = sqlite3.connect('cms_finger.db')
    cursor = conn.cursor()
    cursor.execute("SELECT keys  FROM `tide` ")
    global cms1
    for i in range(1, 1001):
        result = cursor.fetchone()
        if cms1 == "未识别出cms":
            Match_rule_for_tide(result[0], title, header, body)
        if cms1 != "未识别出cms":
            str1 = "cms识别结果(指纹库:tide):"+Match_rule_for_tide(result[0], title, header, body)
            print("\033[33m"+str1+"\033[0m")
            cms1 = "未识别出cms"
            dir = 'fuckurl.txt'
            fp = open(dir, 'a')
            fp.write(url+" "+str1+'\n')
            fp.close()
            break
    print("\033[32m""运行了"+str(time.time() - start_time)+"秒""\033[0m")
