import re

old_headers ='''
Source: source 
Date:Mon, 26 Jul 2021 05:47:06 GMT 
Authorization:hmac id="AKIDKpo6me25b14nzcNefQeoqR95syh2ayx97s0g", algorithm="hmac-sha1", headers="date source", signature="jmwgtLvjj06A/M/TNcCqL72GRsk=" 
Content-Type:application/json; charset=utf-8 
Content-Length:403 
Host:api.motuobang.com 
Connection:Keep-Alive 
Accept-Encoding:gzip 
User-Agent:okhttp/3.14.
'''

pattern = '^(.*?):[\s]*(.*?)$'
headers = ""
for line in old_headers.splitlines():
    headers += (re.sub(pattern,'\'\\1\': \'\\2\',',line)) + '\n'
print(headers[:-2])

print(type(old_headers))