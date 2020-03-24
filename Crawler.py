# -*-coding:utf-8

"""
1. removed redundant libraries
2. combine functions into class
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import csv
import os
import socket
import sys

base_url = "https://www.envylook.com"

envydata = []


# 이미지로 저장


def save_img(filename, imgUrl, retries=3):
    def _progress(count, block_size, total_size):
        sys.stderr.write('\r>> Downloading %s %.1f%%' % (
            imgUrl, float(count * block_size) / float(total_size) * 100.0))
        sys.stderr.flush()

    while retries > 0:
        try:
            urllib.request.urlretrieve(imgUrl, filename + '.jpg', _progress)
            break
        except urllib.error.URLError:  # specified the exception, added retries counter.
            retries -= 1  # refactored
            print("Exception raised: Retrying ...")
            print("Retries left : " + retries)
            continue


def product_detail(no, url):
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
            save_img(str(no) + "-" + "title", s)
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

    imgfile_count = 1
    for d in images:
        s = d.get("src")
        if '//' in s:
            temp.append(s)
            save_img(str(no) + "-" + str(imgfile_count), 'http:' + s)
            print('http:' + s, end="\n")
        else:
            temp.append(base_url + s)
            save_img(str(no) + "-" + str(imgfile_count), base_url + s)
            print(base_url + s, end="\n")
        imgfile_count += 1
    envydata.append(temp)


def envylook_category(category, page):  # Local variable name hid the variable defined in the outer space.
    tail_url = f"/product/list2.html?cate_no={category}&page={page}"
    url = base_url + tail_url

    '''
    urllib not only opens http:// or https:// URLs, but also ftp:// and file://. 
    with this it might be possible to open local files on the executing machine which might be a security risk 
    if the URL to open can be manipulated by an external user.
    '''

    if url.lower().startswith('http'):
        html = urlopen(url).read()
    else:
        raise ValueError from None

    soup = BeautifulSoup(html, 'html.parser')
    info = soup.select(".thumbnail a")
    info2 = soup.find('meta', {'property': 'og:description'})
    info3 = soup.find('meta', {'property': 'og:site_name'})

    dirname = info3.get("content") + "_" + info2.get("content") + "_cate" + str(category) + "_page" + str(page)
    os.mkdir(dirname)
    os.chdir(dirname)

    n = 1
    for d in info:
        s = base_url + d.get("href")
        os.mkdir(str(n))
        os.chdir(str(n))
        product_detail(n, s)
        os.chdir("..")
        print(str(n) + "번째 " + s, end="\n")
        n += 1

    return dirname


cate_no = input("카테고리번호를 입력하세요 : ")
page_no = input("페이지번호를 입력하세요 : ")
socket.setdefaulttimeout(30)
result = envylook_category(cate_no, page_no)

csv_name = result + ".csv"

with open(csv_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['폴더번호', '주소', '상품명', '브랜드', '종류', '타이틀이미지', '정상가', '통화', '할인가', '통화', '요약설명',
         '옵션1', '옵션2', '옵션3', '옵션4', '옵션5', '옵션6', '옵션7', '옵션8', '옵션9', '옵션10', '옵션11', '옵션12',
         '옵션13', '옵션14', '옵션15', '옵션16', '옵션17', '옵션18', '옵션19', '옵션20',
         '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지',
         '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지', '상세이미지'
         ])
    writer.writerows(envydata)

# for d in info:
#     data = str(d)
#     if "og:title" in data:
#         print(data)
#     if "og:image" in data:
#         print(data)
