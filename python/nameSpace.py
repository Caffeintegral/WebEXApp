from urllib.request import urlopen
from xml.etree import ElementTree
import pickle
import os

tagList = {}

if os.path.getsize('tagList.binaryfile') > 0:
    with open('tagList.binaryfile', "rb") as f:
        unpickler = pickle.Unpickler(f)
        # if file is not empty scores will be equal
        # to the value unpickled
        tagList = unpickler.load()

articleList = []

f = urlopen('http://b.hatena.ne.jp/hotentry/it.rss')
xml = f.read()
root = ElementTree.fromstring(xml)

for num, item in enumerate(root.findall('{http://purl.org/rss/1.0/}item')):
    # print('--------------------------------------------------------------')
    # print(item.find('{http://purl.org/rss/1.0/}title').text)
    # print(item.find('{http://purl.org/rss/1.0/}link').text)
    title = item.find(
        '{http://purl.org/rss/1.0/}title').text.encode('cp932', "ignore")
    url = item.find(
        '{http://purl.org/rss/1.0/}link').text.encode('cp932', "ignore")
    articleList.append(
        {num: {'title': title.decode('cp932'),
               "url": url.decode('cp932'),
               'tag': {}}}
    )

    for index, tag in enumerate(item.findall('{http://purl.org/dc/elements/1.1/}subject')):
        # print(articleList[num].get(title).get('tag'))
        tag = tag.text.encode('cp932', "ignore")
        articleList[num].get(num).get('tag').setdefault(
            tag.decode('cp932'), 1.2)
        tagList.setdefault(tag.decode('cp932'), 0)
        # print(tag.text)


fw = open('tagList.binaryfile', 'wb')
pickle.dump(tagList, fw)

fw.close

# print(tagList)
print(articleList)
