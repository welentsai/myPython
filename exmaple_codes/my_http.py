# -*- coding: utf-8 -*-

# import urllib.request

from http.client import HTTPConnection
from urllib.request import urlopen

HTTPConnection.debuglevel = 1

a_url = 'http://www.diveintopython3.net/examples/feed.xml'


# urllib.request.urlopen(a_url) => return a file-like object
# that you can just read() from to get the full contents of the page
#
# urllib.request.urlopen(a_url).read() => return a bytes object, not a string
# data = urllib.request.urlopen(a_url).read()

response  = urlopen(a_url).read()
print(type(response ))
print(response )
print()

response2 = urlopen(a_url)
print(response2)
print()
print(response2.headers.as_string())
print()

data2 = response2.read()
print(len(data2))
