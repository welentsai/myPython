
# -*- coding: utf-8 -*-

import itertools

names = list(open('favorite-people.txt', encoding='utf-8'))
print(names)
print()

# rstrip() string method to strip trailing whitespace from each line
names = [name.rstrip() for name in names]
print(names)
print()

# By default, sorted() sorts alphabetically.
names = sorted(names)
print(names)
print()

# the sorted() function can also take a function as the key parameter
names = sorted(names, key=len)
print(names)
print()

# 注意
# The itertools.groupby() function only works if the input sequence is already sorted by the grouping function.
# 所以 序列資料要先用 sorted() + key function 的方式先排好

# itertools.groupby() function takes a sequence and a key function
# returns an iterator that generates pairs
# Each pair( key_function(each item), another iterator containing all the items that shared same key result )
groups = itertools.groupby(names, len)

for name_length, name_iter in groups:
	print('Names with {0:d} letters:'.format(name_length))
	for name in name_iter:
		print(name)

print(list(zip(range(0, 3), range(10, 13))))

characters = ('S', 'M', 'E', 'D', 'O', 'N', 'R', 'Y')
guess = ('1', '2', '0', '3', '4', '5', '6', '7')

a_tuple = tuple(zip(characters, guess))
print(a_tuple)
print()

a_dict = dict(a_tuple)
print(a_dict)
print()

# ord() => get character unicode in integer
characters = tuple(ord(c) for c in 'SMEDONRY')
guess = tuple(ord(c) for c in '91570682')  

# zip(characters, guess) => return a list of tuple pairs
# dict(zip(characters, guess)) => return a dict list from tuple pairs
translation_table = dict(zip(characters, guess))
print(characters)
print(guess)
print(translation_table)

print('S'.translate(translation_table))
print('SE'.translate(translation_table))
print('SEN'.translate(translation_table))
print('SEND'.translate(translation_table))

# translate() is a string method, 根據 dict 的 key:value, 做搜尋/取代
print('SEND + MORE == MONEY'.translate(translation_table) )
print()

# eval(expression) => take a string and evaluated as a Python expression
# return the result of the evaluated expression
print(eval('1 + 1 == 2'))
print(eval('SEND + MORE == MONEY'.translate(translation_table)))
