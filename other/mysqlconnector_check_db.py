# Creates the db in myslq server

from mysql.connector import connection
import os
from dotenv import load_dotenv

load_dotenv()

my_connection = connection.MySQLConnection(
    host="localhost",
    user=os.environ.get("USER_DB"),
    password=os.environ.get("PASSWORD_DB"),
)

name_db = os.environ.get("NAME_DB")

my_cursor = my_connection.cursor()

my_cursor.execute("SHOW DATABASES")
databases = my_cursor.fetchall()

if (name_db,) not in databases:
    my_cursor.execute(f"CREATE DATABASE {name_db}")
    print(f"Database '{name_db}' created successfully")
else:
    print(f"Database '{name_db}' already exists")


if my_connection.is_connected():
    my_cursor.close()
    my_connection.close()
