#!/bin/bash

# Actualizacion del sistema
echo "Updating System..."
cd ~

sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt autoclear

echo "System upgraded"

# Instalacion de Python y virtualenv

echo "Installing Python..."
sudo apt install python-dev
echo "Python Instaled"

echo "Installing VirtualEnv"
sudo apt install python-virtualenv
echo "VirtualEnv Installed"

# Instalacion de Mongo

echo "Installing Mongo DB..."

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt update
sudo apt install mongodb-org

cat mongoRequirements.txt >> /etc/systemd/system/mongodb.service
systemctl daemon-reload

echo "Mongo DB Installed"

# Creacion del entorno virtual e instalacion de las librerias de python

echo "Creating VirtualEnv..."
cd app
virtualenv flask
. flask/bin/activate
echo "VirtualEnv Created"

echo "Instaling Python Requirements"
pip install -r requeriments.txt
echo "Python Libraries Installed"

. flask/bin/deactivate
# Instalacion del servicio de DNS

echo "Setting Up DNS Service"
cd ~

mkdir duckdns

mv ~/app/duck.sh ~/duckdns/
mv ~/app/duck_daemon.sh ~/duckdns/

cd duckdns

chmod 700 duck.sh

chmod +x duck_daemon.sh
sudo chown root duck_daemon.sh
sudo chmod 744 duck_daemon.sh

sudo ln -s ~/duckdns/duck_daemon.sh /etc/rc2.d/S10duckdns

echo "DNS Servide Ready"

echo "Please, Reboot the system"
