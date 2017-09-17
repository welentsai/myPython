# 指定 utf-8 編碼
# -*- coding:utf-8 -*-

# 單行註解是使用#
# 多行註解則是連續三個單引號
'''
    多行註解
    就是這樣
    沒什麼別的
'''
print("HelloWorld 你好 台灣")

text = "HelloWorld_Text"
print(text)

a = 17
b = 3

print(a//b) # floor division (取整數)

print(b**2) # a powers(冪次)
print(2**7) # 2 的 7 次方

print(round(3.14159265359, 1)) #取到小數1位
print(round(3.14159265359, 4)) #取到小數4位, 4捨5入

# 一般來說，字串包含單引號而沒有雙引號時，會使用雙引號包圍字串
str = 'doesn\'t'  # use \' to escape the single quote...
str2 = "doesn't"  # ...or use double quotes instead

print(str)
print(str2)
print('"Yes," he said.')

#如果你不希望字元前出現 \ 就被當成特殊字元時，可以改使用 raw string，在第一個包圍引號前加上 r 
print(r'C:\some\name') # 不然 \n 會被當成 newline

#字串值可以跨越數行, 加入\取消自動先跳一行
print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")

# 兩個以上相鄰的字串值, 會被自動連接起來
text = ('Put several strings within parentheses '
				'to have them joined together.')

print(text)
print(text[0]) # 字串可以被索引, 但嘗試對字串中某個索引位置賦值會產生錯誤
print(text[5])
print(text[-1]) # 索引可以是負的, 負的索引值由 -1 開始, last char
print(text[-5]) # 倒數5th 

# slice notation
# a[start:end]  => items start through end-1
# a[start:]     => items start through the rest of the array
# a[:end]       => items from beginning through end-1
# a[:]          => a copy of whole array

print(text[0:3]) # subString
print(text[3:11])
print(text[:3])
print(text[2:])
print(text[-2:])
print(text[:-2])

print(len(text)) 

# List, 以逗號分隔
squares = [1, 4, 9, 16, 25, 36]
print(squares[0])
print(squares[-1])

# 支援接合 (concatenation) 
squares = squares + [49, 64, 81, 100]
print(squares)

#不同於字串是 immutable，list 是 mutable 型別
squares[0] = 111
print(squares)

squares.append(121)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(letters)
letters[2:5] = ['C', 'D', 'E']
print(letters)
print(len(letters))

# clear the list
letters[:] = []

# nested list
a = ['a', 'b', 'c']
n = [1, 2, 3]
x = [a, n]
print(x)

# Fibonacci series
# 任何非零的整數值為真 (true)；零為偽 (false)
# 迴圈的主體會縮排
# 結束時多加一行空行來代表結束
a, b = 0, 1
while b < 100:
	print(b, end=',') # 關鍵字引數 end 可以被用來避免額外的換行符加入到輸出中
	a, b = b, a+b

print()

# if ... elif ... else
x = int(input("Please enter an integer: "))

if x < 0 :
	print("x is negative")
elif x == 0:
	print('Zero')
elif x == 1:
	print('Single')
else:
	print('More')

# for loop
for s in squares:
	print(s)

# squares[:] is a whole copy of squares
for s in squares[:]:  # Loop over a slice copy of the entire list.
	if s < 20 :
		print(s)
	else:
		print('bigger than 20')

# 內建 range() 函式, 生成一等差級數
for i in range(len(squares)):
	print(i, squares[i])
	if squares[i] > 20 :
		squares[i] = squares[i] % 20

print(squares)

# range(start, end) => item start through end-1
# // 整數除法(取整數)
for n in range(2,10):  # n from 2 to 9
	for x in range(2,n): 
		if n % x == 0:
			print(n, 'equals', x, '*', n//x)
			break

# The keyword def =>  introduces a function definition
# The key word end => 可以被用來避免額外的換行符加入到輸出中
def fib(n):
	result = []
	a,b = 0,1
	while a < n:
		result.append(a)
		#print(a, end=' ')
		a,b = b, a + b
	#print()
	return result

fib(100)

f100 = fib(100)
print(f100)

def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            return print("4 failures, bye bye")
        print(reminder)


ask_ok("yes or no ?")


