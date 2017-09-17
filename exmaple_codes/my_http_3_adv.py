# -*- coding: utf-8 -*-

import requests

# Session Objects
# The Session object allows you to persist certain parameters (ex, cookies) across requests.
# And it will use urllib3's connection pooling, the underlying TCP connection will be reused, 
# which can result in a significant performance increase

# A Session object has all the methods of the main Requests API

s = requests.Session()

# Sessions can also be used to provide default data to the request methods
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'}) # both 'x-test' and 'x-test2' are sent
#print(r.text)


r = s.get('http://httpbin.org/cookies')
#print(r.text)


# Sessions can also be used as context managers
# This will make sure the session is closed as soon as the with block is exited
with requests.Session() as s:
	s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')


res = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
#print(res.headers) # the headers from server
# print(res.request.headers) # the header we sent to server


res = requests.get('https://requestb.in')

print(res)
