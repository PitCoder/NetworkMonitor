from ASR.celery import app  #importamos nuestra aplicación de Celery

import logging
import time
import json
import rrdtool

from ASR.Apps.GestionAgentes.Adquisition.rrdICMPSegments import *
from ASR.Apps.GestionAgentes.Adquisition.rrdPing import *
from ASR.Apps.GestionAgentes.Adquisition.rrdTraffic import *
from ASR.Apps.GestionAgentes.Adquisition.rrdUDPDatagrams import *
from ASR.Apps.GestionAgentes.Adquisition.rrdTCPSegments import *

from ASR.Apps.GestionAgentes.rrdGraphics import *

DATABASE_PATH = "/home/ESCOM/Documents/NetworkMonitorv2/ASR/ASR/Apps/GestionAgentes/Adquisition/rrDatabases/"
XML_PATH = "/home/ESCOM/Documents/NetworkMonitorv2/ASR/ASR/Apps/GestionAgentes/Adquisition/xmls/"

import os
FILE_DIR = os.path.realpath(os.path.dirname(__file__))
rel_to_abs = lambda *x: os.path.join(FILE_DIR, *x)

logging.basicConfig( level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')

#===========================================================
@app.task #Con esta notación le indicamos a la aplicación de Celery que es parte de la aplicación
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
@app.task #Con esta notación le indicamos a la aplicación de Celery que es parte de la aplicación
def pingReader(comunidad, host):
    logging.debug('Lanzado')
    #ret = rrdtool.create(rel_to_abs('rrDatabases/'+host+'_pingTraffic.rrd'),
    ret = rrdtool.create(DATABASE_PATH + host + '_pingTraffic.rrd',
    "--start","N",
	"--step","10",
    "DS:inpackets:COUNTER:60:U:U",
    "DS:outpackets:COUNTER:60:U:U",
    "RRA:AVERAGE:0.5:1:10",
    "RRA:AVERAGE:0.5:6:10")

    while 1:
        logging.debug('Ejecutando')
        resultado = rrdPing(comunidad,host)
        valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
        logging.debug(valor)
        rrdtool.update(DATABASE_PATH + host + '_pingTraffic.rrd', valor)
        rrdtool.dump(DATABASE_PATH + host + '_pingTraffic.rrd', XML_PATH + host + '_pingTraffic.xml')
        logging.debug('Ciclo Terminado')


#===========================================================
@app.task #Con esta notación le indicamos a la aplicación de Celery que es parte de la aplicación
def icmpSegmentsReader(comunidad, host):
    logging.debug('Lanzado')
    #ret = rrdtool.create(rel_to_abs('rrDatabases/'+host+'_icmpTraffic.rrd'),
    ret = rrdtool.create(DATABASE_PATH + host + '_icmpTraffic.rrd',
    "--start","N",
	"--step","10",
    "DS:inpackets:COUNTER:60:U:U",
    "DS:outpackets:COUNTER:60:U:U",
    "RRA:AVERAGE:0.5:1:10",
    "RRA:AVERAGE:0.5:6:10")

    while 1:
        logging.debug('Ejecutando')
        resultado = rrdICMPSegments(comunidad,host)
        valor = "N:" + str(resultado[0]) + ':' + str(resultado[1])
        logging.debug(valor)
        rrdtool.update(DATABASE_PATH + host + '_icmpTraffic.rrd', valor)
        rrdtool.dump(DATABASE_PATH + host + '_icmpTraffic.rrd', XML_PATH + host + '_icmpTraffic.xml')
        logging.debug('Ciclo Terminado')


#===========================================================
@app.task #Con esta notación le indicamos a la aplicación de Celery que es parte de la aplicación
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
@app.task #Con esta notación le indicamos a la aplicación de Celery que es parte de la aplicación
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


#============================================================
@app.task
def graph(host):
    Graph(host)

