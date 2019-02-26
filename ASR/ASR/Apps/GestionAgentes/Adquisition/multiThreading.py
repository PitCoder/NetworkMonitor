#!bin/bash/python3

import threading
import logging
import time
import json
import rrdtool
from .rrdTraffic import *
from .rrdPing import *
from .rrdICMPSegments import *
from .rrdTCPSegments import *
from .rrdUDPDatagrams import *
from ASR.Apps.GestionAgentes.rrdGraphics import *

import os
FILE_DIR = os.path.realpath(os.path.dirname(__file__))
rel_to_abs = lambda *x: os.path.join(FILE_DIR, *x)

logging.basicConfig( level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')

#===========================================================

def trafficReader(comunidad, host):
    logging.debug('Lanzado')

    # Primero obtenemos cuantos dispositivos y cuales tenemos
    interfacesFounded = getIterfaces(comunidad, host)
    numInterfaces = len(interfacesFounded)
    logging.debug(numInterfaces)

    # Creación de las base de datos Round Robin para el lector de tráfico por interfaz
    for interfaceFound in interfacesFounded:
        ret = rrdtool.create(rel_to_abs("rrDatabases/"+host+"_traffic_" + str(interfaceFound) + ".rrd"),  #Tengo duda si pasamos el Id
                             "--start", "N",
                             "--step", "10",
                             "DS:inoctets:COUNTER:60:U:U",
                             "DS:outoctets:COUNTER:60:U:U",
                             "RRA:AVERAGE:0.5:1:10",
                             "RRA:AVERAGE:0.5:6:10")

        if ret:
            logging.debug(rrdtool.error())

    while 1:
        logging.debug('Ejecutando')
        resultados = rrdTraffic(comunidad, host, numInterfaces)
        print(resultados)

        counter = 1
        for resultado in resultados:
            valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
            logging.debug(valor)
            rrdtool.update(rel_to_abs('rrDatabases/'+host+'_traffic_' + str(counter) + '.rrd'), valor)
            rrdtool.dump(rel_to_abs('rrDatabases/'+host+'_traffic_' + str(counter) + '.rrd'),
                         rel_to_abs('xmls/'+host+'_traffic' + str(counter) + '.xml'))
            counter = counter + 1
        logging.debug('Deteniendo')
#===========================================================

def pingReader(comunidad, host):
    logging.debug('Lanzado')
    ret = rrdtool.create(rel_to_abs('rrDatabases/'+host+'_pingTraffic.rrd'),
    "--start","N",
	"--step","10", 
    "DS:inoctets:COUNTER:60:U:U",
    "DS:outoctets:COUNTER:60:U:U",
    "RRA:AVERAGE:0.5:1:10",
    "RRA:AVERAGE:0.5:6:10")

    while 1:
        logging.debug('Ejecutando')
        resultado = rrdPing(comunidad,host)
        valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
        logging.debug(valor)
        rrdtool.update(rel_to_abs('rrDatabases/'+host+'_pingTraffic.rrd', valor))
        rrdtool.dump(rel_to_abs('rrDatabases/'+host+'_pingTraffic.rrd'), rel_to_abs('xmls/'+host+'_pingTraffic.xml'))
        logging.debug('Ciclo Terminado')

#===========================================================

def icmpSegmentsReader(comunidad, host):
    logging.debug('Lanzado')
    ret = rrdtool.create(rel_to_abs('rrDatabases/'+host+'_icmpTraffic.rrd'),
    "--start","N",
	"--step","10", 
    "DS:inoctets:COUNTER:60:U:U",
    "DS:outoctets:COUNTER:60:U:U",
    "RRA:AVERAGE:0.5:1:10",
    "RRA:AVERAGE:0.5:6:10")

    while 1:
        logging.debug('Ejecutando')
        resultado = rrdICMPSegments(comunidad,host)
        valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
        logging.debug(valor)
        rrdtool.update(rel_to_abs('rrDatabases/'+host+'_icmpTraffic.rrd', valor))
        rrdtool.dump(rel_to_abs('rrDatabases/'+host+'_icmpTraffic.rrd'), rel_to_abs('xmls/'+host+'_icmpTraffic.xml'))
        logging.debug('Ciclo Terminado')

#===========================================================

def tcpSegmentsReader(comunidad, host):
    logging.debug('Lanzado')
    ret = rrdtool.create(rel_to_abs('rrDatabases/'+host+'_tcpTraffic.rrd'),
    "--start","N",
	"--step","10", 
    "DS:inoctets:COUNTER:60:U:U",
    "DS:outoctets:COUNTER:60:U:U",
    "RRA:AVERAGE:0.5:1:10",
    "RRA:AVERAGE:0.5:6:10")

    while 1:
        logging.debug('Ejecutando')
        resultado = rrdTCPSegments(comunidad,host)
        valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
        logging.debug(valor)
        rrdtool.update(rel_to_abs('rrDatabases/'+host+'_tcpTraffic.rrd'), valor)
        rrdtool.dump(rel_to_abs('rrDatabases/'+host+'_tcpTraffic.rrd'), rel_to_abs('xmls/'+host+'_tcpTraffic.xml'))
        logging.debug('Ciclo Terminado')

#===========================================================

def updDatagramsReader(comunidad, host):
    logging.debug('Lanzado')
    ret = rrdtool.create(rel_to_abs('rrDatabases/'+host+'_udpTraffic.rrd'),
    "--start","N",
	"--step","10", 
    "DS:inoctets:COUNTER:60:U:U",
    "DS:outoctets:COUNTER:60:U:U",
    "RRA:AVERAGE:0.5:1:10",
    "RRA:AVERAGE:0.5:6:10")

    while 1:
        logging.debug('Ejecutando')
        resultado = rrdUDPDatagrams(comunidad,host)
        valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
        logging.debug(valor)
        rrdtool.update(rel_to_abs('rrDatabases/'+host+'_udpTraffic.rrd'), valor)
        rrdtool.dump(rel_to_abs('rrDatabases/'+host+'_udpTraffic.rrd'), rel_to_abs('xmls/'+host+'_udpTraffic.xml'))
        logging.debug('Ciclo Terminado')

#===========================================================

def multi(comunidad, host):
    thread1 = threading.Thread(target=trafficReader, name='Traffic Reader', args=[comunidad, host])

    thread2 = threading.Thread(target=pingReader, name='Ping Reader', args=[comunidad, host])

    thread3 = threading.Thread(target=icmpSegmentsReader, name='ICMP Segments Reader', args=[comunidad, host])

    thread4 = threading.Thread(target=tcpSegmentsReader, name='TCP Segments Reader', args=[comunidad, host])

    thread5 = threading.Thread(target=updDatagramsReader, name='UDP Datagrams Reader', args=[comunidad, host])

    thread6 = threading.Thread(target=Graph, name='Graphics', args=host)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()