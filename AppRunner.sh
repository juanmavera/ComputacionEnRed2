#!/bin/bash

cd ~

sudo service mongod start

cd app/

. flask/bin/activate

cd ComputacionEnRed2/

python app.py
