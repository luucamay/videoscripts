#!/usr/bin/python3
import os
import sys
import subprocess
import shutil
import time
import fcntl
import errno

videotool='/bin/true'
videotool='scanpatvid'
maxtime=7200

def fn(comando, dirpat, archdav, archsalida):
	errorcode = 0
	arch = open(archsalida, "a+")
	try:
		salida = subprocess.check_output([comando, dirpat, archdav], stderr=arch, timeout=maxtime)
	except subprocess.CalledProcessError as salidaexc:
		errorcode = salidaexc.returncode
	except subprocess.TimeoutExpired as t:
		errorcode = 124

	if errorcode == 0:
		arch.write(salida.decode())
	elif errorcode == 124:
		arch.write("Tiempo agotado al procesar: '" + archdav + "'\n")
	arch.close()

	return errorcode

def main():
	if len(sys.argv) != 4:
		print("Modo de empleo:")
		print(sys.argv[0] + " DIR_PATRONES DIR_VIDEOS_DAV DIR_VIDEOS_PROCESADOS")
		return
	lista = os.listdir(sys.argv[2])
	if not lista:
		print("No hay archivos en el directorio")

	for arch in lista:
		if not arch.endswith(".dav"):
			continue

		print("Procesando:", arch)
		ruta_dav_recibido = os.path.join(sys.argv[2], arch)
				
		arch_lock = arch + ".lock"
		arch_done = arch + ".done"
		if arch_lock in lista or arch_done in lista:
			continue

		lock_file = open(ruta_dav_recibido + ".lock", "w+")
		fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
		
		archsalida = ruta_dav_recibido + ".log"
		procesa_video = fn(videotool, sys.argv[1], ruta_dav_recibido, archsalida)

		if procesa_video == 0 or procesa_video == 124:	
			try:
				with open(ruta_dav_recibido + ".done", 'w') as done_file:
					done_file.write("")
					done_file.close()
			except IOError as e:
				print("No se pudo abrir o escribir archivo (%s)." % e)
			
			try:
				os.makedirs(sys.argv[3])
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise
			ruta_dav_procesado = os.path.join(sys.argv[3], arch)
			
			shutil.move(ruta_dav_recibido + ".done", ruta_dav_procesado + ".done")
			shutil.move(ruta_dav_recibido + ".log", ruta_dav_procesado + ".log")
			shutil.move(ruta_dav_recibido, ruta_dav_procesado)
			lista_png = os.listdir(".")
			for arch_png in lista_png:	
				if arch_png.endswith(".png"):
					print ("Moviendo archivo png: " + arch_png)
					ruta_png_generado = os.path.join(".", arch_png)
					ruta_png_destino = os.path.join(sys.argv[3], arch_png)
					shutil.move(ruta_png_generado, ruta_png_destino)

		lock_file.close()
		try:
			os.remove(ruta_dav_recibido + ".lock")
		except:
			print("Error al eliminar el lock_file ", ruta_dav_recibido + ".lock")

		time.sleep(2)
		lista = os.listdir(sys.argv[2])

if __name__ == "__main__":
	main()
