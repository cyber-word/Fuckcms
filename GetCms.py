#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/4
# @Author  : jeremy
# @公众号  : 剑南道极客
# @参考项目: webscan、Tidefinger
# @python 3.x
# github: https://github.com/cyber-word
import requests
import user_agent
from bs4 import BeautifulSoup
import lxml
import urllib
from urllib.parse import urlparse
import re
import threading
import sqlite3
import time
from queue import Queue
import GetCmsFromTide
import GetCmsFromCms


# 创建一个WebInfo类用来存储扫描到的信息
class WebInfo:
    def __init__(self, domain, title, http_server, language, set_Cookie, X_Powered_By, cms, body, header):
        self.header = header
        self.body = body
        self.set_Cookie = set_Cookie
        self.X_Powered_By = X_Powered_By
        self.language = language
        self.http_server = http_server
        self.domain = domain
        self.title = title
        self.cms = cms

    def print(self):
        print("\033[32m""domain:" + self.domain + "\033[0m")
        print("\033[33m""title:" + self.title + "\033[0m")
        print("\033[34m""http_server:" + self.http_server + "\033[0m")
        print("\033[35m""language:" + self.language + "\033[0m")
        print("\033[36m""X-Powered-By:" + self.X_Powered_By + "\033[0m")
        # print(self.__dict__) 原本用作遍历输出所有属性


def GetWebInfo(queue, Dbs):
    while queue.empty() is not True:
        url = queue.get()
        headers = {
            'User-Agent': user_agent.generate_user_agent()
        }
        try:
            r = requests.get(url=url, headers=headers, timeout=5)
            print("-" * 25+"扫描对象"+"-"*25)
            print(url)
            r.encoding = 'unicode'
            headers = str(r.headers)
            bodys = r.text
            contents = r.content
            try:
                title = BeautifulSoup(bodys, 'lxml').title.text.strip()
            except Exception as error:
                title = "暂未识别出title"
            try:
                Cookie = r.headers['Coolie']
            except Exception as error:
                Cookie = "暂未识别，可能是当前页面没有cookie"
            try:
                Server = r.headers['Server']
            except Exception as error:
                Server = "暂未识别出当前页面服务器"
            domain = urlparse(url).netloc
            domain = domain.replace('www.', '')
            ThisWebInfo = WebInfo(domain, title, Server, "暂未识别当前页面语言", Cookie,
                                  "未识别出x-powered-by", "未识别出cms,但可能x-powered-by中有", bodys, headers)
            # 识别语言
            if 'X-Powered-By' in r.headers:
                ThisWebInfo.X_Powered_By = r.headers['X-Powered-By']
            if 'set-Cookie' in r.headers:
                ThisWebInfo.set_Cookie = r.headers['Set-Cookie']
            if 'Cookie' in r.headers:
                ThisWebInfo.set_Cookie = r.headers['Set-Cookie']
            if "PHPSSIONID" in ThisWebInfo.set_Cookie:
                ThisWebInfo.language = "PHP"
            if "JSESSIONID" in ThisWebInfo.set_Cookie:
                ThisWebInfo.language = "JAVA"
            if "ASP.NET" in ThisWebInfo.X_Powered_By or "ASPSESS" in ThisWebInfo.set_Cookie or "ASP.NET" in ThisWebInfo.set_Cookie:
                ThisWebInfo.language = "ASP.NET"
            if "JBoss" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "JAVA"
            if "Servlet" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "JAVA"
            if "Next.js" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "NODEJS"
            if "Express" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "NODEJS"
            if "PHP" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "PHP"
            if "JSF" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "JAVA"
            if "WP" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "PHP"
            if "enduro" in ThisWebInfo.X_Powered_By:
                ThisWebInfo.language = "NODEJS"
            try:
                if Dbs == "tide":
                    ThisWebInfo.print()
                    print("\033[32m使用tide指纹库识别的结果:\033[0m")
                    GetCmsFromTide.Get_rule_from_tide(title, headers, bodys)
                if Dbs == "cms":
                    ThisWebInfo.print()
                    print("\033[32m使用cms指纹库识别的结果:\033[0m")
                    GetCmsFromCms.Get_rule_from_cms(url)
                if Dbs == "all":
                    ThisWebInfo.print()
                    print("\033[32m使用tide指纹库识别的结果:\033[0m")
                    GetCmsFromTide.Get_rule_from_tide(title, headers, bodys)
                    print("\033[32m使用cms指纹库识别的结果:\033[0m")
                    GetCmsFromCms.Get_rule_from_cms(url)
            except Exception as error:
                pass
            # 识别网站语言
        except Exception as error:
            print("-"*50)
            print("连接不到该网站:" + url)
        queue.task_done()
    # print(r.headers)  # 获得响应头信息

# GetWebInfo("http://www.lcnjj.cn/")
# >> `{'X-Processed-Time': '0.000617980957031', 'Connection': 'keep-alive', 'Via': '1.1 vegur',
#      'Content-Length': '268', 'X-Powered-By': 'Flask', 'Date': 'Thu, 23 Nov 2017 04:13:40 GMT',
#      'Server': 'meinheld/0.6.1', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true',
#      'Content-Type': 'application/json'}
# >> application / json
# >> 268
