# Creates the db in myslq server

from mysql.connector import connection

mydb = connection.MySQLConnection(host="localhost", user="root", password="1234567890")

my_cursor = mydb.cursor()

my_cursor.execute("SHOW DATABASES")
databases = my_cursor.fetchall()

if ("our_users",) not in databases:
    my_cursor.execute("CREATE DATABASE our_users")
    print("Database 'our_users' created successfully")
else:
    print("Database 'our_users' already exists")

if mydb.is_connected():
    my_cursor.close()
    mydb.close()
