#!bin/bash/python3

#This script will read all the IP estatistics of the agent

import time
import rrdtool
from .getSNMP import *

class Switcher(object):
	def numbers_to_connections(self, arg):
		'Dispatch method'
		method_name = 'state_' + str(arg)
		# Get the method from 'self'. Deafult to lambda
		method =  getattr(self, method_name, lambda: 'Valor Inválido')
		# Call the method as we return it
		return method()

	def state_1(self):
		return 'cerrado'

	def state_2(self):
		return 'escuchando'

	def state_3(self):
		return 'sync enviado'

	def state_4(self):
		return 'sync recibido'

	def state_5(self):
		return 'estableciendo'

	def state_6(self):
		return 'fin espera 1'

	def state_7(self):
		return 'fin espera 2'

	def state_8(self):
		return 'esperando a cerrar'

	def state_9(self):
		return 'reconociendo'

	def state_10(self):
		return 'cerrando'

	def state_11(self):
		return 'tiempo de espera'

	def state_12(self):
		return 'borrando TCB'


#Primero obtenemos todas las direcciones IP de los conexiones TCP y las filtramos
def rrdTCPConnections(comunityName, agentIP):
	connections_counter = 0
	total_number_connections = 0
	state_tcp_connection = 0
	local_ipAddress = ""
	local_port = -1
	remote_ipAddress = ""
	remote_port = -1

	#Listas de variables
	tcp_connections = []
	tcp_states = []
	connections = []
	connection = []

	#Conexión TCP local
	tcp_connections = set(consultaWALKSNMP(comunityName, agentIP, '1.3.6.1.2.1.6.13.1.2'))

	for tcp_connection in tcp_connections:
		#Estado de la conexión TCP
		oid = '1.3.6.1.2.1.6.13.1.1.' + tcp_connection
		connection.append(tcp_connection)
		
		tcp_states = []
		resultados = consultaWALKSNMP(comunityName, agentIP, oid)
		s = Switcher()

		for resultado in resultados:
			numres = int(resultado)
			tcp_states.append(s.numbers_to_connections(numres))
		connection.append(tcp_states)

		#Puerto Local
		oid = '1.3.6.1.2.1.6.13.1.3.' + tcp_connection
		puertos_locales = consultaWALKSNMP(comunityName, agentIP, oid) 
		connection.append(puertos_locales)

		#Dirección IP Remota
		oid = '1.3.6.1.2.1.6.13.1.4.' + tcp_connection
		ips_remotas = consultaWALKSNMP(comunityName, agentIP, oid) 
		connection.append(ips_remotas)

		#Puerto Remoto
		oid = '1.3.6.1.2.1.6.13.1.5.' + tcp_connection
		puertos_remotos = consultaWALKSNMP(comunityName, agentIP, oid) 
		connection.append(puertos_remotos)

		connections.append(connection)
		connection = []
	return connections
