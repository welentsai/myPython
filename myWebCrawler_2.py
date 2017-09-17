# -*- coding: utf-8 -*-

# 讀取國泰牌告匯率, 並把當日匯率整理成tuple list

import re # regular expression 
import requests 
from bs4 import Tag
from bs4 import BeautifulSoup

# 台銀牌告匯率
result = requests.get("https://www.cathaybk.com.tw/cathaybk/personal/exchange/product/currency-billboard/")

#print(result.status_code)
#print(result.headers)
#print(result.content)

html_doc = result.content

soup = BeautifulSoup(html_doc, 'html.parser')  # soup is instance of <bs4.BeautifulSoup>

#print(soup.prettify()) #整理html排版

# tag.get_text() => the text part of a document or tag
rateList = [tag.get_text().strip() for tag in soup.find("table", "table-rate").find_all("td")]

# [0::3] means create subset collection of elements that (index % 3 == 0)
# rateList[0::3] => 幣別
# rateList[1::3] => Bank Buy
# rateList[2::3] => Bank Sell
rateTable = list(zip(rateList[0::3], rateList[1::3], rateList[2::3]))

for row in rateTable:
	print(row)
