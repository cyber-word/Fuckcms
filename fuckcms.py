#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: jeremy
# github: https://github.com/cyber-word
# 公众号： 剑南道极客
import argparse
import GetCms
import sys
import threading
from threading import Thread  # 引入多线程
from queue import Queue  # 引入队列机制
import time
import banner

# Check py version
def CheckVersion():
    PythonVersion = sys.version.split()[0]
    if PythonVersion <= "3":
        exit('Need Python3.x')


CheckVersion()
print(banner.banner())
# Get argparse
parser = argparse.ArgumentParser()
parser.description = 'please enter -u (required) -f (optional) -t (optional)'
parser.add_argument("-u", "--url", help="this is a url to be scanned", dest="url", type=str, default="no input url")
parser.add_argument("-f", "--file", help="this is a url list to be scanned", dest="path", type=str, default="no input "
                                                                                                            "file")
parser.add_argument("-t", "--thread", help="this is the numeber of threads to be used", dest="ThreadNum", type=int,
                    default=10)
parser.add_argument("-d", "--dbs", help="this is the finger dbs that to be used", dest="FingerDbs", type=str,
                    default="all")
args = parser.parse_args()
print("\033[35m""*"*50+"\033[0m")
print("\033[33m""url: "+args.url+"\033[0m")
print("\033[33m""file path: "+args.path+"\033[0m")
print("\033[33m""scanThreadNum: "+str(args.ThreadNum)+"\033[0m")
print("\033[33m""Finger dbs: "+args.FingerDbs+"\033[0m")
print("\033[35m""*"*50+"\033[0m")
if args.path == "no input file":
    if args.url != "no input url":
        if args.FingerDbs == "all":
            queue = Queue()
            queue.put(args.url)
            for i in range(1, args.ThreadNum):
                thread = Thread(target=GetCms.GetWebInfo, args=(queue,args.FingerDbs))
                thread.start()
            queue.join()
    else:
        print("请重新输入")
else:
    queue = Queue()
    txt_path = args.path  # 要扫描的网站存放路径
    f = open(txt_path)
    data_lists = f.readlines()  # 读出的是str类型
    start_time = time.time()
    for data in data_lists:
        data1 = data.strip('\n')  # 去掉开头和结尾的换行符
        queue.put(data1)  # 将url读取到queue中
        # getinfo.GetWebInfo(data1)
    for i in range(1, args.ThreadNum):
        thread = Thread(target=GetCms.GetWebInfo, args=(queue,args.FingerDbs))
        thread.start()
    queue.join()
    print("\033[32m""扫描完毕共花费了:" + str(time.time() - start_time) + "秒""\033[0m")
