#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
RASPOC - ein kleines python-Script für rtl_fm und multimon_ng 
getestes auf Raspberry Pi und Cubieboard

-- Pyton MySQL-Support installieren
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar && tar xfv mysql-connector.tar && cd mysql-connector-python* && chmod +x ./setup.py && sudo ./setup.py install

-- USAGE:
sudo ./multimon_rtl_mysql.py [KANAL] [DEVICENUMBER] [ERRORPPM] [DEMOD] ([DEMOD])([DEMOD])

-- INFOS
KANAL:
Vor den Kanal ein O fuer Oberband - ein U fuer Unterband. Es werden nur die technischen Kanaele 101-125 im 2m Band beruecksichtigt! Kanal E fuer E*BOS
DEVICE:
Das Device ist bei einem SDR-Stick immer 0. Bei mehr als einem Stick ist der Stick mit rtl_test zu ermitteln.
ERRORPPM
ist zu testen mit rtl_test. Als Zahl ohne weiteres. Meist 31.
DEMOD:
Es stehen 5 Demodulationsarten des multimon-ng zur Verarbeitung. 
FMSFSK (FMS BOS DE)
POCSAG512 (Achtung, hier nur mit Anpassung des Script)
POCSAG1200
POCSAG2400 
ZVEI2 (normales ZVEI BOS DE)
Es können max. 3 gleichzeitig pro Stick und Frequenz genutzt werden

