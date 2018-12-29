import requests

url = 'https://note.nkmk.me'

hb_count = 'http://api.b.st-hatena.com/entry.count'

r = requests.get(hb_count, params={'url': url})

print(r.url)
# http://api.b.st-hatena.com/entry.count?url=https%3A%2F%2Fnote.nkmk.me

print(r.text)
# 5

print(type(r.text))
# <class 'str'>

print(int(r.text))
# 5

print(type(int(r.text)))
# <class 'int'>