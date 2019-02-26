#!bin/bash/python3

import time
import rrdtool
from .getSNMP import *


def getIterfaces(comunityName, agentIP):
    interfaces_state = []
    active_interfaces = []

    interfaces_state = consultaWALKSNMP(comunityName, agentIP, '1.3.6.1.2.1.2.2.1.8')

    for interface_state in interfaces_state:
        interface_data = interface_state.split()

        if interface_data[2] == '1':
            active_interfaces.append(int(interface_data[0].split('.')[-1]))

    return active_interfaces


# This script will read all the network interfaces and print their names
def rrdTraffic(comunityName, agentIP, numInterfaces):
    interfaces_counter = 0
    total_input_traffic = 0
    total_output_traffic = 0

    interface_description = ''
    interface = []
    resultado = []

    while (interfaces_counter < numInterfaces):
        # Tráfico de entrada en la interfaz (bytes)
        oid = '1.3.6.1.2.1.2.2.1.10.' + str(interfaces_counter + 1)
        total_input_traffic = int(
            consultaINTSNMP(comunityName, agentIP, oid))
        interface.append(total_input_traffic)

        # Tráfico de salida en la interfaz (bytes)
        oid = '1.3.6.1.2.1.2.2.1.16.' + str(interfaces_counter + 1)
        total_output_traffic = int(
            consultaINTSNMP(comunityName, agentIP, oid))
        interface.append(total_output_traffic)

        interfaces_counter = interfaces_counter + 1
        resultado.append(interface)
        interface = []
    return resultado
