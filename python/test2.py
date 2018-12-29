import pyrebase

config = {
    "apiKey": "AIzaSyDQFAWoIUx5I0g7yaSiIfqnPJL_2dmLxlI",
    "authDomain": "webex-4608e.firebaseapp.com",
    "databaseURL": "https://webex-4608e.firebaseio.com",
    "storageBucket": "webex-4608e.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
db.child("users").child("Morty")
data = {"name": "Mortimer Morty Smith"}
db.child("users").set(data)
db.child("users").set(3)

# data = {"name": "Mortimer 'Morty' Smith"}
# db.child("users").child("334").set(data)

users = db.child("users").get()
print(users.val())
