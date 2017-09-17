
# -*- coding:utf-8 -*-

import csv

# csv.reader
with open('木柵_2015.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print(row)

# csv.DictReader
# csv module 把資料parsing成dictionary的格式
# 第一列當作dictionary的key
with open('木柵_2015.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		pass
		# print(row)
		# print(row['成交日期'])
