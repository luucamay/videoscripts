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
    result = mycursor.fetchone()
    if result:
        ciudad = result[0]
    return ciudad

def get_canal(cod_canal):
    cod_canal = cod_canal[2:]
    canal = ''
    mycursor = mydb.cursor()
    sql = "SELECT nombre FROM tvcanal WHERE cod_canal = %s"
    val = (cod_canal, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    print(val, result)
    if result:
        canal = result[0]
    return canal