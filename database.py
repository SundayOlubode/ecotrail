import pymongo
import os
from dotenv import load_dotenv
load_dotenv('.env')

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
USER_TABLE_NAME = os.getenv("USER_TABLE_NAME")
COMMENT_TABLE_NAME = os.getenv("COMMENT_TABLE_NAME")

myclient = pymongo.MongoClient(MONGO_URL)

mydb = myclient[DB_NAME]
user_col = mydb[USER_TABLE_NAME]


def register_user(email, username, password):
    mydict = {"email": email, "username": username, "password": password}
    new_user = user_col.insert_one(mydict)
    return new_user


def login_user(email, password):
    user = user_col.find_one({"email": email, "password": password})
    return user
