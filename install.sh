#!/bin/sh
#####################################################################
# Installations-Script für rtl_fm & multimon-ng sowie download des raspoc-Script in den Ordner /home/pi/py-sripte
# Das Script vorher mit "chmod +x install.sh" ausführbar machen
# mit "./install.sh" als root Prozess starten
######################################################################

# clear the screen
tput clear
 
# Move cursor to screen location X,Y (top left is 0,0)
tput cup 3 15
 
# Set a foreground colour using ANSI escape
tput setaf 3
echo "RASPOC - A multimon-ng & rtl_fm Feature-Script"
tput sgr0
tput cup 5 15
# Set reverse video mode
tput rev
echo "INSTALLATION LAEUFT..."
tput sgr0

tput cup 7 15
echo "1. rtl_fm herunterladen"
# RTL SDR Installation
# Install dependencies
apt-get update > hi.txt 2>&1
apt-get -y install git cmake build-essential libusb-1.0 qt4-qmake libpulse-dev libx11-dev sox > hi.txt 2>&1
tput cup 8 15
echo "2. rtl_fm compilieren"
# Fetch and compile rtl-sdr source
mkdir -p ~/src/ 
cd ~/src/
git clone git://git.osmocom.org/rtl-sdr.git >> hi.txt 2>&1
cd rtl-sdr
mkdir build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> hi.txt 2>&1
make >> hi.txt 2>&1
make install >> hi.txt 2>&1
ldconfig >> hi.txt 2>&1


tput cup 9 15
echo "3. multimon-ng herunterladen und kompilieren"

# Multimon-NG kompilieren und installieren:
git clone https://github.com/EliasOenal/multimonNG.git >> hi.txt 2>&1
cd multimonNG/
mkdir build
cd build
qmake ../multimon-ng.pro >> hi.txt 2>&1
make >> hi.txt 2>&1
make install >> hi.txt 2>&1

tput cup 10 15
echo "4. python-mysql Support installieren"

# Schritt 3:
# Pyton MySQL-Support installieren:
# (Das raspoc-Script benutzt eine nicht in der Standardversion von Python vorhandene MySQL-Libary welche noch installiert werden muss)
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar >> hi.txt 2>&1
tar xfv mysql-connector.tar >> hi.txt 2>&1
cd mysql-connector-python*
chmod +x ./setup.py
./setup.py install >> hi.txt 2>&1


tput cup 11 15
echo "5. Umgebung für Scripte erstellen - /home/pi/py-sripte"
# Schritt 4:
# Ordner für raspoc anlegen:
mkdir /home/pi/py-sripte && cd /home/pi/py-sripte
git clone https://github.com/Smith-fms/raspoc.git >> hi.txt 2>&1

tput cup 12 15
echo "6. Scripte ausführbar machen und die sdr_stick Treiber blacklisten"

#  Schritt 5:
# Script ausführbar machen:
cd raspoc
chmod +x *

# standard treiber des SDR-Sticks aus dem Kernelmodulen blacklisten
echo -e "# blacklist the DVB drivers to avoid conflict with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core" >> /etc/modprobe.d/raspi-blacklist_sdr.conf

tput cup 13 15
echo "Fertig!"
