# import bs4
import requests
import os
import time
import sqlite3
import json

# SQL_Path = os.path.join(os.getcwd(),"./data/DataBase/Questions.db")

# conn = sqlite3.connect(SQL_Path)

# cur = conn.cursor()

# cur.execute("CREATE TABLE IF NOT EXISTS INFO(id TEXT PRIMARY KEY,key INTEGER)")
# cur.execute("INSERT INTO INFO values(?,?)",[("Ver",1),("Time",time.time())])

header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}

content = requests.get("https://www.xinjiaoyu.com/api/v3/server_questions/category/attribute/22",headers=header)

if content.status_code != 200:
    exit()

content = json.loads(content.text)

print(content)