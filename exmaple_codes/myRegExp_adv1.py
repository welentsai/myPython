# -*- coding: utf-8 -*-

import re


# [sxz] => s or x or z, but only one of them
# [^abc] => any single character except a, b, or c
def plural(noun):          
	if re.search('[sxz]$', noun):             
	    return re.sub('$', 'es', noun) #  replacing the end of the string (matched by $) with the string es    
	elif re.search('[^aeioudgkprt]h$', noun):
	    return re.sub('$', 'es', noun)       
	elif re.search('[^aeiou]y$', noun):      
	    return re.sub('y$', 'ies', noun)     
	else:
	    return noun + 's'


# [] => match exactly one of them
# [abc] => match a or b or c, but only one of them
print(re.search('[abc]', 'Mark'))
print(re.sub('[abc]','o', 'Mark'))
print(re.sub('[abc]','o', 'rock'))
print(re.sub('[abc]','o', 'caps')) #re.sub() replaces all of the matches
print()


# ([^aeiou]) => a remembered group, used to remember "the character before y"
# \1 => refer to first group, in this example \1 refer to c
print(re.sub('([^aeiou])y$', r'\1ies', 'vacancy'))