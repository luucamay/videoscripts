#!/bin/bash
#
# banner_csv_upload.sh - Sube archivos CSV al sistema para importar
#                        información de banners. La importación se
#                        realiza en «Menciones TV»
#                        IMC Menu: Menciones TV > Importar CSV
#
# 2020-02-16 Hardy Beltran Monasterios <hbeltran@jaltana.com>
#            - Versión inicial
#
####

URL="http://www.mc-bolivia.net/imc/transcripcion/menciones/save_csv.php"
AUTH="departamento:sistemas"
PATH="/bin:/usr/bin"

if [[ $# -ne 1 ]]; then
    echo "Illegal number of parameters"
    echo "Usage: $0 csv_file"
    exit 1
fi

CSVFILE="$1"

if [ ! -f "$CSVFILE" ]; then
    echo "$CSVFILE: file does not exist or is not readable"
    exit 2
fi

# Web form variables as used by program save_csv.php
VAR1='save_archivo=enviado'
VAR2='submit=Enviar'
VARFILE="csv=@${CSVFILE}"

TMPFILE=$(mktemp csvup.XXXXXXXXXXXX)
TMPEFILE=$(mktemp err.XXXXXXXXXXXX)

echo "Trying upload file: $CSVFILE"

curl -u $AUTH -F $VAR1 -F $VAR2 -F $VARFILE $URL > $TMPFILE 2> $TMPEFILE

if [ $? -ne 0 ]; then
    echo "Unable to upload file: $CSVFILE"
    echo "Curl error code returned: $?"
    echo "Error detail:"
    cat $TMPEFILE
    exit 3
fi

# Verify if CSV import has error
egrep -q 'ERROR:.*Abortando' $TMPFILE

if [ $? -eq 0 ]; then
    echo "ERROR: Al importar archivo CSV: $CSVFILE"
    cp $TMPFILE /var/tmp
    echo "Vea los detalles en el archivo: /var/tmp/$TMPFILE"
    exit 4
fi

# Verify if was successfull
grep -q 'Se importaron correctamente' $TMPFILE

if [ $? -eq 0 ]; then
    echo "Archivo CSV importado correctamente."
    cp $TMPFILE /var/tmp
    echo "Vea los detalles en el archivo HTML: /var/tmp/$TMPFILE"
    exit 0
fi

# We should never reach here. Some weird thing happened
exit 1
