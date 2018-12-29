# import feedparser

# RSS_URL = "http://b.hatena.ne.jp/hotentry/it.rss"

# hatena_RSS = feedparser.parse(RSS_URL)

# print(hatena_RSS.feed.title)

# for entry in hatena_RSS.entries:
#   title = entry.title.encode('cp932', "ignore")
#   # title = entry.title
#   link  = entry.link
#   des  = entry.description
#   tag   = entry.dc:subject.encode('cp932', "ignore")
#   print(title.decode('cp932'))
#   print(tag.decode('cp932'))
#   # print(title)
#   print(link)
#   print(des)
#   print('------------------------------------------------------------------------------------------------')
  
#   # print(tag.decode('cp932'))

# from urllib.request import urlopen
# from lxml import etree

# f = urlopen('http://b.hatena.ne.jp/hotentry/it.rss')
# xml = f.read()
# root = etree.fromstring(xml)

# tag = root.xpath('./item', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
# print(tag)

# from lxml import etree
# from urllib.request import urlopen

from urllib.request import urlopen
from xml.etree import ElementTree

f = urlopen('http://b.hatena.ne.jp/hotentry/it.rss')
xml = f.read()
root = ElementTree.fromstring(xml)

for s in root.findall('{http://purl.org/rss/1.0/}item'):
    for i in s.findall('{http://purl.org/dc/elements/1.1/}subject'):
        print(i.text)