Bei Problemen bitte ein Issuse aufmachen! 
'''
import time
import sys
import subprocess
import os
import mysql
import mysql.connector

########################################
##### Hier die Userdaten eintragen ##### 
########################################
dbserver = "localhost"
dbuser = ""
dbpassword = ""
datenbank = "raspoc"
TabellePOC = "ras_pocsag_hist"
TabelleFMS = "ras_fms_hist"
TabelleZVEI = "ras_zvei_hist"

########################################
##### Userdaten ENDE               ##### 
#########################################################################################################
### rtl_test aufrufen um Device zu identifizieren!
### Scriptaufruf Beispiel POCSAG 1200 Baud per Device 0: sudo ./multimon_rtl_mysql.py U106 0 31 POCSAG1200 
### Scriptaufruf Beispiel ZVEI & FMS: sudo ./multimon_rtl_mysql.py O444 1 31 FMSFSK ZVEI2
#########################################################################################################

# Kanal = ((Frequenz - 84,015 MHz) / 0,02 MHz) + 347 des Oberbandes 4m
# Vor den Kanal ein O fuer Oberband - ein U fuer Unterband. Es werden nur die technischen Kanaele 101-125 im 2m Band beruecksichtigt! Kanal E fuer E*BOS
kanal = sys.argv[1]
# DVB-T Stick Device ID, Testen mit "rtl_test"
deviceid = int(sys.argv[2])

# Fehlerkorrektur ppm DVB-T Stick
ppmerror = int(sys.argv[3])
# -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -a FMSFSK -a ZVEI2
if len(sys.argv) == 7:
    demod1 = "-a "+sys.argv[4]
    demod2 = "-a "+sys.argv[5]
    demod3 = "-a "+sys.argv[6]
elif len(sys.argv) == 6:
    demod1 = ("-a "+sys.argv[4])
    demod2 = "-a "+sys.argv[5]
    demod3 = ""
elif len(sys.argv) == 5:
    demod1 = ("-a "+sys.argv[4])
    demod2 = ""
    demod3 = ""
else:
    print "Zuviele Argumente! - max. 3 Demodulationen einstellbar!"

a_schleife_zvei = ""
a_address_fms = ""
a_status_fms = ""
a_richtung_fms = ""
a_zeit_zvei = int(time.time())
a_zeit_fms = int(time.time())
frequenz = "0"
if kanal[0:2] == "U1":
   frequenz = ((int(kanal[1:4]) - 101) * 0.02) + 165.210
elif kanal[0:2] == "O1":
   frequenz = ((int(kanal[1:4]) - 101) * 0.02) + 169.810
elif kanal[0:1] == "O":
   frequenz = ((int(kanal[1:4]) - 347) * 0.02) + 84.015
elif kanal[0:1] == "U":
   frequenz = ((int(kanal[1:4]) - 347) * 0.02) + 74.215
elif kanal[0:1] == "E":
   frequenz = "448.425"
else:
   frequenz = "1"

print "eingestellter Kanal: " + kanal[1:4] + " " + kanal[0] + "B"
print "Kanalfrequenz: " + str(frequenz) + " MHz"
print "Device Nr.: "+str(deviceid) + " SDR-Stick"
print "Error Korrektur: "+str(ppmerror) + " ppm"
print "Dekodierung von: "+demod1[3:13]+" "+demod2[3:13]+" "+demod3[3:13]

# ZVEI Filter Schleifen
zvei_filter = ['00000', '11111', '22222', '33333', '44444', '55555', '66666', '77777', '88888', '99999']
try:
    connection = mysql.connector.connect(host = str(dbserver), user = str(dbuser), passwd = str(dbpassword), db = str(datenbank))
except:
    print "Keine Verbindung zum Server"
    exit(0)
def curtime():
    return time.strftime("%Y-%m-%d %H:%M:%S")
with open('Fehler.txt','a') as file:
    file.write(('#' * 20) + '\n' + curtime() + '\n')
multimon_ng = subprocess.Popen("rtl_fm -d "+str(deviceid)+" -f "+str(frequenz)+"M -M fm -s 22050 -p "+str(ppmerror)+" -E DC -F 0 -g 100 | multimon-ng "+str(demod1)+" "+str(demod2)+" "+str(demod3)+" -f alpha -t raw -",
                               #stdin=rtl_fm.stdout,
                               stdout=subprocess.PIPE,
                               stderr=open('error.txt','a'),
                               shell=True)
try:
    while True:
        line = multimon_ng.stdout.readline()
        multimon_ng.poll()
        with open('Line.txt','a') as a:
            a.write(line)
         # ZVEI - Abfrage
        if line.startswith('ZVEI2'):
            address = line[7:12].replace(" ", "")
            address = address.replace("\n","")
            address = address.replace("\r","")
            if len(address) == 5:
                   ### Schleifen filtern 00000, 11111, ... ###	
                   if address == any(zvei_filter) :
                       print address + " - ZVEI ausgefiltert - nichts unternommen"
                 ### Schleifen filtern /ENDE ###         
                   else:
                        utc_stamp = int(time.time())
                        # Wiederholton 'F' auflösen
                        s1 = address[0]
                        s2 = address[1]
                        s3 = address[2]
                        s4 = address[3]
                        s5 = address[4]
                        if s2 == "F":
                            s2 = s1
                        if s3 == "F":
                            s3 = s2
                        if s4 == "F":
                            s4 = s3
                        if s5 == "F":
                            s5 = s4
                        address2 = s1 + s2 + s3 + s4 + s5
                        # Pruefen ob Schleife numerisch ist
                        if address2.isdigit() is True:
                            # Pruefen auf Doppelalarmierung
                            if address2 == a_schleife_zvei and utc_stamp < a_zeit_zvei + 10:
                                print address2 + " - ZVEI Doppelalarmierung - nichts unternommen"
                            else:
                                output=(curtime()+' '+ address2+'\n')
                                print curtime(), address2
                                with open('ZVEI.txt','a') as f:                                           
                                            f.write(output)
                                cursor = connection.cursor()
                                cursor.execute("INSERT INTO "+str(TabelleZVEI)+" (time,schleife,kanal) VALUES (%s,%s,%s)",(curtime(),address2,kanal,))
                                cursor.close()
                                connection.commit()
                        else:
                            print address + " - ZVEI nicht numerisch - nichts unternommen"
                        a_zeit_zvei = utc_stamp
                        a_schleife_zvei = address2
            else:
                print address + " - ZVEI nicht vollstaendig - nichts unternommen"
                
        # FMS - Abfrage
        elif line.startswith('FMS'):
            utc_stamp = int(time.time())		
            bos = line[19]
            land = line[36]
            kreis= line[65:67]
            fhzg = line[72:76]
            status = line[84]
            status = status.replace("\n","")
            status = status.replace("\r","")
            richtung = line[101]
            richtung = richtung.replace("\n","")
            richtung = richtung.replace("\r","")
            address = (bos+''+ land+''+ kreis+''+ fhzg)
            # Pruefen auf Doppelstatus
            if address == a_address_fms and status == a_status_fms and richtung == a_richtung_fms and utc_stamp < a_zeit_fms + 3:
                print address + ", Status: " + status + ", Richtung: " + richtung + " - FMS Doppelstatus - nichts unternommen"
            else:
                output= (curtime()+' '+ bos+''+ land+''+ kreis+''+ fhzg+' '+status+' '+richtung+'\n')
                # Pruefen ob FMS Telegram vollstaendig ist	
                if address != "" and status != "" and richtung != "":
                    # Nur Fahrzeug --> Leitstelle (0) in DB schreiben
                    if richtung == "0":
                        print curtime(), address, status, richtung
                        with open('FMS.txt','a') as f:                                           
                           f.write(output)
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO "+str(TabelleFMS)+" (timestamp,kennung,status,richtung,kanal) VALUES (%s,%s,%s,%s,%s)",(curtime(),address,status,richtung,kanal,))
                        cursor.close()
                        connection.commit()
                    else:
                        print address + ", Status: " + status + ", Richtung: " + richtung + " - FMS falsche Richtung - nichts unternommen"	
                else:
                    print address + ", Status: " + status + ", Richtung: " + richtung + " - FMS nicht vollstaendig - nichts unternommen"
            a_zeit_fms = utc_stamp
            a_address_fms = address
            a_status_fms = status
            a_richtung_fms = richtung	
        # POCSAG - Abfrage
        elif line.__contains__("Alpha:"):
            if line.startswith('POCSAG'):
                utc_stamp = int(time.time())	
                address = line[21:28].replace(" ", "").zfill(7)	                        
                subric = line[40:41].replace(" ", "").replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
                message = line.split('Alpha:   ')[1].strip().rstrip('<EOT>').strip()    
                output=(curtime()+' '+ address+' '+ subric+' '+ message+'\n')
                print curtime(), address, subric, message                               
                with open('POCSAG.txt','a') as f:
                    f.write(output)
                #Datensatz einfuegen
                cursor = connection.cursor()
                cursor.execute("INSERT INTO "+str(TabellePOC)+" (time,ric,funktion,text) VALUES (%s,%s,%s,%s)",(curtime(),address,subric,message,))
                cursor.close()
                connection.commit()
            if not "Alpha:" in line:                                                    
                with open("POCSAG.txt","a") as missed:
                    address = line[21:28].replace(" ", "").zfill(7)
                    subric = line[40:41].replace(" ", "").replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
                    print  curtime(), address, subric
                    missed.write(line)
                    #Datensatz einfuegen
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO "+str(TabellePOC)+" (time,ric,funktion,text) VALUES (%s,%s,%s,%s)",(curtime(),address,subric,'',))
                    cursor.close()
                    connection.commit()
except KeyboardInterrupt:
    os.kill(multimon_ng.pid, 9)
