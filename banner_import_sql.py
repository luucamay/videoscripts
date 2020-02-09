#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def connect_db():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="usertest",
            passwd="Th1s1s4P4ss!",
            database="videos"
        )
        print("MySQL conexion abierta")
    except Error as e:
        print("Error al conectar a la base de datos MySQL. ", e)
    return connection

def close_connection(mydb):
    mydb.close()
    print("MySQL conexion cerrada")

def get_ciudad(cod_ciu, mydb):
    cod_ciu = cod_ciu.split('-')[1]
    ciudad = 'Ciudad no encontrada'
    mycursor = mydb.cursor()
    sql = "SELECT nom_ciu FROM tciudad WHERE cod_ciu = %s"
    val = (cod_ciu, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    mycursor.close
    if result:
        ciudad = result[0]
    return ciudad

def get_canal(cod_canal, mydb):
    cod_canal = cod_canal[2:]
    canal = 'Canal no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT nombre FROM tvcanal WHERE cod_canal = %s"
    val = (cod_canal, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    mycursor.close
    if result:
        canal = result[0]
    return canal

def get_rubro(cod_rubro, mydb):
    rubro = 'Rubro no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT nom_rubro FROM tvrubro WHERE cod_rubro = %s AND estado = 1"
    val = (cod_rubro, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    mycursor.close
    if result:
        rubro = result[0]
    return rubro

def get_anunciante(cod_anu, mydb):
    anunciante = 'Anunciante no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT anunciante FROM tvanunciante WHERE cod_anu = %s AND estado = 1"
    val = (cod_anu, )
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    mycursor.close
    if result:
        anunciante = result[0]
    return anunciante

def get_producto(cod_anu, cod_rubro, cod_prod, mydb):
    producto = 'Producto no encontrado'
    mycursor = mydb.cursor()
    sql = "SELECT nombre FROM tvproducto WHERE cod_anu = %s AND cod_rubro = %s AND cod_producto = %s AND estado = 1"
    val = (cod_anu, cod_rubro, cod_prod,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    mycursor.close
    if result:
        producto = result[0]
    return producto
