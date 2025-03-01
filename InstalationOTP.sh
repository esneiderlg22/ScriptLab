#!/bin/bash

sudo apt update && sudo apt upgrade

sudo apt install git && sudo apt install -y python3 python3-pip

mkdir -p ~/Esptool

cd ~/Esptool || exit

git clone https://github.com/esneiderlg22/ScriptLab.git

python3 -m pip install --break-system-packages esptool cowsay pyfiglet

chmod 777 /home/pi/Esptool/ScriptLab/cargaMonitor.py

DESKTOP_PATH=~/$(xdg-user-dir DESKTOP)

# Crear el archivo en el escritorio
echo "[Desktop Entry]
Name=Actualizar Script
Exec=lxterminal -e /usr/bin/python3 /home/pi/Esptool/ScriptLab/cargaMonitorRaspbian.py
Icon=utilities-terminal
Terminal=true
Type=Application" > /home/pi/Desktop/ActualizarScript.desktop

# Dar permisos de ejecución
chmod +x /home/pi/Desktop/ActualizarScript.desktop







