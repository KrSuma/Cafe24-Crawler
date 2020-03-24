# -*-coding:utf-8

'''
1. removed redundant libraries
2. combine functions into class

'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import csv
import os
import socket
import sys

baseurl = "https://www.envylook.com"

envydata = []


# 이미지로 저장


def saveimg(filename, imgUrl, retries=3):
    def _progress(count, block_size, total_size):
        sys.stderr.write('\r>> Downloading %s %.1f%%' % (
            imgUrl, float(count * block_size) / float(total_size) * 100.0))
        sys.stderr.flush()

    while retries > 0:
        try:
            urllib.request.urlretrieve(imgUrl, filename + '.jpg', _progress)
            break
        except urllib.UrlError:
            retries -= 1
            print("Exception raised: Retrying ...")
            print("Retries left :" + retries)
            continue


def productdetail(no, url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.select("meta[property]")
    explain = soup.select_one("#SMS_TD_summary")
    option = soup.select("#product_option_id1 option,#product_option_id2 option")
    images = soup.select("#prdDetail center img")
    temp = [no]

    for d in info:
        s = d.get("content")
        temp.append(s)
        if "jpg" in s:
            saveimg(str(no) + "-" + "title", s)
        print(s, end="\n")

    temp.append(explain.text)
    print(explain.text)
    n = 0
    for d in option:
        s = d.get("value")
        if '*' in s:
            pass
        else:
            temp.append(s)
            print(s, end="\n")
            n += 1

    for i in range(20 - n):
        temp.append("")
        print(i)

    imgfilecount = 1
    for d in images:
        s = d.get("src")
        if '//' in s:
            temp.append(s)
            saveimg(str(no) + "-" + str(imgfilecount), 'http:' + s)
            print('http:' + s, end="\n")
        else:
            temp.append(baseurl + s)
            saveimg(str(no) + "-" + str(imgfilecount), baseurl + s)
            print(baseurl + s, end="\n")
        imgfilecount += 1
    envydata.append(temp)


def envylookcategory(cate_no, page_no):
    tailurl = f"/product/list2.html?cate_no={cate_no}&page={page_no}"
    url = baseurl + tailurl

    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.select(".thumbnail a")
    info2 = soup.find('meta', {'property': 'og:description'})
    info3 = soup.find('meta', {'property': 'og:site_name'})

    dirname = info3.get("content") + "_" + info2.get("content") + "_cate" + str(cate_no) + "_page" + str(page_no)
    os.mkdir(dirname)
    os.chdir(dirname)

    n = 1
    for d in info:
        s = baseurl + d.get("href")
        os.mkdir(str(n))
        os.chdir(str(n))
        productdetail(n, s)
        os.chdir("..")
        print(str(n) + "번째 " + s, end="\n")
        n += 1

    return dirname


cate_no = input("카테고리번호를 입력하세요 : ")
page_no = input("페이지번호를 입력하세요 : ")
socket.setdefaulttimeout(30)
result = envylookcategory(cate_no, page_no)

csvname = result + ".csv"

with open(csvname, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['폴더번호', '주소', '상품명', '브랜드', '종류', '타이틀이미지', '정상가', '통화', '할인가', '통화', '요약설명', '옵션1', '옵션2', '옵션3', '옵션4',
         '옵션5', '옵션6', '옵션7', '옵션8', '옵션9', '옵션10', '옵션11', '옵션12', '옵션13', '옵션14', '옵션15', '옵션16', '옵션17', '옵션18',
         '옵션19', '옵션20', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지',
         '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지'])
    writer.writerows(envydata)

# for d in info:
#     data = str(d)
#     if "og:title" in data:
#         print(data)
#     if "og:image" in data:
#         print(data)
