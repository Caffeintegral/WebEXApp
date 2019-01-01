from urllib.request import urlopen
from xml.etree import ElementTree
import pyrebase
from firebasetoken import config


firebase = pyrebase.initialize_app(config)
db = firebase.database()

articleList = []
maxAveArticle = []
selectedArticle = []

data = db.child("tagList").get()
tagList = dict(data.val())

data = db.child("selectedArticle").get()
titleList = dict(data.val())
for i in titleList.keys():
    selectedArticle.append(titleList.get(i))


print('selectedArticle')
print(selectedArticle)


def selectCategory():
    global url
    print('カテゴリーを選択して下さい')
    print('1：総合人気ランキング')
    print('2：総合新着ランキング')
    print('3：世の中人気ランキング')
    print('4：世の中新着ランキング')
    print('5：政治と経済人気ランキング')
    print('6：政治と経済新着ランキング')
    print('8：暮らし新着ランキング')
    print('9：学び人気ランキング')
    print('10：学び新着ランキング')
    print('11：テクノロジー人気ランキング')
    print('12：テクノロジー新着ランキング')
    print('13：エンタメ人気ランキング')
    print('14：エンタメ新着ランキング')
    print('15：アニメとゲーム人気ランキング')
    print('16：アニメとゲーム新着ランキング')
    print('17：おもしろ人気ランキング')
    print('18：おもしろ新着ランキング')
    print('>')

    num = int(input())
    if num <= 18 and num > 0:

        if num == 1:
            url = 'http://b.hatena.ne.jp/hotentry.rss'
        elif num == 2:
            url = 'http://b.hatena.ne.jp/entrylist.rss'
        elif num == 3:
            url = 'http://b.hatena.ne.jp/hotentry/social.rss'
        elif num == 4:
            url = 'http://b.hatena.ne.jp/entrylist/social.rss'
        elif num == 5:
            url = 'http://b.hatena.ne.jp/hotentry/economics.rss'
        elif num == 6:
            url = 'http://b.hatena.ne.jp/entrylist/economics.rss'
        elif num == 7:
            url = 'http://b.hatena.ne.jp/hotentry/life.rss'
        elif num == 8:
            url = 'http://b.hatena.ne.jp/entrylist/life.rss'
        elif num == 9:
            url = 'http://b.hatena.ne.jp/hotentry/knowledge.rss'
        elif num == 10:
            url = 'http://b.hatena.ne.jp/entrylist/knowledge.rss'
        elif num == 11:
            url = 'http://b.hatena.ne.jp/hotentry/it.rss'
        elif num == 12:
            url = 'http://b.hatena.ne.jp/entrylist/it.rss'
        elif num == 13:
            url = 'http://b.hatena.ne.jp/hotentry/entertainment.rss'
        elif num == 14:
            url = 'http://b.hatena.ne.jp/entrylist/entertainment.rss'
        elif num == 15:
            url = 'http://b.hatena.ne.jp/hotentry/game.rss'
        elif num == 16:
            url = 'http://b.hatena.ne.jp/entrylist/game.rss'
        elif num == 17:
            url = 'http://b.hatena.ne.jp/hotentry/fun.rss'
        elif num == 18:
            url = 'http://b.hatena.ne.jp/entrylist/fun.rss'

        db.child("category").set({'url': url})

    else:
        print('変更しませんでした')


def getXml():
    global tagList
    data = db.child("category").get()

    url = data.val().get('url')
    f = urlopen(url)
    xml = f.read()
    root = ElementTree.fromstring(xml)
    for num, item in enumerate(root.findall('{http://purl.org/rss/1.0/}item')):
        title = item.find(
            '{http://purl.org/rss/1.0/}title').text.encode('cp932', "ignore")

        url = item.find(
            '{http://purl.org/rss/1.0/}link').text.encode('cp932', "ignore")
        articleList.append(
            {num: {'title': title.decode('cp932').replace(
                chr(165), '').replace(
                'u3000', ''),
                "url": url.decode('cp932'),
                'tag': {},
                'ave': 0
            }
            }
        )

        for index, tag in enumerate(item.findall('{http://purl.org/dc/elements/1.1/}subject')):
            tag = tag.text.encode('cp932', "ignore")
            tagD = tag.decode('cp932')

            tagList.setdefault(tag.decode('cp932').replace(
                '$', '').replace('#', '').replace(
                '[', '').replace(']', '').replace(
                '.', ''), 0)
            articleList[num].get(num).get('tag').setdefault(
                tag.decode('cp932'), tagList.get(tag.decode('cp932')))


def calcAve():

    for index, article in enumerate(articleList):
        ave = 0
        sum = 0

        tagDictLen = len(article.get(index).get("tag"))
        for tagValue in article.get(index).get("tag"):
            if article.get(index).get("tag").get(tagValue) is not None:
                sum += article.get(index).get("tag").get(tagValue)

        ave = sum / tagDictLen
        article.get(index)['ave'] = ave


def getMaxAveArticle():
    temp = -100000000
    global maxAveArticle

    for index, article in enumerate(articleList):
        num = article.get(index).get("ave")

        if num > temp and not article.get(index).get("title") in selectedArticle:
            temp = num
            maxAveArticle = article.get(index)

    return maxAveArticle


def reviewScore():
    print('1~5の5段階で評価してください．>')
    score = input()
    if score.isdecimal():
        score = int(score)
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
    else:
        print('今回は評価しませんでした')


def main():
    selectCategory()
    db.child("category").set({'url': url})
    getXml()
    calcAve()
    print(getMaxAveArticle())
    reviewScore()
    db.child("selectedArticle").push(dict(maxAveArticle).get('title'))
    db.child("tagList").set(tagList)


if __name__ == "__main__":
    main()
