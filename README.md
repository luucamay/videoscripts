# Videoscripts
Un repositorio para guardar algún script en python para resolver problemas de concurrencia

## Procesar videos (scanea_videos.py)
Para esta parte utiliza el script 'scanea_videos.py'.

1. Del directorio **/recibido** toma un archivo.dav
2. Verifica si está siendo procesado (.lock) o ya ha sido procesado (.done)
    1. los archivos .lock estoy asumiendo que estarán en el mismo directorio de **/recibido**
    2. la misma pregunta para los archivos .done estos se encuentran en el mismo directorio de **/recibido**, pero luego se mueven junto con los archivos .dav al directorio **/procesado**
3. Si no se cumplen las condiciones del paso 2, empezamos a procesar este archivo.dav
4. Se crea el archivo.lock en el directorio **/recibido**
5. Procesa el archivo.dav con scanpatvid
6. Revisamos si el proceso concluye correctamente (acá pienso que se debería usar un comando que revise un proceso exitoso, tal vez fn podría retornar un valor si hay un error)
7. Si el proceso tiene éxito, crea el archivo.done y muevelo a **/procesado** junto con el archivo.dav
8. Registra el error o el éxito en el archivo.log 
9. Este archivo.log he decidido almacenarlo en el servidor que procesa el archivo
10. Actualiza la lista de archivos

## Procesar logs para generar archivos CSV (banner_import_py)
Para esta parte utiliza el script 'banner_import.py'.

Este script recibe un solo parametro que es el directorio de archivos logs que han sido generados despues de haber procesado los archivos.dav.

El script primero verifica que el archivo que esta por procesar tiene la extensión '.log' y luego lo procesa para añadir un registro en una línea al archivo CSV generado por cada vez que se ejecuta el script.

### Recomendacion
Importante checar que el formato del nombre del archivo.log y del contenido dentro del log sea el esperado por el script.

### Requerimientos
Instala **mysql-connector**

```
pip3 install mysql-connector
```

### Como funciona
Descarga los archivos:
- 'banner_import.py'
- 'banner_import_sql.py'

Ambos archivos deben estar en el mismo directorio.

Para ejecutar el script utiliza el siguiente comando:

```
python3 banner_import.py 'DIRECTORIO DE ARCHIVOS LOG'
```
