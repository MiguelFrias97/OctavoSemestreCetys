#!/bin/bash
p=$(pidof python)
echo $p
if [ -z $p ] ;
then
echo "No hay proceso de python corriendo"
else
sudo kill -sigkill $p
fi
