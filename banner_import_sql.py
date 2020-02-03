import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="usertest",
    passwd="Th1s1s4P4ss!",
    database="videos"
)
# TODO check if successful connection

def get_ciudad(cod_ciu):
    cod_ciu = cod_ciu.split('-')[0]
    ciudad = ''
    mycursor = mydb.cursor()
    mycursor.execute("SELECT nom_ciu FROM tciudad")
    ciudad = mycursor.fetchone()[0]
    return ciudad

