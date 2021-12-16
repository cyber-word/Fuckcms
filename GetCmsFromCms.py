#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: jeremy
# github: https://github.com/cyber-word
# 公众号： 剑南道极客
import re
import sqlite3
import time
import hashlib
import requests
import user_agent

cms2 = "未识别出cms"


def GetMd5(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()


def Match_rule_for_cms(url, cms_name, path, match_pattern, options):
    global cms2
    headers = {
        'User-Agent': user_agent.generate_user_agent()
    }
    # print(url+path)
    res = requests.get(url=url + path, headers=headers, timeout=5)
    res.encoding = "utf-8"
    contents = res.content
    body = res.text
    if res.status_code == 200:
        if options == "md5":
            # print("我进入了md5的检验")
            if match_pattern == GetMd5(contents):
                cms2 = cms_name
                # print("md5" + cms2)
                # print(res.status_code)
                print(url+path)
                if cms2 != "未识别出cms":
                    return cms2
                # print(body)
                # print(contents)
        # if match_pattern == getMD5(contents):
        #     cms2 = cms_name
        if options == "keyword":
            if match_pattern in body:
                print("响应码:"+str(res.status_code))
                cms2 = cms_name
                # print("keyword" + cms2)
                print(url+path)
                if cms2 != "未识别出cms":
                    return cms2
                # print(booy)
                # print(contents)
        # if match_pattern.lower() in body.lower():
        #     cms1 = cms_name
    if cms2 != "未识别出cms":
        return cms2



def Get_rule_from_cms(url):
    # body : r.text
    # contents : r.content
    start_time = time.time()
    conn = sqlite3.connect('cms_finger.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cms_name,path,match_pattern,options FROM `cms` ")
    global cms2
    for i in range(1, 1001):
        result = cursor.fetchone()
        # result =[cms_name, path, match_pattern, options]
        if cms2 == "未识别出cms":
            Match_rule_for_cms(url, result[0], result[1], result[2], result[3])
        if cms2 != "未识别出cms":
            str1 = "cms识别结果(指纹库:cms):" + cms2
            print("\033[33m" + str1 + "\033[0m")
            cms2 = "未识别出cms"
            dir = 'fuckurl.txt'
            fp = open(dir, 'a')
            fp.write(url+" "+str1+'\n')
            fp.close()
            break
    print("\033[32m""cms识别(指纹库:cms)运行了" + str(time.time() - start_time) + "秒""\033[0m")
