# -*- coding: utf-8 -*-

import requests 
import json

class StockAiCrawler:
	''' a calss to craw json data from Stock-ai'''

	# class variable and also instance variable
	uri = "https://stock-ai.com/eomDataQuery"

	def __init__(self, symblCode, startYr, startM, endYr, endM):
		self.setPayload(symblCode, startYr, startM, endYr, endM)

	def setPayload(self, symblCode, startYr, startM, endYr, endM):
		self.payload = {
			'a':'c',
			'showType':'Value',
			'symbolCode':symblCode, # M1B 貨幣總計數 (= M1A ＋ 活期儲蓄存款) 
			'startYear':startYr,
			'startMonth':startM,
			'endYear':endYr,
			'endMonth':endM,
			'hash':'d41d8cd98f00b204e9800998ecf8427e'	
		}

	def fetch(self):
		self.result = requests.post(self.uri, data = self.payload)
		self.jsonObj = json.loads(self.result.content)

	def display(self):
		for row in self.jsonObj['rows']:
			print(row)
