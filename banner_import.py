#!/usr/bin/python3
import os
import sys
import datetime
import time

def create_csv(archsalida, datos_from_log, datos_from_name):
    try:
        with open(archsalida, 'a+') as file:
            for data in datos_from_log:
                registro = ""
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
    datetimeobj = datetime.datetime.strptime(str_date, '%Y%m%d%H%M%S')
    date = datetimeobj.strftime('%d/%m/%Y')
    hour = datetimeobj.strftime('%H:%M:%S')
    return date, hour

def get_obs_nom(str_obs_nom, case):
    ans = str_obs_nom.split('-')
    return ans[case]

def procesa_nombre_archivo(string_name):
    datos_nombre = {}
    name_array = string_name.split('_')
    datos_nombre['cod_ciu'] = name_array[0]
    datos_nombre['cod_canal'] = name_array[1]
    datos_nombre['fecha_emision'], datos_nombre['hora_emision'] = format_date(name_array[2])
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
                    pos = line_array.index('MATCH')
                    log_data['nombre_spot'] = get_obs_nom(line_array[pos+1], 1)
                    log_data['observacion'] = get_obs_nom(line_array[pos+1], 0)
                    log_data['duracion'] = to_seconds(line_array[pos+2])
                    log_data['cod_rubro'] = line_array[pos+3]
                    log_data['cod_producto'] = line_array[pos+4]
                    log_data['cod_anunciante'] = line_array[pos+5].rstrip()
                    # linea procesada en log_data
                    lista_datos.append(log_data)
    except IOError:
        print("No se puede acceder al archivo", arch)
    return lista_datos

def main():
    if len(sys.argv) != 2:
        print("Modo de empleo:")
        print(sys.argv[0] + " DIR_DAV_LOGS")
        return
    lista = os.listdir(sys.argv[1])
    if not lista:
        print("No hay archivos en el directorio")

    fecha_registro = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    
    for arch in lista:
        if not arch.endswith(".log"):
            continue
        print("Procesando: ", arch)
        arch_log = os.path.join(sys.argv[1], arch)
        datos_log = procesa_log(arch_log)
        if not datos_log:
            continue
        datos_name_arch = procesa_nombre_archivo(arch)
        #arch_csv = arch_log + '.csv'
        arch_csv = 'banner_import-' + fecha_registro + '.csv'
        crea_csv = create_csv(arch_csv, datos_log, datos_name_arch)
        if crea_csv != 0:
            continue
        try:
            os.rename(arch_log, arch_log + '.imported')
        except:
            print("Error al renombrar archivo", arch_log)
        time.sleep(2)

if __name__ == "__main__":
  main()
