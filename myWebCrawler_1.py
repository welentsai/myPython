# -*- coding: utf-8 -*-

# 讀取台銀牌告匯率, 並把當日匯率整理成tuple list

import re # regular expression 
import requests 
from bs4 import Tag
from bs4 import BeautifulSoup

# 台銀牌告匯率
result = requests.get("http://rate.bot.com.tw/xrt?Lang=zh-TW")

#print(result.status_code)
#print(result.headers)
#print(result.content)

html_doc = result.content

soup = BeautifulSoup(html_doc, 'html.parser')  # soup is instance of <bs4.BeautifulSoup>

#soup.prettify() #整理html排版

#幣別
currencyList = [tag.string.strip() for tag in soup.find_all("div", "visible-phone")]
#print(currencyList)

#現金匯率
rateCashList = [tag.string for tag in soup.find_all("td", "rate-content-cash")]
#print(rateCashList)

#即期匯率
rateSightList = [tag.string for tag in soup.find_all("td", "rate-content-sight")]
#print(rateSightList)

# using for HTML5 data-* tag
# print(soup.find_all(attrs={"data-table": "幣別"}))

# [0::2] means create subset collection of elements that (index % 2 == 0)
#print(list(rateCashList[0::2]))

# zip() -> create tuple
#現金匯率 tuple (買入, 賣出)
rateCashTuple = list(zip(rateCashList[0::2], rateCashList[1::2]))

#即期匯率 tuple (買入, 賣出)
rateSightTuple = list(zip(rateSightList[0::2], rateSightList[1::2]))

rateList = list(zip(currencyList, rateCashTuple, rateSightTuple))

for i in rateList:
	print(i)
