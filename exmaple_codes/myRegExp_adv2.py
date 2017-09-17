
# -*- coding: utf-8 -*-

import re

# group 1
def match_sxz(noun):
	return re.search('[sxz]$', noun)

def apply_sxz(noun):
	return re.sub('$', 'es', noun)

# group 2
def match_h(noun):
    return re.search('[^aeioudgkprt]h$', noun)

def apply_h(noun):
    return re.sub('$', 'es', noun)

# group 3
def match_y(noun):                             
    return re.search('[^aeiou]y$', noun)
        
def apply_y(noun):                             
    return re.sub('y$', 'ies', noun)

# gruop default
def match_default(noun):
    return True

def apply_default(noun):
    return noun + 's'


# function tuples
# everything in Python is an object, including functions.
# The rules data structure contains functions — not names of functions, but actual function objects.
rules = ((match_sxz, apply_sxz),               
         (match_h, apply_h),
         (match_y, apply_y),
         (match_default, apply_default)
         )

def plural(noun):           
    for matches_rule, apply_rule in rules:       
        if matches_rule(noun):
            return apply_rule(noun)

# 方法二
def plural2(noun):
    if match_sxz(noun):
        return apply_sxz(noun)
    if match_h(noun):
        return apply_h(noun)
    if match_y(noun):
        return apply_y(noun)
    if match_default(noun):
        return apply_default(noun)

# 方法三, 再更抽象

# 建構一個抽象的 function tuple
# return a tuple of two functions
def build_match_and_apply_functions(pattern, search, replace):
    def matches_rule(word):                                     
        return re.search(pattern, word)
    def apply_rule(word):                                       
        return re.sub(search, replace, word)
    return (matches_rule, apply_rule)                          

# a tuple of tuples of strings
patterns = \
	(
		('[sxz]$',           '$',  'es'),
		('[^aeioudgkprt]h$', '$',  'es'),
		('(qu|[^aeiou])y$',  'y$', 'ies'),
		('$',                '$',  's')                                 
	)

# list comprehension
# rules ends up => a list of tuples, where each tuple is a pair of functions
# run time 時, 所有function才被產生出來, 並保存在rules中
rules = [build_match_and_apply_functions(pattern, search, replace)
         for (pattern, search, replace) in patterns]

def plural3(noun):
    for matches_rule, apply_rule in rules:
        if matches_rule(noun):
            return apply_rule(noun)

# 方法五
# 把 plural 規則放在一個外部檔案(config file)
# 把程式跟規則分開
# Code is code, data is data


rules = []

# The with statement creates what’s called a context:
# when the with block ends, Python will automatically close the file, 
# even if an exception is raised inside the with block.
with open('plural4-rules.txt', encoding='utf-8') as pattern_file:
	for line in pattern_file:
		# None =>  means “split on any whitespace (tabs or spaces, it makes no difference).”
		# 3 => split on whitespace 3 times
		pattern, search, replace = line.split(None, 3)
		# get a tuple of functions and append to rules
		rules.append(build_match_and_apply_functions(
			pattern, search, replace))