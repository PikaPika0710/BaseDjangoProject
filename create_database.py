import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE " + os.getenv("DB_NAME"))
#
# for x in mycursor:
#     if x[0] == "todo_app":
#         print("found")
#     # print(x)
