#!/usr/bin/python3
import os
import sys
import subprocess
import shutil
import time
import fcntl

def fn(comando, dirpat, archdav, archsalida):
	salida = subprocess.check_output([comando, dirpat, archdav])
	try:
		with open(archsalida, "w") as arch:
			arch.write(salida.decode())
	except IOError as e:
		print("No se pudo abrir o escribir archivo  (%s)." % e)

def main():
	if len(sys.argv) != 4:
		print("Modo de empleo:")
		print(sys.argv[0], " DIR_PATRONES DIR_VIDEOS_DAV DIR_VIDEOS_PROCESADOS")
		return
	lista = os.listdir(sys.argv[2])
	if not lista:
		print("No hay archivos en el directorio")

	for arch in lista:
		if ".done" in arch or ".lock" in arch:
			continue

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
		
		try:
			with open(ruta_dav_recibido + ".done", 'w') as done_file:
				done_file.write("")
				done_file.close()
		except IOError as e:
			print("No se pudo abrir o escribir archivo (%s)." % e)
		
		lock_file.close()
		try:
			os.remove(lock_file)
    	except:
        	print("Error al eliminar el lock_file ", lock_file)

		try:
			os.makedirs(sys.argv[3])
		except FileExistsError:
			pass
		ruta_dav_procesado = os.path.join(sys.argv[3], arch)
		
		shutil.move(ruta_dav_recibido + ".done", ruta_dav_procesado + ".done")
		shutil.move(ruta_dav_recibido, ruta_dav_procesado)
		
		time.sleep(2)
		lista = os.listdir(sys.argv[2])

if __name__ == "__main__":
	main()
