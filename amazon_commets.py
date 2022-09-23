# -*- coding: utf-8 -*-
"""
@Time ： 2022/3/17 17:31
@Auth ： wes
@File ：amazon_commets.py
@IDE ：PyCharm
@email：2934218525@qq.com

"""
import time

import requests
import re
from selenium.webdriver.common.by import By
import utility.generate_headers
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
#读取需要的；链接
with open("read_link.txt","r",encoding = "utf-8") as file:
    s = file.read().split("\n")
#创建浏览器驱动
driver = webdriver.Chrome(executable_path='chromedriver.exe')
num = 0
#遍历链接进行需要的操作
for i in s:
    # if num==0:
    #     num += 1
    #     continue
    if len(i)<5:
        continue
    print(i)
    sign =""""""
    try:
        #提取sign值
        sign = re.findall("dp/(.*?)",i)[0]
    except:
       pass
    if len(sign) <5:
        sign = re.findall("dp/(.*?)\?",i)[0]
    print("当前爬取的id 是: {}".format(sign))

    csv_write = csv.writer(open(f"{sign}.csv","w",newline="",encoding="utf-8"))
    csv_write.writerow(["user","content","times","scores"])
    num0 = 1
    fore_url = i.split(r"/dp/")[0]
    print(fore_url)
    for j in range(1,150):
        if num0 == 1:
            url = f"{fore_url}/product-reviews/{sign}/ref=cm_cr_getr_d_paging_btm_prev_{j}?ie=UTF8&reviewerType=all_reviews&pageNumber={j}"
        else:
            url = f"{fore_url}/product-reviews/{sign}/ref=cm_cr_arp_d_paging_btm_next_{num0}?ie=UTF8&reviewerType=all_reviews&pageNumber={num0}"
        print(url)
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content,'lxml')
        names = []
        comments = []
        scores = []
        times = []
        all = soup.find_all(attrs = {"data-hook":"review"})

        for h in all:
            h = str(h)
            print(h)
            h = h.replace("\n","")
            h = h.replace("   ","")
            h = h.replace("  ","")
            scores.append(re.findall('a-icon-alt">(.*?)</spa',h)[0].split(" ")[0])
            times.append(re.findall('data-hook="review-date">(.*?)</spa',h)[0])
            names.append(re.findall('span class="a-profile-name">(.*?)</span>',h)[0])
            cuts = h.split('review-text-content" data-hook="review-body"><span>')[-1].split('review-comments comments-f')[0].split("<")[0]
            comments.append(cuts)




        need = []
        if len(names)==0:
            if "Tut uns Leid!" in content:
                break
            if "a-size-medium view-point-title" not in content:
                while True:
                    if "a-size-medium view-point-title" not in driver.page_source:
                        j-=1
                        continue
                    break
                    time.sleep(1)


        print(len(names),len(scores),len(times),len(comments))
        if len(names) ==0:
            break

        for i in range(len(comments)):
            need.append([names[i],comments[i],times[i],scores[i]])
            print(names[i],scores[i],times[i],comments[i])

        print(len(names),len(scores),len(times),len(comments))
        print(url)
        csv_write.writerows(need)
