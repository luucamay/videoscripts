from mysql_connection import mydb
import mysql.connector

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM tvmencion")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
