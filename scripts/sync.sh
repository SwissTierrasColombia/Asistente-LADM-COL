#!/bin/bash

# you can execute with $ watch ./scripts/sync.sh

# rationale: se busca la ruta del script para que no importe desde
# donde se ejecuta el .sh
# link: https://stackoverflow.com/questions/630372/determine-the-path-of-the-executing-bash-script
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
  DEFAULT_QGIS_PLUGIN_PATH="$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/asistente_ladm_col"
  echo "¿Dónde está la ruta destino de tu plugin?: [ $DEFAULT_QGIS_PLUGIN_PATH ]"
  read QGIS_PLUGIN_PATH
  if [ "$QGIS_PLUGIN_PATH" = "" ]
  then
    QGIS_PLUGIN_PATH="$DEFAULT_QGIS_PLUGIN_PATH"
  fi
  tee "$file" << EOF
# Establezca valores NOMBRE=VALOR sin espacios en el igual
ASISTENTE_LADM_DIR="$QGIS_PLUGIN_PATH"
EOF
  echo "Se ha modificado el archivo de configuración $MY_PATH/$file."
fi

source $file

# rationale: ir al directorio padre
cd "$MY_PATH"/..

echo "Sincronizando $ASISTENTE_LADM_DIR"
rsync -av asistente_ladm_col/ $ASISTENTE_LADM_DIR
