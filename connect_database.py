import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="usertest",
  passwd="Th1s1s4P4ss!",
  database="videos"
)

print(mydb)
