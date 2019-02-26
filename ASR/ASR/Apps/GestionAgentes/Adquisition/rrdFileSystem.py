#!bin/bash/python3

import time
import rrdtool
from .getSNMP import *

#Esta funcion hace la conversión de bytes a su escala más conveniente
def sizeof_fmt(num, suffix='B'):
	for unit in ['','K','M','G','T','P','E','Z']:
		if abs(num) < 1024.0:
			return "%3.2f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Y', suffix)

#Primero obtenemos todas los index de los dispositivos, para poder realizar la consulta a la tabla
def rrdFileSystem(comunityName, agentIP):
	device = []
	resultado = []

	index_devices = []
	index_devices = consultaWALKSNMP(comunityName,agentIP,'1.3.6.1.2.1.25.2.3.1.1')

	for index_device in index_devices:
		#Descripción del dispositivo de almacenamiento
		oid = '1.3.6.1.2.1.25.2.3.1.3.' + index_device
		device_description = str(consultaSTRINGSNMP(comunityName, agentIP, oid))
		device.append(device_description)

		#Capacidad de almacenamiento del dispositivo en bloques
		oid = '1.3.6.1.2.1.25.2.3.1.5.' + index_device
		device_capacity = int(consultaINTSNMP(comunityName, agentIP, oid))

		#Uso de almacenamiento del dispositivo en bloques
		oid = '1.3.6.1.2.1.25.2.3.1.6.' + index_device
		device_usage = int(consultaINTSNMP(comunityName, agentIP, oid))

		#Tamaño del bloque
		oid = '1.3.6.1.2.1.25.2.3.1.4.' + index_device
		device_blockSize = int(consultaINTSNMP(comunityName, agentIP, oid))
	
		#Conversiones
		#Conviertiendo todo a bytes
		device.append(sizeof_fmt(device_capacity * device_blockSize))
		device.append(sizeof_fmt(device_usage * device_blockSize))	

		resultado.append(device)
		device =[]
	return resultado
