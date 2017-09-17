# -*- coding: utf-8 -*-

import re

# 建構一個抽象的 function tuple
# return a tuple of two functions
def build_match_and_apply_functions(pattern, search, replace):
  def matches_rule(word):                                     
      return re.search(pattern, word)
  def apply_rule(word):                                       
      return re.sub(search, replace, word)
  return (matches_rule, apply_rule)   


# LazyRule 類別
class LazyRules:

	# class variable and also instance variable
	rules_filename = 'plural4-rules.txt'

	def __init__(self):
	  self.pattern_file = open(self.rules_filename, encoding='utf-8')
	  self.cache = []

	def __iter__(self):
	  self.cache_index = 0
	  return self

	def __next__(self):
	  self.cache_index += 1
	  print(len(self.cache))
	  print(self.cache_index)
	  if len(self.cache) >= self.cache_index:
	    return self.cache[self.cache_index - 1]

	  if self.pattern_file.closed:
	  	print("file close !! , gonna raise StopIteration")
	  	raise StopIteration

	  line = self.pattern_file.readline()
	  if not line:
	      self.pattern_file.close()
	      print("not line !! , gonna raise StopIteration")
	      raise StopIteration

	  pattern, search, replace = line.split(None, 3)
	  funcs = build_match_and_apply_functions(
	      pattern, search, replace)
	  self.cache.append(funcs)
	  return funcs

rules = LazyRules()
r1 = LazyRules()
r2 = LazyRules()

print(r1.rules_filename)
print(r2.rules_filename)
print()

r2.rules_filename = "rrr"
print(r1.rules_filename) # r1 keep the same
print(r2.rules_filename) # r2 override its own instance variable
print()

r2.__class__.rules_filename = 'papayawhip.txt' # r2 change class varible 
print(r1.rules_filename) # r1 never override, so effected
print(r2.rules_filename) # r2 already override, so no effected
print()

for r in rules:
	print(r)