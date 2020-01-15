#!/usr/bin/python3
import os
import sys
import datetime
import time

def format_date(str_date):
    datetimeobj = datetime.datetime.strptime(str_date, '%Y%m%d%H%M%S')
    date = datetimeobj.strftime('%d/%m/%Y')
    hour = datetimeobj.strftime('%H:%M:%S')
    return date, hour

def get_obs(str_observacion):
    obs = str_observacion.split('.')
    obs = obs[0].split('-')
    return obs[1]

def procesa_nombre_archivo(string_name):
    datos_nombre = {}
    name_array = string_name.split('_')
    datos_nombre['cod_ciu'] = name_array[0]
    datos_nombre['cod_canal'] = name_array[1]
    datos_nombre['fecha_emision'], datos_nombre['hora_emision'] = format_date(name_array[2])
    datos_nombre['observacion'] = get_obs(name_array[3])
    return datos_nombre

def to_seconds(string_time):
    string_time = string_time[3:]
    x = time.strptime(string_time, '%H:%M:%S')
    total_sec = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return int(total_sec)

def procesa_log(arch):
    lista_datos = []
    try:
        with open(arch) as file:
            for line in file:
                line_array = line.split(' ')
                line_set = set(line_array)
                if 'MATCH' in line_set:
                    log_data = {}
                    for i in range(len(line_array)):
                        if line_array[i] == 'MATCH':
                            log_data['nombre_spot'] = line_array[i+1]
                            log_data['duracion'] = to_seconds(line_array[i+2])
                            log_data['cod_rubro'] = line_array[i+3]
                            log_data['cod_producto'] = line_array[i+4]
                            log_data['cod_anunciante'] = line_array[i+5].rstrip()
                    # linea procesada en log_data
                    lista_datos.append(log_data)
    except IOError:
        print("No se puede acceder al archivo", arch)
    return lista_datos

def main():
    # process the string name
    if len(sys.argv) != 2:
        print("Modo de empleo:")
        print(sys.argv[0] + " DIR_DAV_LOGS")
        return
    lista = os.listdir(sys.argv[1])
    if not lista:
        print("No hay archivos en el directorio")
    for arch in lista:
        if not arch.endswith(".log"):
            continue
        print("Procesando: ", arch)
        arch_log = os.path.join(sys.argv[1], arch)
        datos = procesa_log(arch_log)
        # dictionary
        datos_name_arch = procesa_nombre_archivo(arch)
        print(datos)
        print(datos_name_arch)

    # process the text inside the log file

if __name__ == "__main__":
  main()
