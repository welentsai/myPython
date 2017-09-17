# 指定 utf-8 編碼
# -*- coding:utf-8 -*-

# a file is called a module
# definitions from a module can be imported into other modules or into the main module

# Each module has its own private symbol table
# the author of a module can use global variables in the module

# Fibonacci numbers module

def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while b < n:
        print(b, end=' ')
        a, b = b, a+b
    print()

def fib2(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result