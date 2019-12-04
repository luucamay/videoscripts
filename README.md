## videoscripts
Un repositorio para guardar algún script en python para resolver problemas de concurrencia

## Descripción general de funcionamiento del script

1. Del directorio **/recibido** toma un archivo.dav
2. Verifica si está siendo procesado (.lock) o ya ha sido procesado (.done)
    1. los archivos .lock estoy asumiendo que estarán en el mismo directorio de **/recibido**, o prefieres que estén en el servidor desde donde se procesa, lo cuál no creo que sea conveniente porque los otros servidores procesadores no sabrían dónde buscar el .lock file
    2. la misma pregunta para los archivos .done estos se encuentran en el mismo directorio de **/recibido**, pero luego se mueven junto con los archivos .dav al directorio **/procesado**
3. Si no se cumplen las condiciones del paso 2, empezamos a procesar este archivo.dav
4. Se crea el archivo.lock en el directorio **/recibido**
5. Procesa el archivo.dav con scanpatvid
6. Revisamos si el proceso concluye correctamente (acá pienso que se debería usar un comando que revise un proceso exitoso)
7. Si el proceso tiene éxito, crea el archivo.done y muevelo a **/procesado** junto con el archivo.dav
8. Registra el error o el éxito en el archivo.log 
9. Este archivo.log he decidido almacenarlo en el servidor que procesa el archivo

