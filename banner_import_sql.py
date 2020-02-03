import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="usertest",
    passwd="Th1s1s4P4ss!",
    database="videos"
)
# TODO check if successful connection

def get_ciudad(cod_ciu):
    cod_ciu = cod_ciu.split('-')[1]
    ciudad = ''
    mycursor = mydb.cursor()
    sql = "SELECT nom_ciu FROM tciudad WHERE cod_ciu = %s"
    val = (cod_ciu, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()[0]
    if result:
        ciudad = result
    return ciudad

def get_canal(cod_canal):
    canal = ''
    mycursor = mydb.cursor()
    mycursor.execute("SELECT nombre FROM tvcanal")
    canal = mycursor.fetchone()[0]
    return canal