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
    if result:
        canal = result[0]
    return canal

def get_rubro(cod_rubro):
    rubro = 'Rubro no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT nom_rubro FROM tvrubro WHERE cod_rubro = %s AND estado = 1"
    val = (cod_rubro, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        rubro = result[0]
    return rubro

def get_anunciante(cod_anu):
    anunciante = 'Anunciante no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT anunciante FROM tvanunciante WHERE cod_anu = %s AND estado = 1"
    val = (cod_anu, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        anunciante = result[0]
    return anunciante

def get_producto(cod_anu, cod_rubro, cod_prod):
    producto = 'Producto no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT nombre FROM tvproducto WHERE cod_anu = %s AND cod_rubro = %s AND cod_producto = %s AND estado = 1"
    val = (cod_anu, cod_rubro, cod_prod,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        producto = result[0]
    return producto