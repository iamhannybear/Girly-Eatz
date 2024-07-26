import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = con.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS restaurant_db')
print('Database successfully created')