#!python3.6-32
import hashlib
m = hashlib.md5()
flist = ["fitz/__init__.py", "fitz/_fitz.pyd", "fitz/fitz.py", "fitz/utils.py",]
for f in flist:
    fr = open(f, "rb")
    m.update(fr.read())
    fr.close()

md5new = m.hexdigest()
fr = open("md5.txt")
md5old = fr.read()
fr.close()
if md5new != md5old:
    raise ValueError("md5 mismatch: probable download error")

from distutils.core import setup
from distutils.sysconfig import get_python_lib
from distutils.sysconfig import get_python_version
import os, platform

bitness    = '32bit'
py_version = '3.6'

if not platform.architecture()[0] == bitness:
    raise ValueError('this setup is for platform "%s" only' % (bitness,))

if not get_python_version() == py_version:
    raise ValueError('this setup is for Python version %s only' % (py_version,))

setup_name = 'fitz'

pkg_tab = open("PKG-INFO").read().split("\n")
long_dtab = []
classifier = []
for l in pkg_tab:
    if l.startswith("Classifier: "):
        classifier.append(l[12:])
        continue
    if l.startswith(" "):
        long_dtab.append(l.strip())
long_desc = "\n".join(long_dtab)
pl = os.path.join(get_python_lib(), setup_name)
setup(name = setup_name,
      version = "1.11.0", 
      description = 'Python bindings for the PDF rendering library MuPDF',
      long_description = long_desc,
      classifiers = classifier,
      url = 'https://github.com/rk700/PyMuPDF',
      author = 'Ruikai Liu',
      author_email = 'lrk700@gmail.com',
      license = 'GPLv3+',
      ext_modules = [],
      data_files = [(pl, ['fitz/_fitz.pyd'])],
      py_modules = ['fitz.fitz', 'fitz.utils'])
