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
		rutacompdav = os.path.join(sys.argv[2], arch)
		ruta_dav_procesado = os.path.join(sys.argv[3], arch)
				
		arch_lock = rutacompdav + ".lock"
		arch_done = rutacompdav + ".done"
		if arch_lock in lista or arch_done in lista:
			continue
		
		lock_file = open(arch_lock, 'w')
		fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)

		archsalida = str(arch) + ".log"
		fn("scanpatvid", sys.argv[1], rutacompdav, archsalida)
		lock_file.close()

		shutil.move(rutacompdav, ruta_dav_procesado)
		# register the dav file processed

		time.sleep(2)
		lista = os.listdir(sys.argv[2])

if __name__ == "__main__":
	main()
