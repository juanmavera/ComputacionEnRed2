#!/bin/bash

# Actualizacion del sistema

cd ~

sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt autoclear

# Instalacion de Python y virtualenv

sudo apt install python-dev
sudo apt install python-virtualenv

# Instalacion de Mongo

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt update
sudo apt install mongodb-org

cat mongoRequirements.txt >> /etc/systemd/system/mongodb.service
systemctl daemon-reload

# Creacion del entorno virtual e instalacion de las librerias de python

cd app
virtualenv flask
. flask/bin/activate

pip install -r requeriments.txt
