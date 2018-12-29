from urllib.request import urlopen
from xml.etree import ElementTree
import pyrebase

config = {
    "apiKey": "AIzaSyDQFAWoIUx5I0g7yaSiIfqnPJL_2dmLxlI",
    "authDomain": "webex-4608e.firebaseapp.com",
    "databaseURL": "https://webex-4608e.firebaseio.com",
    "storageBucket": "webex-4608e.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

articleList = []
maxAveArticle = []

data = db.child("tagList").get()
tagList = dict(data.val())


def getXml():
    global tagList
    print(tagList)
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
                   'tag': {},
                   'ave': 0
                   }
             }
        )

        for index, tag in enumerate(item.findall('{http://purl.org/dc/elements/1.1/}subject')):
            # print(articleList[num].get(title).get('tag'))
            tag = tag.text.encode('cp932', "ignore")
            tagD = tag.decode('cp932')
            # if not tag.decode('cp932') in tagList:
            #     db.child("tagList").child(tag.decode('cp932')).set(0)
            # print('exist')
            # else:
            #     db.child("tagList").child(tag.decode('cp932')).set(0)

            tagList.setdefault(tag.decode('cp932'), 0)
            print('----------------')
            print(tagList.get(tagD))
            articleList[num].get(num).get('tag').setdefault(
                tag.decode('cp932'), tagList.get(tag.decode('cp932')))
            # articleList[num].get(num).get('tag').setdefault(
            #     tag.decode('cp932'), 1)

            # print(tag.text)


def calcAve():

    for index, article in enumerate(articleList):
        ave = 0
        sum = 0
        tagDictLen = len(article.get(index).get("tag"))
        for tagValue in article.get(index).get("tag"):
            sum += article.get(index).get("tag").get(tagValue)
            print(article.get(index).get("tag").get(tagValue))

        ave = sum / tagDictLen
        # print(article.get(index).get("tag"))
        print(len(article.get(index).get("tag")))
        article.get(index)['ave'] = ave
        print(article.get(index).get("ave"))


def getMaxAveArticle():
    temp = -100000000
    global maxAveArticle
    for index, article in enumerate(articleList):
        num = article.get(index).get("ave")

        if num > temp:
            temp = num
            # print(temp)
            maxAveArticle = article.get(index)
            # print('maxAveArticle is '+maxAveArticle)

    return maxAveArticle


def reviewScore():
    print('1~5の5段階で評価してください．>')
    score = int(input())  # iを取得し、intに値を入れる
    if score <= 5 and score > 0:

        num = 0
        if score == 1:
            num = -1
        elif score == 2:
            num = -0.5
        elif score == 3:
            num = 0
        elif score == 4:
            num = 0.5
        elif score == 5:
            num = 1

        for tag in maxAveArticle.get('tag'):
            temp = tagList.get(tag)
            sum = temp + num
            tagList[tag] = sum
            print(tag + ':' + str(tagList.get(tag)))
    else:
        print('今回は評価しませんでした')


def main():
    getXml()
    calcAve()
    print(getMaxAveArticle())
    reviewScore()
    print(tagList)

    # print(articleList)
    db.child("tagList").set(tagList)


if __name__ == "__main__":
    main()
