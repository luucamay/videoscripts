#!/usr/bin/python3
import os
import sys
import datetime
import time
import logging
from banner_import_sql import *

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
csv_row_number = 0

def create_csv(archsalida, datos_from_log, datos_from_name):
    try:
        with open(archsalida, 'a+') as file:
            # if no rows have been written in the csv
            global csv_row_number
            if csv_row_number == 0 :
                header = 'N;FECHA DE EMISION;MEDIO;CIUDAD;RUBRO;ANUNCIANTE;PRODUCTO;OBSERVACION;DURACION SEG.;HORA EMISION;NOMBRE' + '\n'
                file.write(header)

            for data in datos_from_log:
                csv_row_number += 1
                registro = ""
                registro += str(csv_row_number) + ';'
                registro += datos_from_name['fecha_emision'] + ';'
                registro += datos_from_name['cod_canal'] + ';'
                registro += datos_from_name['cod_ciu'] + ';'
                registro += data['cod_rubro'] + ';'
                registro += data['cod_anunciante'] + ';'
                registro += data['cod_producto'] + ';'
                registro += data['observacion'] + ';'
                registro += str(data['duracion']) + ';'
                registro += datos_from_name['hora_emision'] + ';'
                registro += data['nombre_spot'] + '\n'
                file.write(registro)
    except IOError:
        print("No se puede acceder al archivo", archsalida)
    return 0

def format_date(str_date):
    date = hour = ''
    try:
        datetimeobj = datetime.datetime.strptime(str_date, '%Y%m%d%H%M%S')
        date = datetimeobj.strftime('%d/%m/%Y')
        hour = datetimeobj.strftime('%H:%M:%S')
    except ValueError:
        print ("'", str_date, "' no es una fecha")
    return date, hour

def get_obs_nom(str_obs_nom):
    ans = {'obs':'', 'name':''}
    tmp = str_obs_nom.split('-')
    if len(tmp) == 2:
        ans['obs'] = tmp[0]
        ans['name'] = tmp[1]
    elif len(tmp) == 1:
        ans['name'] = tmp[0]
    else:
        print('error in observation and name')
    return ans

def procesa_nombre_archivo(string_name, conexion):
    # BO-200_ch1_main_20200128072000_20200128073000.dav.log
    datos_nombre = {}
    name_array = string_name.split('_')
    if len(name_array) != 5:
        return datos_nombre
    datos_nombre['cod_ciu'] =  get_ciudad(name_array[0], conexion)
    datos_nombre['cod_canal'] = get_canal(name_array[1], conexion)
    datos_nombre['fecha_emision'], datos_nombre['hora_emision'] = format_date(name_array[3])
    return datos_nombre

def to_seconds(string_time):
    string_time = string_time[3:]
    x = time.strptime(string_time, '%H:%M:%S')
    total_sec = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return int(total_sec)

def procesa_log_data(arch, conexion):
    lista_datos = []
    try:
        with open(arch) as file:
            for line in file:
                line_array = line.split(' ')
                line_set = set(line_array)
                if 'MATCH' in line_set:
                    log_data = {}
                    pos = line_array.index('MATCH')
                    obs_name_dic = get_obs_nom(line_array[pos+1])
                    log_data['nombre_spot'] = obs_name_dic['name']
                    log_data['observacion'] = obs_name_dic['obs']
                    log_data['duracion'] = to_seconds(line_array[pos+2])
                    cod_rubro = line_array[pos+3][1:]
                    cod_producto = line_array[pos+4][1:]
                    cod_anu = line_array[pos+5].rstrip()[1:]
                    log_data['cod_rubro'] = get_rubro(cod_rubro, conexion)
                    log_data['cod_anunciante'] = get_anunciante(cod_anu, conexion)
                    log_data['cod_producto'] = get_producto(cod_anu, cod_rubro, cod_producto, conexion)
                    # linea procesada en log_data
                    lista_datos.append(log_data)
                    logging.debug('- Registro: %s', log_data['nombre_spot'])

    except IOError:
        print("No se puede acceder al archivo", arch)
    return lista_datos

def procesa_log_file(arch_log):
    """
    Toma un archivo .log generado por scanpatvid y procesa su contenido
    El resultado del proceso se escribe en un archivo CSV.
    """
    logging.debug('Procesando log: %s', arch_log)

    conexion = connect_db()
    if not conexion:
        return
    datos_name_arch = procesa_nombre_archivo(arch_log, conexion)

    # making sure none of the fields are empty strings from the name of the file
    if not (datos_name_arch and datos_name_arch['fecha_emision'] and datos_name_arch['hora_emision'] and datos_name_arch['cod_ciu'] and datos_name_arch['cod_canal']):
        print('Formato del nombre de archivo ', arch,' no es el correcto')
        close_connection(conexion)
        return
    
    datos_log = procesa_log_data(arch_log, conexion)
    if datos_log:
        # The filename ends with '.dav.log', eight characters
        arch_csv = arch_log[0:len(arch_log)-8] + '.csv'
        crea_csv = create_csv(arch_csv, datos_log, datos_name_arch)
        if crea_csv == 0:
            print('Archivo CSV generado:', arch_csv)
        else:
            close_connection(conexion)  
            print('No se pudo escribir en el archivo CSV', arch_csv)      
            return

    close_connection(conexion)
    try:
        os.rename(arch_log, arch_log + '.imported')
    except:
        print("Error al renombrar archivo", arch_log)

def main():
    """
    Cuando se invoca el script directamente, se procesa
    varios archivos .log en un directorio
    """
    if len(sys.argv) != 2:
        print("Modo de empleo:")
        print(sys.argv[0] + " DIR_DAV_LOGS")
        return
    lista = os.listdir(sys.argv[1])
    if not lista:
        print("No hay archivos .log en el directorio")

    for arch in lista:
        if not arch.endswith(".log"):
            continue

        arch_log = os.path.join(sys.argv[1], arch)
        procesa_log_file(arch_log)

if __name__ == "__main__":
  main()
