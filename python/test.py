# dict = {"yamada": 75, "endou": 82}


# list = dict.keys()
# print(dict.keys())    # ["yamada", "endou"]

# nowArticleList = [
#     {'title': 'aaa', 'tag': 1},
#     {'title': 'bbb', 'tag': 2},
#     {'title': 'ccc', 'tag': 3}
# ]

# nowArticleTags = [
#     {'tag': 1, 'name': 'afo'},
#     {'tag': 2, 'name': '72'},
#     {'tag': 3, 'name': '334'}
# ]

# articleDict = {i['tag']: i for i in nowArticleTags}

# for article in nowArticleList:
#     article.update({'tag': articleDict[article['tag']]})

# print(nowArticleList)
party = []

pokemon1 = {'title': {"url": 'www.afo',
                      'tag': {'HTML': 0, 'js': 0.5, 'CSS': -1}}}
# pokemon2 = {"afo": {"タイプ": "334"}}

party.append(pokemon1)
# party.append(pokemon2)

print(party[0].get("title").get('url'))
print(party[0].get("title").get('tag').get('HTML'))

party[0].get("title").get('tag').setdefault('ts', 1.2)
# party.append(pokemon2)

print(party[0].get("title").get('tag'))
print(party[0].get("title").get('tag').get('ts'))


# import pickle

# sample_list = ["asd", "afo", "asdasdasf"]
# f = open('sample.binaryfile', 'wb')
# pickle.dump(sample_list, f)
# f.close
# def a():
#     print("334")


# def main():
#     a()


# if __name__ == "__main__":
#     main()
