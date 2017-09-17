# -*- coding: utf-8 -*-

from pymongo import MongoClient
import datetime
import pprint

client = MongoClient('mongodb://welen:welen88@ds064198.mlab.com:64198/welendb')

# get DB 
db = client['welendb']

# get Collection
tradings = db.tradings # same =>  db['tradings']

print('total data count is ' + str(tradings.count()))

# 搜尋 一筆
# get single Document
#print(tradings.find_one())
#pprint.pprint(tradings.find_one())

# 欄位 搜尋 
# Query for More Than One Document
#for trading in tradings.find({'chg': '-0.05'}):
	#print(trading)

# 日期範圍 搜尋 
# find trading older than a certain date
# sort the results by date
d = datetime.datetime(2009, 1, 31, 0)
for trading in tradings.find({"date": {"$lt": d}}).sort("date"):
	print(trading)