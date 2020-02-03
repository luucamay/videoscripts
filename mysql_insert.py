from mysql_connection import mydb
import mysql.connector

mycursor = mydb.cursor()

sql = "INSERT INTO tvmencion (cod_canal, cod_ciu) VALUES (%s, %s)"
val = ("ATB", "Oruro")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

