# -*- coding: utf-8 -*-

# UTF-8 is a variable-length encoding system for Unicode.
# That is, different characters take up a different number of bytes. 
# For ascii characters (A-Z, &c.) utf-8 uses just one byte per character. 
# A document encoded in utf-8 uses the exact same stream of bytes on any computer.

# Disadvantages: because each character can take a different number of bytes, 
# finding the Nth character is an O(N) operation

# Advantages: super-efficient encoding of common ascii characters. 
# No worse than UTF-16 for extended Latin characters. Better than UTF-32 for Chinese characters.

# In Python 3, all strings are sequences of Unicode characters. 
# Bytes are not characters; bytes are bytes. Characters are an abstraction.


# format a string
# String object "{0}'s password is {1}"
# format() is a string method
print("{0}'s password is {1}".format("welen", "5566"))

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], \
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

print(type(SUFFIXES))

si_suffixes = SUFFIXES[1000]

print(si_suffixes)

# {0} refer to first argument
# {0[0]} refer to the first item of the list si_suffixes
# {0[1]} refer to the 2nd item of the list si_suffixes

print("1000{0[0]} = 1{0[1]}".format(si_suffixes))

# :.1f is format specifier
# a colon (:) marks the start of the format specifier
# “.1” means “round to the nearest tenth”
# “f” means “fixed-point number” 
print('{0:.1f} {1}'.format(698.26, 'GB'))

s = '''Finished files are the re-
sult of years of scientif-
ic study combined with the
experience of years.'''

print(s)

query = 'user=pilgrim&database=master&password=PapayaWhip'
a_list = query.split('&')
print(a_list)

# str.split(sep=None, maxsplit=-1) => Return a list
# maxsplit => the number of times you want to split
# If maxsplit is not specified or -1, then there is no limit
# the list will have at most maxsplit+1 elements

# for example, maxsplit = 1 => means only split once
# split once => has 2 elements


# return list of two-element-lists [v.split('=', 1)]
# 
a_list_of_lists = [ v.split('=', 1) for v in a_list if '=' in v]
print(a_list_of_lists)

a_dict = dict(a_list_of_lists)
print(a_dict)

# A bytes object is immutable;
by = b'abcd\x65' # define a bytes object, hex number from \x00 to \xff
print(by)

by += b'\x66'
print(by)

# operation mix bytes and strings will cause errors

a_string = '深入 Python' 

# str.encode() returns a bytes object
by = a_string.encode('utf-8') 

print(type(by))
