import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="usertest",
  passwd="Th1s1s4P4ss!",
  database="videos"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)

# print(mydb)
