import pyrebase
from firebasetoken import config


firebase = pyrebase.initialize_app(config)
db = firebase.database()

articleList = []
maxAveArticle = []

# data = db.child("selectedArticle").get()
# titleList = dict(data.val())
# for i in titleList.keys():
#     print(titleList.get(i))

data = db.child("category").get()
tagList = data.val()
print(tagList.get('url'))
