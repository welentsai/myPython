# -*- coding: utf-8 -*-

# TWSE 台灣證交所
# 首頁 > 交易資訊 > 盤後資訊 > 個股日成交資訊 > 0050

import json
import requests
import time

#fulluri = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20170914&stockNo=0050"

uri = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="

# 回傳該年 1 ~ 12 月份的
def getDateList(year):
	_mLi = []
	for m in range(12):
		_mLi.append(str(year) + str(m+1).zfill(2) + '01')
		#print(str(year) + str(m+1).zfill(2) + d)
	return _mLi

# Get Daily Stock  Trade Info from TWSE
def getStockTradeInfo(date, stkNo):
	_uri = uri + date + '&stockNo=' + stkNo # 組成完整的 URI
	result = requests.get(_uri)
	jsonObj = json.loads(result.content)	
	for row in jsonObj['data']:
		#print(list(zip(jsonObj['fields'], row)))
		print(row)
	return

dateList = getDateList(2016)

for date in dateList:
	getStockTradeInfo(date, '0050')
	time.sleep(0.1) # time delay for 0.1 second	