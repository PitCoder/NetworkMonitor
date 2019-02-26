#!bin/bash/python3

import time
import rrdtool
from .getSNMP import *

#This script will read all TCP packets from input/output
def rrdTCPSegments(comunityName, agentIP):
	total_input_segments = 0
	total_output_segments = 0
	segmentTraffic = []

	#Segmentos de paquetes TCP de entrada
	oid = '1.3.6.1.2.1.6.10.0'
	total_input_traffic = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	segmentTraffic.append(total_input_segments)
	
	#Segmentos de paquetes TCP de salida
	oid = '1.3.6.1.2.1.6.11.0'
	total_output_segments = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	segmentTraffic.append(total_output_segments)

	return segmentTraffic
