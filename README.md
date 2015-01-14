This is only a python-script for manipulate outputs of rtl_fm and multimon-ng. This script writes data in mysql for ZVEI, FMS and POCSAG. It provides features for filtering and manipulating.

At the first Lines you have to fill in your own details like SQL-Server, frequencies etc. Please consider, it´s for german language! 

<p align="center">!!!!<br>
Please attention! The install.sh is BETA! There is no guarantee for working on a RaspPi.<br>
!!!!</p>

<H3>Short Usage</H3>
RASPOC - ein kleines python-Script für rtl_fm und multimon_ng getestes auf Raspberry Pi und Cubieboard<br>
-- Pyton MySQL-Support installieren<br>
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O<br>
mysql-connector.tar && tar xfv mysql-connector.tar && cd mysql-connector-python* && chmod +x ./setup.py && sudo ./setup.py install<br><br>
<b>-- USAGE:<br></b>
sudo ./multimon_rtl_mysql.py [KANAL] [DEVICENUMBER] [DEMOD] ([DEMOD]) ([DEMOD])<br>

<b>KANAL:<br></b>
Vor den Kanal ein O fuer Oberband - ein U fuer Unterband. Es werden nur die technischen Kanaele 101-125 im 2m Band<br> beruecksichtigt! Kanal E fuer E*BOS<br>
<b>DEVICE:<br></b>
Das Device ist bei einem SDR-Stick immer 0. Bei mehr als einem Stick ist der Stick mit rtl_test zu ermitteln.<br>
<b>DEMOD:<br></b>
Es stehen 5 Demodulationsarten des multimon-ng zur Verarbeitung. <br>
FMSFSK (FMS BOS DE)<br>
POCSAG512 (Achtung, hier nur mit Anpassung des Script)<br>
POCSAG1200<br>
POCSAG2400 <br>
ZVEI2 (normales ZVEI BOS DE)<br>
Es können max. 3 gleichzeitig pro Stick und Frequenz genutzt werden<br>

<b>Bei Problemen bitte ein Issuse aufmachen! <br></b>
