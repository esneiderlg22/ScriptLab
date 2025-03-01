#!/bin/bash

sudo apt update && sudo apt upgrade

sudo apt install git && sudo apt install -y python3 python3-pip

mkdir -p ~/Esptool

cd ~/Esptool || exit

git clone https://github.com/esneiderlg22/ScriptLab.git

python3 -m pip install --break-system-packages esptool cowsay pyfiglet re

chmod 777 cargaMonitor.py

DESKTOP_PATH=~/$(xdg-user-dir DESKTOP)

# Crear el archivo en el escritorio
cat <<EOL > "$DESKTOP_PATH/ActualizarScript.desktop"
[Desktop Entry]
Name=Actualizar Script
Exec=lxterminal -e /usr/bin/python3 /home/pi/Esptool/cargaMonitor.py
Icon=utilities-terminal
Terminal=true
Type=Application
EOL

# Dar permisos de ejecución al archivo
chmod 777 "$DESKTOP_PATH/ActualizarScript.desktop"







