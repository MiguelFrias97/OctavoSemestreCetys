Procedimiento para configurar RFID (MFRC522)

Primero entrar a raspi-config como root y habilitar SPI.
Para corroborar que se encuentre habilitado, entrar a /boot/config.txt y 
revisar que la linea dtparam=spi=on este descomentada.

despues, debe hacer reboot

revisar que los dispositivos se encuentren funcionando:
lsmod | grep spi , deben aparecer:
/dev/spidev.0.0 y/o /dev/spidev1.1 (o algo similar)


Probablemente sea necesario:
apt update
apt upgrade
apt install python-dev
apt install python-spidev

clonar repositorio de github:
git clone https://github.com/lthiery/SPI-Py.git
git checkout 8cce26b9ee6e69eb041e9d5665944b88688fca68
python setup.py install (como root)

Descarga Archivos para utiliza RFID.

