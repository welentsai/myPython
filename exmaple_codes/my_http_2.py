# -*- coding: utf-8 -*-

import requests
import json

# GET request
# res is a Response object, which contains a server's response to an HTTP request.
res = requests.get('https://api.github.com/events')
#print(res.text)  # get a str object 
# print(res.content) # get a bytes object
#print(res.encoding)
# print(res.json()) #  json() => to deal with response with JSON data


# GET request with params
# Passing Parameters In URLs
# e.g. httpbin.org/get?key=val
# using the params keyword argument
payload = {'key1': 'value1', 'key2': 'value2'}
payload2 = {'key1': 'value1', 'key2': ['value2', 'value3']}
res3 = requests.get('http://httpbin.org/get', params=payload2)
#print(res3.url)


# More complicated POST requests
# 像一張HTML Form的表格

# to do this, simply pass a dictionary to the data argument.
payload = {'key1': 'value1', 'key2': 'value2'}
res = requests.post("http://httpbin.org/post", data=payload)
#print(res.text)

# You can also pass a list of tuples to the data argument.
payload = (('key1', 'value1'), ('key1', 'value2'))
res = requests.post('http://httpbin.org/post', data=payload)
#print(res.text)

# json.dumps() => return a str object
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
res = requests.post(url, data=json.dumps(payload))
#print(res.url)

# pass it directly using the json parameter
res2 = requests.post(url, json=payload)

# POST a File
# It is strongly recommended that you open files in binary mode.
url = 'http://httpbin.org/post'
files = {'file': open('favorite-people.txt', 'rb')}

res = requests.post(url, files=files)
#print(res.text)
#print(res.status_code)

# If we made a bad request (a 4XX client error or 5XX server error response), we can raise it with
#print(res.raise_for_status())
#print(res.headers)


# Cookies

# deal with cookies from server
# Cookies are returned in a RequestsCookieJar, which acts like a dict
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
#print(r.cookies)

# To send your own cookies to the server, you can use the cookies parameter:
url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
#print(cookies)
r = requests.get(url, cookies=cookies)
#print(r.text)

# Cookies are returned in a RequestsCookieJar
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')

#print(jar)
url = 'http://httpbin.org/cookies'
r = requests.get(url, cookies=jar)
#print(r.text)

# Redirection and History

# The Response.history list contains the Response objects that were created in order to complete the request.
r = requests.get('http://github.com')

print(r.url)
print(r.status_code)
print(r.history)

