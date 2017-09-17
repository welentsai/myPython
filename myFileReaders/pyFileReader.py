# -*- coding: utf-8 -*-
import re

line_number = 0

# Regular Expression
# \w => Matches Unicode word characters [a-zA-Z0-9_]
# [] => to indicate a set 
# [\w-] => any word char and char '-'
# [\w-]+ => any word composed by word chars and '-'

custList = []

with open('data/20161121134754-RCHMA-utf8.txt', encoding='utf-8') as a_file:
	for a_line in a_file:
		line_number += 1
		if "Values" in a_line:
			rdata = re.split('Values', a_line)[1]
			custList.append(tuple(re.findall(r"[\w-]+", rdata)))

for cust in custList:
	print(cust)