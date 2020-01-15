#!/usr/bin/python3
import os
import sys

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
        try:
            with open(arch_log) as f:
                print("log file has been found")
                # print(f.readlines())
                # Do something with the file
        except IOError:
            print("File not accessible")

    # process the text inside the log file

if __name__ == "__main__":
  main()
