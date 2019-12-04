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
		fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)

		archsalida = str(arch) + ".log"
		fn("scanpatvid", sys.argv[1], rutacompdav, archsalida)
		lock_file.close()
		done_file = open(arch_done, 'w')
		done_file.write("")
		done_file.close()
		# remove lock file
		os.remove(lock_file)

		shutil.move(rutacompdav, ruta_dav_procesado)
		shutil.move(arch_done, ruta_dav_procesado + ".done")
		# register the dav file processed: archsalida ya tiene ese registro, es un archivo.log, en qué debería cambiar?

		time.sleep(2)
		lista = os.listdir(sys.argv[2])

if __name__ == "__main__":
	main()
