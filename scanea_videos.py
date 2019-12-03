#!/usr/bin/python3
import os
import sys
import subprocess
import time

def fn(comando, dirpat, archdav, archsalida):
	salida = subprocess.check_output([comando, dirpat, archdav])
	with open(archsalida, "w") as arch:
		arch.write(salida.decode())

def main():
	if len(sys.argv) != 3:
		print("Modo de empleo:")
		print(sys.argv[0], " DIR_PATRONES DIR_VIDEOS_DAV")
		return
	lista = os.listdir(sys.argv[2])
	for arch in lista:
		print("Procesando:", arch)
		rutacompdav = os.path.join(sys.argv[2], arch)
		arch_lock = str(arch) + ".lock"
		arch_done = str(arch) + ".done"
		# pending: update lista all the time
		if arch_lock in lista or arch_done in lista:
			continue
		archsalida = str(arch) + ".log"		
		fn("scanpatvid", sys.argv[1], rutacompdav, archsalida)
		# save video in server video
		# register the dav file processed
		# move dav file to processed dir
		time.sleep(2)

if __name__ == "__main__":
	main()
