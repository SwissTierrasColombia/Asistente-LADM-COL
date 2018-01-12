#!/bin/bash

# you can execute with $watch ./scripts/sync.sh

# rationale: se busca la ruta del script para que no importe desde
# donde se ejecuta el .sh
MY_PATH="`dirname \"$0\"`"              # relative
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$MY_PATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  exit 1  # fail
fi
#echo "$MY_PATH"

# rationale: ir al directorio scripts
cd "$MY_PATH"

# rationale: si no existe el archivo de configuracion lo crea
# link: https://stackoverflow.com/questions/4511403/bash-create-a-file-if-it-does-not-exist-otherwise-check-to-see-if-it-is-writea
file=scripts.conf
if [[ ! -e "$file" ]]
then
  tee "$file" << EOF
# Establezca valores NOMBRE=VALOR sin espacios en el igual
ASISTENTE_LADM_DIR="/home/jorge/bin/QGIS/build-master/output/python/plugins/Asistente-LADM_COL/"
EOF
  echo "Modifique el archivo $MY_PATH/$file a su conveniencia."
fi

source $file

# rationale: ir al directorio padre
cd "$MY_PATH"/..

echo "Sincronizando $ASISTENTE_LADM_DIR"
rsync -av Asistente-LADM_COL/ $ASISTENTE_LADM_DIR
