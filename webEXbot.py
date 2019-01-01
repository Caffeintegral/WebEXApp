from urllib.request import urlopen
from xml.etree import ElementTree
import pyrebase
from firebasetoken import config
from discordToken import dToken
import discord
from discord.ext import commands


firebase = pyrebase.initialize_app(config)
db = firebase.database()

client = commands.Bot(command_prefix='', description='')
token = dToken

articleList = []
maxAveArticle = []
selectedArticle = []

isRead = False

data = db.child("tagList").get()
tagList = dict(data.val())

data = db.child("selectedArticle").get()
titleList = dict(data.val())
for i in titleList.keys():
    selectedArticle.append(titleList.get(i))

categoryNameList = ['1：総合人気ランキング', '2：総合新着ランキング',
                    '3：世の中人気ランキング', '4：世の中新着ランキング',
                    '5：政治と経済人気ランキング', '6：政治と経済新着ランキング',
                    '7：暮らし人気ランキング', '8：暮らし新着ランキング',
                    '9：学び人気ランキング', '10：学び新着ランキング',
                    '11：テクノロジー人気ランキング', '12：テクノロジー新着ランキング',
                    '13：エンタメ人気ランキング', '14：エンタメ新着ランキング',
                    '15：アニメとゲーム人気ランキング', '16：アニメとゲーム新着ランキング',
                    '17：おもしろ人気ランキング', '18：おもしろ新着ランキング']


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('category'):
        msg = discord.Embed(
            title="カテゴリー一覧", description="例．ch-cate 1 で，総合人気ランキング", color=0x80ffff)
        msg.add_field(name='1：総合人気ランキング', value='ch-cate 1', inline=True)
        msg.add_field(name='2：総合新着ランキング', value='ch-cate 2', inline=True)
        msg.add_field(name='3：世の中人気ランキング', value='ch-cate 3', inline=True)
        msg.add_field(name='4：世の中新着ランキング', value='ch-cate 4', inline=True)
        msg.add_field(name='5：政治と経済人気ランキング', value='ch-cate 5', inline=True)
        msg.add_field(name='6：政治と経済新着ランキング', value='ch-cate 6', inline=True)
        msg.add_field(name='7：暮らし人気ランキング', value='ch-cate 7', inline=True)
        msg.add_field(name='8：暮らし新着ランキング', value='ch-cate 8', inline=True)
        msg.add_field(name='9：学び人気ランキング', value='ch-cate 9', inline=True)
        msg.add_field(name='10：学び新着ランキング', value='ch-cate 10', inline=True)
        msg.add_field(name='11：テクノロジー人気ランキング', value='ch-cate 11', inline=True)
        msg.add_field(name='12：テクノロジー新着ランキング', value='ch-cate 12', inline=True)
        msg.add_field(name='13：エンタメ人気ランキング', value='ch-cate 13', inline=True)
        msg.add_field(name='14：エンタメ新着ランキング', value='ch-cate 14', inline=True)
        msg.add_field(name='15：アニメとゲーム人気ランキング',
                      value='ch-cate 15', inline=True)
        msg.add_field(name='16：アニメとゲーム新着ランキング',
                      value='ch-cate 16', inline=True)
        msg.add_field(name='17：おもしろ人気ランキング', value='ch-cate 17', inline=True)
        msg.add_field(name='18：おもしろ新着ランキング', value='ch-cate 18', inline=True)

        await client.send_message(message.channel, embed=msg)

    if message.content.startswith('help'):
        msg = discord.Embed(
            title="コマンド一覧",  color=0x80ffff)
        msg.add_field(name='category',
                      value='カテゴリの一覧を確認することができます．', inline=True)
        msg.add_field(
            name='ch-cate 数字', value='カテゴリーの設定を変更することができます．例えば「ch-cate 2」でカテゴリー2の総合新着ランキングに変更できます．', inline=True)
        msg.add_field(name='get', value='記事を推薦してもらうことができます', inline=True)
        msg.add_field(name='4：review 数字',
                      value='記事をレビューすることができます．例えば「review 2」で5段階評価で2という評価ができます．', inline=True)

        await client.send_message(message.channel, embed=msg)

    if message.content.startswith('ch-cate'):
        reply = message.content.split()  # スペースごとに分割
        num = reply[1]  # １つ目の引数を取得
        global url
        if num.isdecimal():
            num = int(num)
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

            msg = categoryNameList[num - 1] + 'に，変更しました．'

            db.child("category").set({'url': url})

        await client.send_message(message.channel, msg)

    if message.content.startswith('get'):
        global isRead
        if client.user != message.author:
            getXml()
            calcAve()
            getMaxAveArticle()
            isRead = True
            destext = "読み終わったら評価しましょう！ review 2 で評価2(5段階評価で1~5)"
            msg = discord.Embed(
                title=dict(maxAveArticle).get('title'), url=dict(maxAveArticle).get('url'), description=destext, color=0x80ffff)

            db.child("selectedArticle").push(dict(maxAveArticle).get('title'))
            await client.send_message(message.channel, embed=msg)

    if message.content.startswith('review'):
        global isRead
        reply = message.content.split()
        score = reply[1]

        if score.isdecimal() and isRead:
            score = int(score)
            if score <= 5 and score > 0:
                num = 0
                if score == 1:
                    num = -1
                    msg = '★'
                elif score == 2:
                    num = -0.5
                    msg = '★★'
                elif score == 3:
                    num = 0
                    msg = '★★★'
                elif score == 4:
                    num = 0.5
                    msg = '★★★★'
                elif score == 5:
                    num = 1
                    msg = '★★★★★'
                for tag in maxAveArticle.get('tag'):
                    temp = tagList.get(tag)
                    sum = temp + num
                    tagList[tag] = sum
                    print(tag + ':' + str(tagList.get(tag)))

        else:
            msg = '記事を読んでください．コマンドは get です．'

        isRead = False
        db.child("tagList").set(tagList)
        await client.send_message(message.channel, msg)


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
    client.run(token)


if __name__ == "__main__":
    main()
