#!/bin/bash

sudo apt update && sudo apt upgrade

sudo apt install git && sudo apt install -y python3 python3-pip

mkdir -p ~/Esptool

cd ~/Esptool || exit

git clone https://github.com/esneiderlg22/ScriptLab.git

pip3 install esptool cowsay pyfiglet





