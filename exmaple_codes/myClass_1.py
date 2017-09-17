# -*- coding: utf-8 -*-

# 範例 1 
# PapayaWhip Class
# the pass statement => This is a Python reserved word that just means “move along, nothing to see here”. 
# It’s a statement that does nothing
class PapayaWhip:
    pass  

# Note: The first argument of every class method, including the __init__() method, 
# is always a reference to the current instance of the class. 
# By convention, this argument is named self. 
# In all class methods, self refers to the instance whose method was called. 
# you do not specify self when calling the method; Python will add it for you automatically.

# 範例 2
# Fib Class
# Python classes can have something similar to a constructor: the __init__() method.
# The __init__() method is called immediately after an instance of the class is created.
#
# 第一行的註解會變成 docstrings , instance 可用__doc__取得
#
# Instance variables are specific to one instance of a class. 
# self.max => instance variable, whole instance scope access
# self.a => instance variable
# self.b => instance variable
#
# The __iter__() method is called whenever someone calls iter(fib)
# a for loop will call this automatically
# the __iter__() method can return any object that implements a __next__() method.
#
# The __next__() method is called whenever someone calls next() on an iterator of an instance of a class.
# When the __next__() method raises a StopIteration exception, this signals to the caller that the iteration is exhausted
# If the caller is a for loop, it will notice this StopIteration exception and gracefully exit the loop.
# To spit out the next value, an iterator’s __next__() method simply returns the value. Do not use yield here;
# 
class Fib:
    '''iterator that yields numbers in the Fibonacci sequence'''

    def __init__(self, max): 
        self.max = max

    # only thing to do is to return a iterator (any object that implements a __next__() method)
    def __iter__(self): 
        self.a = 0
        self.b = 1
        return self

    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib


fib = Fib(100)
print(fib)
# Every class instance has a built-in attribute, __class__, which is the object’s class.
print(fib.__class__)
print(fib.__doc__)
print()

# Iterator 可以手動使用
print(iter(fib)) # iter(fib_inst) => returns an iterator object
print(next(fib)) # next() => call __next__()
print(next(fib))
print(next(fib))
print(next(fib))
print(next(fib))
print(next(fib))
print()

# for loop 自動使用 Iterator
# the for loop calls iter(fib_inst), which returns an iterator object
# in Fib, because the __iter__() method returns self, so fib_iter == fib_inst
# To “loop through” the iterator, the for loop calls next(fib_iter), 
# which calls the __next__() method on the fib_iter object
# When next(fib_iter) raises a StopIteration exception, the for loop will swallow the exception and gracefully exit. 
for n in Fib(1000):
    print(n, end=' ')


unique_characters = 'what the wonderful world'

assert len(unique_characters) <= 10, 'Too many letters'

