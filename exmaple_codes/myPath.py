# -*- coding: utf-8 -*-

import os
import glob

print(os.getcwd())

# absolute path
#os.chdir('/myPython/modules')
#print(os.getcwd())

# relative path
#os.chdir('modules/fitz')
#print(os.getcwd())

# get the contents of a directory
print(glob.glob('l*.py'))
print(glob.glob('*L*.py'))
print(glob.glob('*.py'))
print(glob.glob('/myPython/modules/*.*'))

print(os.path.realpath('myPath.py'))