# -*- coding: utf-8 -*-
import re

# re.sub(pattern, repl, string) => return a string
# replace pattern in string by repl 

s = '100 NORTH MAIN ROAD'
print(s)
print(s.replace('ROAD', 'RD.'))
print()

s = '100 NORTH BROAD ROAD' # 'ROAD' appears twice in the address
print(s)
print(s.replace('ROAD', 'RD.')) # result is not we expected
print()

# The $ means “end of the string.”
# the caret ^ means “beginning of the string.”)
print(re.sub('ROAD$', 'RD.', s))
print()

s = '100 BROAD'

# It recommended always using raw strings when dealing with regular expressions
# \b => which means “a word boundary must occur right here.”
# to match :
#		1. ROAD at the end of a string
#		2. it was its own word
print(re.sub('\\bROAD$', 'RD.', s)) # backslash plague
print(re.sub(r'\bROAD$', 'RD.', s)) # raw string, by prefixing the string with the letter r.
print()

s = '100 BROAD ROAD APT. 3'
print(re.sub(r'\bROAD$', 'RD.', s))
print(re.sub(r'\bROAD\b', 'RD.', s))
print()

s = '100 BROAD (ROAD) APT. 3'
print(re.sub(r'\bROAD\b', 'RD.', s))
print()

'''
Roman Numerals
I = 1
V = 5
X = 10
L = 50
C = 100
D = 500
M = 1000
'''

# ^ matches what follows only at the beginning of the string
# M? optionally matches a single M character
# Since M? is repeated three times, you’re matching anywhere from zero to three M characters in a row
# $ matches the end of the string
pattern = '^M?M?M?$'

# re.search() return a match object, return None if not found
print(re.search(pattern, 'MMM')) 
print(re.search(pattern, 'MM')) 
print(re.search(pattern, '')) 
print(re.search(pattern, 'MMMM')) 
print(re.search(pattern, 'p')) 
print()

pattern = '^M?M?M?(CM|CD|D?C?C?C?)$'
print(re.search(pattern, 'C')) 
print(re.search(pattern, 'CC'))
print(re.search(pattern, 'CCCC'))
print(re.search(pattern, 'D'))
print(re.search(pattern, 'MD')) # MD is 1500
print(re.search(pattern, 'MCM')) # MCM in roman numeral is 1900
print(re.search(pattern, 'MMMCC')) # MMMCC is 3300
print()

# The {n,m} Syntax
# M{0,3} => from zero to three M characters
pattern = '^M{0,3}$'
print(re.search(pattern, 'M'))
print(re.search(pattern, 'MMMM'))
print()

# Verbose Regular Expressions
# 	1. Whitespace is ignored.
#		2. Comments are ignored.
# So we can put some inline documentation that we can understand it six months later

pattern = '''
    ^                   # beginning of string
    M{0,3}              # thousands - 0 to 3 Ms
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 Cs),
                        #            or 500-800 (D, followed by 0 to 3 Cs)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 Xs),
                        #        or 50-80 (L, followed by 0 to 3 Xs)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 Is),
                        #        or 5-8 (V, followed by 0 to 3 Is)
    $                   # end of string
    '''

print(re.search(pattern, 'M', re.VERBOSE))
print(re.search(pattern, 'MCMLXXXIX', re.VERBOSE))
print()


# re.compile() => return a regular expression object
# Always read regular expressions from left to right.  (左至右)
# \d means “any numeric digit” (0 through 9)
# \d{3} => exactly 3 numeric digits
# (\d{3}) => match exactly three numeric digits, and then remember them as a group that I can ask for later
phonePattern = re.compile(r'^(\d{3})-(\d{3})-(\d{4})$')
print(phonePattern.search('800-555-1212').groups())
print()

# (\d+)$ => match a group of one or more digits, at the end of string 
phonePattern = re.compile(r'^(\d{3})-(\d{3})-(\d{4})-(\d+)$')
print(phonePattern.search('800-555-1212-1').groups())
print(phonePattern.search('800-555-1212-1234').groups())
print()

# \D 	=> matches any character except a numeric digit
# \D+ => one or more characters that ar not digits
phonePattern = re.compile(r'^(\d{3})\D+(\d{3})\D+(\d{4})\D+(\d+)$')
print(phonePattern.search('800 555 1212 1234').groups())
print(phonePattern.search('800-555-1212-1234').groups())
print()

# \D* => 0 or more non digits
# (\d*)$ => 0 or more digits as group, at the end of string
phonePattern = re.compile(r'^(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
print(phonePattern.search('80055512121234').groups())
print(phonePattern.search('800.555.1212 x1234').groups())
print(phonePattern.search('800-555-1212').groups())
print()


phonePattern = re.compile(r'^\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
print(phonePattern.search('(800)5551212 ext. 1234').groups())
print(phonePattern.search('800-555-1212').groups())
print()

# lack of ^ => not matching the beginning of the string anymore
phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
print(phonePattern.search('work 1-(800) 555.1212 #1234').groups())
print(phonePattern.search('800-555-1212').groups())
print(phonePattern.search('80055512121234').groups())
print()

# put all together
phonePattern = re.compile(r'''
                # don't match beginning of string, number can start anywhere
    (\d{3})     # area code is 3 digits (e.g. '800')
    \D*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    \D*         # optional separator
    (\d{4})     # rest of number is 4 digits (e.g. '1212')
    \D*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
    $           # end of string
    ''', re.VERBOSE)

print(phonePattern.search('work 1-(800) 555.1212 #1234').groups())
print(phonePattern.search('800-555-1212').groups())