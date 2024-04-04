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
comment_col = mydb[COMMENT_TABLE_NAME]


def create_comment(comment, username, chart_tag):
    mydict = {"comment": comment, "username": username, "chart_tag": chart_tag}
    new_comment = comment_col.insert_one(mydict)
    return new_comment


def fetch_all_comments(chart_tag):
    comments = comment_col.find({"chart_tag": chart_tag})
    return comments


def register_user(email, username, password):
    mydict = {"email": email, "username": username, "password": password}
    new_user = user_col.insert_one(mydict)
    return new_user


def login_user(email, password):
    user = user_col.find_one({"email": email, "password": password})
    return user


def get_user_by_email(email):
    user = user_col.find_one({"email": email})
    return user


def get_user_by_username(username):
    user = user_col.find_one({"username": username})
    return user


def fetch_all_users():
    users = user_col.find()
    print('Users', users)
    return users
