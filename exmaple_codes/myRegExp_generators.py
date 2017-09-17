# -*- coding: utf-8 -*-

import re

# the yield keyword in make_counter means that this is not a normal function
# It is a special kind of function which generates values one at a time.
# Calling it will return a generator that can be used to generate successive values of x
def make_counter(x):
	print('entering make_counter')
	while True:
		yield x
		print('incrementing x')
		x = x + 1

# create an instance of the make_counter generator
# make_counter() function returns a generator object
counter = make_counter(2)

print(counter)

# The next() function takes a generator object and returns its next value.
# first call of next(), it executes the code in make_counter() up to the first yield statement, 
# then returns the value that was yielded.
print(next(counter))

# it resumes exactly where it left off and continues until it hits the next yield statement.
print(next(counter))
print(next(counter))


# A Fibonacci Generator
def fib(max):
    a, b = 0, 1          
    while a < max:
        yield a          
        a, b = b, a + b 

# You can use a generator like fib() in a for loop directly
# The for loop will automatically call the next() function to get values from the fib() generator
for n in fib(100):
	print(n, end=' ')

print()
# pass a generator to the list() function
# iterate through the entire generator
print(list(fib(1000)))


# 回到 plural 規則, 利用 Generator 來處理
# With generators, you can do everything lazily
# What have you lost? Performance!

# a rules generator
def rules(rules_filename):
    with open(rules_filename, encoding='utf-8') as pattern_file:
        for line in pattern_file:
            pattern, search, replace = line.split(None, 3)                   
            yield build_match_and_apply_functions(pattern, search, replace) 

def plural5(noun, rules_filename='plural4-rules.txt'):
	# for loop 搭配 rules() generator
    for matches_rule, apply_rule in rules(rules_filename):                   
        if matches_rule(noun):
            return apply_rule(noun)
    raise ValueError('no matching rule for {0}'.format(noun))