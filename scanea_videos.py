#!/usr/bin/python3
import os
import sys
import subprocess
import shutil
import time
import fcntl

def fn(comando, dirpat, archdav, archsalida):
	salida = subprocess.check_output([comando, dirpat, archdav])
	with open(archsalida, "w") as arch:
		arch.write(salida.decode())

def main():
	if len(sys.argv) != 3:
		print("Modo de empleo:")
		print(sys.argv[0], " DIR_PATRONES DIR_VIDEOS_DAV DIR_VIDEOS_PROCESADOS")
		return
	lista = os.listdir(sys.argv[2])
	for arch in lista:
		print("Procesando:", arch)
		ruta_dav_recibido = os.path.join(sys.argv[2], arch)
				
		arch_lock = arch + ".lock"
		arch_done = arch + ".done"
		if arch_lock in lista or arch_done in lista:
			continue
				
		lock_file = open(ruta_dav_recibido + ".lock", "w+")
		fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)

		archsalida = str(arch) + ".log"
		fn("scanpatvid", sys.argv[1], ruta_dav_recibido, archsalida)
		
		done_file = open(ruta_dav_recibido + ".done", 'w')
		done_file.write("")
		done_file.close()
		
		lock_file.close()
		os.remove(lock_file)

		ruta_dav_procesado = os.path.join(sys.argv[3], arch)
		shutil.move(ruta_dav_recibido + ".done", ruta_dav_procesado + ".done")
		shutil.move(ruta_dav_recibido, ruta_dav_procesado)
		
		time.sleep(2)
		lista = os.listdir(sys.argv[2])

if __name__ == "__main__":
	main()
