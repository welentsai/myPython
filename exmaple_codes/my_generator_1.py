# -*- coding: utf-8 -*-

import itertools 

unique_characters = {'E', 'D', 'M', 'O', 'N', 'S', 'R', 'Y'}

# iterate through all the values and make it as a tuple or list or set
print(tuple(ord(c) for c in unique_characters))
print(list(ord(c) for c in unique_characters))
print(set(ord(c) for c in unique_characters))
print()

# ord(c) => c is a character , return an integer representing the Unicode code

# # generator expression 方法一
# 看起來像 list comprehension, 但是用括號()包起來, 而不是[]
gen = (ord(c) for c in unique_characters)

print(type(gen))
print(next(gen))
print(next(gen))
print()

# generator expression 方法二, 
# yield keyword => make this function as a generator
def ord_map(a_string):
	for c in a_string:
		yield ord(c)
print(type(gen))
print(next(gen))
print(next(gen))
print()

# permutations => 排列
# The permutations() function takes a sequence (here a list of three integers) and a number
# permutations() return a iterator
perms = itertools.permutations([1, 2, 3], 2)

# The permutations() function doesn’t have to take a list. It can take any sequence — even a string.
# A string is just a sequence of characters.
perms = itertools.permutations('ABC', 3)

print(list(itertools.permutations('ABC', 3)))
print()

# pruduct() => 笛卡爾乘積
print('Cartesian product of two sequences "ABC" and "123" ')
print(list(itertools.product('ABC', '123')))
print()

# combinations => 組合
print(list(itertools.combinations('ABC', 2)))
print(list(itertools.combinations('ABC', 3)))
print()
