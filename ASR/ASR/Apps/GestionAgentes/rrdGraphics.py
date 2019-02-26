import sys
import rrdtool
import time
import os
FILE_DIR = os.path.realpath(os.path.dirname(__file__))
rel_to_abs = lambda *x: os.path.join(FILE_DIR, *x)

tiempo_actual = int(time.time())

GRAPHICS_PATH = "/home/ESCOM/Documents/NetworkMonitorv2ASR/ASR/Apps/GestionAgentes/static/graphs/"
DATABASE_PATH = "/home/ESCOM/Documents/NetworkMonitorv2/ASR/ASR/Apps/GestionAgentes/Adquisition/rrDatabases/"
XML_PATH = "/home/ESCOM/Documents/NetworkMonitorv2/ASR/ASR/Apps/GestionAgentes/Adquisition/xmls/"

def Graph(host): #Recibimos el Host del agente para abrir cada archivo de la MIB
    while 1:
        '''
        ret = rrdtool.graph("/static/graphs/"+host+"_traffic.png",  #Regresamos una carpeta y guardamos en static  ***Hay que checar, sino sacamos este archivo para que quede dentro de GestionAgentes
        "--start", str(tiempo_actual),
        "--end","N",
        "--vertical-label=Bytes/s",
        "DEF:inoctets="+rel_to_abs("'rrDatabases"+host+"_traffic.rrd'")+":inoctets:AVERAGE",  ##Checar esta parte
        "DEF:outoctets="+rel_to_abs("'rrDatabases/"+host+"_traffic.rrd'")+":outoctets:AVERAGE", ##Checar esta parte
        "AREA:inoctets#7293CB:In traffic",
        "AREA:outoctets#E1974C:Out traffic")

        ret = rrdtool.graph( "/static/graphs/"+host+"_tcpTraffic.png",
        "--start", str(tiempo_actual),
        "--end","N",
        "--vertical-label=Bytes/s",
        "DEF:inoctets="+rel_to_abs("'rrDatabases/"+host+"_tcpTraffic.rrd'")+":inoctets:AVERAGE",
        "DEF:outoctets="+rel_to_abs("'rrDatabases/"+host+"_tcpTraffic.rrd'")+":outoctets:AVERAGE",
        "AREA:inoctets#7293CB:In traffic",
        "AREA:outoctets#E1974C:Out traffic")
        time.sleep(30)

        ret = rrdtool.graph( "/static/graphs/"+host+"_udpTraffic.png",
        "--start", str(tiempo_actual),
        "--end","N",
        "--vertical-label=Bytes/s",
        "DEF:inoctets="+rel_to_abs("'rrDatabases/"+host+"_udpTraffic.rrd'")+":inoctets:AVERAGE",
        "DEF:outoctets="+rel_to_abs("'rrDatabases/"+host+"_udpTraffic.rrd'")+":outoctets:AVERAGE",
        "AREA:inoctets#7293CB:In traffic",
        "AREA:outoctets#E1974C:Out traffic")
        time.sleep(30)
        
        '''
        time.sleep(10)

        #ret = rrdtool.graph( "/static/graphs/"+host+"_pingTraffic.png",
        ret = rrdtool.graph(GRAPHICS_PATH + host + '_pingTraffic.png',
        "--start", str(tiempo_actual),
        "--end","N",
        "--vertical-label=Packets/s",
        "DEF:inpackets="+ DATABASE_PATH + host +'_pingTraffic.rrd' + ":inpackets:AVERAGE",
        "DEF:outpackets="+ DATABASE_PATH + host +'_pingTraffic.rrd' + ":outpackets:AVERAGE",
        "AREA:inpackets#7293CB:Input ping packets",
        "AREA:outpackets#E1974C:Output ping packets")

        #ret = rrdtool.graph( "/static/graphs/"+host+"_icmpTraffic.png",
        ret = rrdtool.graph(GRAPHICS_PATH + host + '_icmpTraffic.png',
        "--start", str(tiempo_actual),
        "--end","N",
        "--vertical-label=Packets/s",
        "DEF:inpackets="+ DATABASE_PATH + host + '_icmpTraffic.rrd' + ":inpackets:AVERAGE",
        "DEF:outpackets="+ DATABASE_PATH + host +'_icmpTraffic.rrd' + ":outpackets:AVERAGE",
        "AREA:inpackets#7293CB:Input ICMP packets",
        "AREA:outpackets#E1974C:Output ICMP packets")
    
