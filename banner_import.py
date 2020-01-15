#!/usr/bin/python3
import os
import sys

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
                            log_data['duracion'] = line_array[i+2]
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
        if not arch.endswith(".dav"):
            continue
        print("Procesando: ", arch)
        arch_dav = os.path.join(sys.argv[1], arch)
        arch_log = arch_dav + ".log"
        datos = procesa_log(arch_log)
        print(datos)

    # process the text inside the log file

if __name__ == "__main__":
  main()
