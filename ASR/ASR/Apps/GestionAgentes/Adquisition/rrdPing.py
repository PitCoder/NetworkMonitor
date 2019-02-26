#!bin/bash/python3

import time
import rrdtool
from .getSNMP import *

#This script will read all TCP packets from input/output
def rrdPing(comunityName, agentIP):
	pingTraffic = []
	oid = ""
	total_input_ping = 0
	total_output_ping = 0

	#Ping de entrada
	oid = str('1.3.6.1.2.1.5.9.0')
	#print(oid)
	total_input_ping  = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	print("Ping entrada:" + str(total_input_ping))
	pingTraffic.append(total_input_ping)

	#Ping salida
	oid = '1.3.6.1.2.1.5.20.0'
	#print(oid)
	total_output_ping  = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	print("Ping salida:" + str(total_output_ping))
	pingTraffic.append(total_output_ping)

	return pingTraffic
