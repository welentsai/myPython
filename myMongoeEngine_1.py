# -*- coding: utf-8 -*-

from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField

import datetime

# Regular connect
client = connect('welendb', host='mongodb://welen:welen88@ds064198.mlab.com:64198/welendb')

print(client)

# The way to link a class to an existing collection => using meta:
class TwCap(Document):
	# Meta variables.
	meta = {
		'collection': 'twCaps' # 對應到 twCaps Document in existing MongoDB
	}
	v = IntField(db_field='__v') # 對應到 __v field 的 MongoEngine 寫法
	date = DateTimeField(default=datetime.datetime.utcnow)
	price = StringField(required=True)

# find all
# for cap in TwCap.objects:
# 	print(cap)

# find with condition
for cap in TwCap.objects(price='30951400'):
	print(cap.date, end=' , price: ')
	print(cap.price)
