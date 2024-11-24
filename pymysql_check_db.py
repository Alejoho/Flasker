import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

my_connection = pymysql.connect(
    host="localhost",
    user=os.environ.get("USER_DB"),
    password=os.environ.get("PASSWORD_DB"),
)

name_db = os.environ.get("NAME_DB")

try:
    with my_connection.cursor() as my_cursor:
        my_cursor.execute("SHOW DATABASES")
        databases = my_cursor.fetchall()

        if (name_db,) not in databases:
            my_cursor.execute(f"CREATE DATABASE {name_db}")
            print(f"Database '{name_db}' created successfully")
        else:
            print(f"Database '{name_db}' already exists")
finally:
    my_connection.close()
