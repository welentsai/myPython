# -*- coding: utf-8 -*-

import re # regular expression 
import requests 
import json

uri = "https://stock-ai.com/eomDataQuery"

payload = {
	'a':'c',
	'showType':'Value',
	#symbolCode:"twIndexScore", # 台灣景氣對策信號(分數)
	#symbolCode:"marketCapitalization", # 台灣台股上市公司當月總市值
	'symbolCode':'twA02', # M1B 貨幣總計數 (= M1A ＋ 活期儲蓄存款) 
	'startYear':'2000',
	'startMonth':'01',
	'endYear':'2017',
	'endMonth':'07',
	'hash':'d41d8cd98f00b204e9800998ecf8427e'	
}

result = requests.post(uri, data=payload)

jsonObj = json.loads(result.content)

for row in jsonObj['rows']:
	print(row)
	#print(row['sDate'])