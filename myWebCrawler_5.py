# -*- coding: utf-8 -*-

import re # regular expression 
import requests 
import json

# import user class
# from <foler> import <file>
# from <folder.file> import <class>

#from stockAiCrawler import StockAiCrawler
from stockAiCrawler.StockAiCrawler import StockAiCrawler

# symbolCode = twA02 =>  M1B 貨幣總計數 (= M1A ＋ 活期儲蓄存款) 
mycrawler = StockAiCrawler('twA02', '2000', '01', '2017', '08')
mycrawler.fetch()
mycrawler.display()

#symbolCode = marketCapitalization => 台灣台股上市公司當月總市值
mycrawler.setPayload('marketCapitalization', '2000', '01', '2017', '08')
mycrawler.fetch()
mycrawler.display()

#symbolCode = twIndexScore => 台灣景氣對策信號(分數)
mycrawler.setPayload('twIndexScore', '2000', '01', '2017', '08')
mycrawler.fetch()
mycrawler.display()