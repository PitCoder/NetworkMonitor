#!bin/bash/python3

import time
import rrdtool
from .getSNMP import *

#This script will read all TCP packets from input/output
def rrdICMPSegments(comunityName, agentIP):
	icmpTraffic = []
	oid = ""
	total_input_icmp = 0
	total_output_icmp = 0

	#Ping de entrada
	oid = str('1.3.6.1.2.1.5.1.0')
	#print(oid)
	total_input_icmp  = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	print("ICMP entrada:" + str(total_input_icmp))
	icmpTraffic.append(total_input_icmp)

	#Ping salida
	oid = '1.3.6.1.2.1.5.14.0'
	#print(oid)
	total_output_icmp  = int(
	consultaINTSNMP(comunityName, agentIP, oid))
	print("ICMP salida:" + str(total_output_icmp))
	icmpTraffic.append(total_output_icmp)

	return icmpTraffic
