
# -*- coding: utf-8 -*-

import os, glob
import numpy

li = [1, 6, 3, 5, 2, 4]

strs = ['aa', 'BB', 'zz', 'CC', 'AA', 'bb']

li.append(3)

# li.sort() # 相同資料形態可以sorting
print(sorted(strs))

print(li[0])
print(li[0:2]) # start at 0, end to 2 - 1
print(li[1:-1]) # end at -1, last char
print(li)
print('list li length is :' + str(len(li)))
print(li.count(3)) # 回傳3在list中的出現次數, count occurrences of a specific list item
print(li.pop()) # pop() 回傳last list item
print(2 in li) # condition check,  2 in li , return true/false

# ===
print('====== aLi start ==== ')
aLi = ['A', 'B', 'c', 0, 3]

print(aLi[2:5])

bLi = [aLi[-2]] + [aLi[1]]  # 兩list 用 + 號串接
print(bLi)

print([aLi[-1]]*3) # 重複3次

print('====== aLi end ==== ')

#=====

girls = ['Emily', 'Hannah', 'Madison', 'Ashley', 'Sarah', \
				'Alexis', 'Samantha', 'Jessica', 'Elizabeth', 'Taylor', \
				'Lauren', 'Alyssa', 'Kayla', 'Abigail', 'Brianna', \
				'Olivia', 'Emma', 'Megan', 'Grace', 'Victoria']

for girl in girls:
	if girl.startswith(('A', 'M')):
		print(girl)

#=== EX5
a = ['A', 'B', 'c', 0, 3]
a = a[:2] + a[1:]
a = a[2:5]
a = [a[-2]] + [a[1]]
a = [a[-1]]*3
a = a[:2]

print(a)

#=== EX6
names = ["Emily", "Amy", "Penny", "Bernadette"]
california = [2269, 542, 54, 21]
new_york = [881, 179, 12, 11]

for i in range(len(names)):
	print(california[i] + new_york[i], end=' ')

print()

#=== EX7
a = [1, 3, 4, 5]
a.pop()
a = a + [5, 3]
a.reverse()
a.remove(5)
a.sort()
a.append(4)

print(a)

#=== Shortcuts EX 1
print('=== list short cuts ===')

counts = [356, 412, 127, 8, 32]

print(sum(counts))

for i in range(10):
	print('*' * i)

#=== ShortCuts Ex 2
names = ['Lilly', 'Lily', 'Leila', 'Lilja', 'Lillie']
counts = [356, 412, 127, 8, 32]

# zip() 回傳一個iterator, 指向 data tuples
# the zip() function in Python 3 returns an iterator 
# The purpose of this is to save memory (像一個指標結構指向data所在)
table = list(zip(names, counts)) # create a list out of zip()

print(table)

#=== ShortCuts EX3
names = ['Lilly', 'Lily', 'Leila', 'Lilja', 'Lillie']

# enumerate() Return an enumerate object
# The enumerate() function adds a counter to an iterable.
# The counter from start which defaults to 0
# the data tuple => (count, iterable[count])

print(list(enumerate(names, start=1)))

for i, name in enumerate(names):
	print(i, name)

#=== ShortCuts EX4
print(list(range(10, 51, 10)))

print(list(range(33, 29, -1)))


# Table Example

# columns: Name, #California, #New York
table = [
				  ["Emily", 2269, 881],
				  ["Amy", 542, 179],
				  ["Penny", 54, 12],
				  ["Bernadette", 21, 11]
				]

print(table)

for row in table:
	for i in row:
		print(i, end=', ')
	print()


# 在用2維list時, 要先初始化, Python稱之為 list comprehension
# Creates a list containing 5 lists, each of 8 items, all set to 0
# 或是使用 numpy
w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)] 
print(Matrix)

Matrix[2][3] = 5

x,y = 2, 3
print(Matrix[2][3])

table = numpy.zeros((10, 10))

i = 1
for x in range(10):
	for y in range(10):
		table[x][y] = i
		i+=1

print(table)


# List Comprehensions

a_list = [1, 9, 8, 4]

# To make sense of this, look at it from right to left
a_list = [elem * 2 for elem in a_list]

print(a_list)

# List Comprehensions

# new list [os.path.realpath(f)]
print([os.path.realpath(f) for f in glob.glob('*.py')])

# new list [f]
# at condition "if os.stat(f).st_size > 1000"
print([f for f in glob.glob('*.py') if os.stat(f).st_size > 1000])

# new list of tuples => [(f, os.stat(f))]
metadata = [(f, os.stat(f)) for f in glob.glob('*test*.py')] 
print(type(metadata))

# Dictionary Comprehensions

# new dict {f:os.stat(f)}
# it contains two expressions separated by a colon. 
# The expression before the colon (f in this example) is the dictionary key; 
# the expression after the colon (os.stat(f) in this example) is the value.
metadata_dict = {f:os.stat(f) for f in glob.glob('*l*.py')} 
print(metadata_dict)


metadata_dict = {f:os.stat(f) for f in glob.glob('*')} 

# The method items() returns a list of dict's (key, value) tuple pairs
# new dict { os.path.splitext(f)[0] : meta.st_size }
# at condition "if meta.st_size > 1000"
metadata_dict = {os.path.splitext(f)[0]:meta.st_size for f, meta in metadata_dict.items() if meta.st_size > 1000}
print(metadata_dict)

# Set Comprehensions

# note : set is unordered
a_set = set(range(10))
print(a_set)

print({x**2 for x in a_set})

print({x for x in a_set if x % 2 == 0})

