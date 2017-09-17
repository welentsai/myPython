# -*- coding: utf-8 -*-

# 讀取空氣品質監測JSON
# Output : 所有監測地區 AQI數值

import json
import re # regular expression 
import requests 
from bs4 import BeautifulSoup


# 空氣品質監測JSON
result = requests.get("https://taqm.epa.gov.tw/taqm/aqs.ashx?lang=tw&act=aqi-epa")

jsonObj = json.loads(result.content)

# python中, json object = dict 
for row in jsonObj['Data']:
	print(row['SiteName'], end=' ')
	print(row['AQI'])
