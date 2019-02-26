#!bin/bash/python3

import time
import rrdtool
from .getSNMP import *

#This script will read all UDP packets from input/output
def rrdUDPDatagrams(comunityName, agentIP):
	total_input_datagrams = 0
	total_output_datagrams = 0
	datagramsTraffic = []
	
	#Segmentos de datagramas UDP de entrada
	oid = '1.3.6.1.2.1.7.1.0'	
	total_input_traffic = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	datagramsTraffic.append(total_input_datagrams)
	
	#Segmentos de datagramas UDP de salida
	oid = '1.3.6.1.2.1.7.4.0'
	total_output_segments = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	datagramsTraffic.append(total_output_datagrams)

	return datagramsTraffic
