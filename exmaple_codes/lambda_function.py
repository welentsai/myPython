# -*- coding:utf-8 -*-
# Lambda Function
# Small anonymous functions can be created with the lambda keyword
# they are just syntactic sugar for a normal function definition. 
# Like nested function definitions
# They are syntactically restricted to a single expression

def make_incrementor(n):
	return lambda x : x + n # uses a lambda expression to return a function


f = make_incrementor(42)

print(f(0)) #42 
print(f(1)) #43

# tuple
t = 12345, 54321, 'hello!'
singleton = 'hello', # tuple, 含有一個項目的 tuple 經由一個值加上一個逗點來創建

print(singleton)
print(len(singleton))

# set 
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}

# dictionary
# key: value pair
# 字串和數字都可以當作 key
tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
print(tel)

# print 餵參數的用法
print('What is your {0}?  It is {1}.'.format('Name', 'Peter'))



