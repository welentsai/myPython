# 指定 utf-8 編碼
# -*- coding:utf-8 -*-

import sys
import os
import re # regular expression
from datetime import date
import locale
import myModule

myModule.fib(100)

print(myModule.__name__) # __name__ , global variable to get module name 

print(sys.path)

# dir() lists the names you have defined currently
# it lists all types of names: variables, modules, functions, etc
print(dir(os))

print(date.today())

birthday = date(1982, 1, 31)

age = date.today() - birthday

print(age.days)

print(dir(locale))
