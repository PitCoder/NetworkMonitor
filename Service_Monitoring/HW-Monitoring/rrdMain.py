#! /usr/bin/python3
from getSNMP import *
from rrdUpdate import *
from rrdCreateDatabase import *
import threading

def startEvalDirect(agent_ip, port, comunity_name, oid, mode):
	if mode == "1":
		#Se seleciono un SNMPGET a una oid en especifico, primero verificamos si se puede leer
		consulta = consultaSNMP(comunity_name, agent_ip, port, oid)

		if (consulta == "None" or consulta == ""):
			return "NO SUCH INSTANCE CURRENTLY EXISTS AT THIS OID - FAILURE"
		else:
			database_name = input("Inserte el nombre de la base de datos: ")

			if createDatabaseExam(database_name) == True:
				updateThread = threading.Thread(target = updateDirectGetDatabase, 
					name = "Update - Worker", 
					args = (database_name, comunity_name, agent_ip, port, oid))
				updateThread.start()

				return "SUCCESS"

			else:
				return "DATABASE CREATION - FAILURE"
			
	elif mode == "2":
		#Se seleciono un SNMPWALK a una oid en especifico, primero verificamos si se puede leer
		consulta = consultaWALKSNMP(comunity_name, agent_ip, port, oid)

		if (consulta == "None" or consulta == ""):
			return "NO SUCH INSTANCE CURRENTLY EXISTS AT THIS OID - FAILURE"

		else:
			database_name = input("Inserte el nombre de la base de datos: ")

			if createDatabase(database_name, len(consulta)) == True:
				updateThread = threading.Thread(target = updateDirectWalkDatabase, 
					name = "Update - Worker", 
					args = (database_name, comunity_name, agent_ip, port, oid))
				updateThread.start()

				return "SUCCESS"

			else:
				return "DATABASE CREATION - FAILURE"
	else:
		return "BAD MODE - FAILURE"

def startEvalPercentage(agent_ip, port, comunity_name, oid_top, oid_variable, mode):
	if mode == "1":
		#Se seleciono un SNMPGET a una oid en especifico, primero verificamos si se puede leer
		consulta1 = consultaSNMP(comunity_name, agent_ip, port, oid_top)
		consulta2 = consultaSNMP(comunity_name, agent_ip, port, oid_variable)

		if (consulta1 == "None" or consulta1 == "" or consulta2 == "None" or consulta2 == ""):
			return "NO SUCH INSTANCE CURRENTLY EXISTS AT THIS OID - FAILURE"
		else:
			database_name = input("Inserte el nombre de la base de datos: ")

			if createDatabase(database_name, 1) == True:
				updateThread = threading.Thread(target = updatePercentageGetDatabase, 
					name = "Update - Worker", 
					args = (database_name, comunity_name, agent_ip, port, oid_top, oid_variable))
				updateThread.start()

			return "READ SUCESS"

	elif mode == "2":
		#Se seleciono un SNMPWALK a una oid en especifico, primero verificamos si se puede leer
		consulta1 = consultaWALKSNMP(comunity_name, agent_ip, port, oid_top)
		consulta2 = consultaWALKSNMP(comunity_name, agent_ip, port, oid_variable)

		if (consulta1 == "None" or consulta1 == "" or consulta2 == "None" or consulta2 == "" or len(consulta1) != len(consulta2)):
			return "NO SUCH INSTANCE CURRENTLY EXISTS AT THIS OID - FAILURE"

		else:
			for i in range(len(consulta1)):
				valor = "N:" + str((consulta2[i]*100)/consulta1[i])
				print(valor)
			return "READ SUCESS"

	else:
		return "BAD MODE - FAILURE"

def startEvalIO(agent_ip, port, comunity_name, oid_input, oid_output, mode):
	if mode == "1":
		#Se seleciono un SNMPGET a una oid en especifico, primero verificamos si se puede leer
		consulta1 = consultaSNMP(comunity_name, agent_ip, port, oid_input)
		consulta2 = consultaSNMP(comunity_name, agent_ip, port, oid_output)

		if (consulta1 == "None" or consulta1 == "" or consulta2 == "None" or consulta2 == ""):
			return "NO SUCH INSTANCE CURRENTLY EXISTS AT THIS OID - FAILURE"
		else:
			variable_input =  int(consultaSNMP(comunity_name, agent_ip, port, oid_top))
			variable_output = int(consultaSNMP(comunity_name, agent_ip, port, oid_variable)) 
			valor = "N:" + str(variable_input) + ":" + str(variable_output)
			print(valor)
			return "READ SUCCESS"

	elif mode == "2":
		#Se seleciono un SNMPWALK a una oid en especifico, primero verificamos si se puede leer
		consulta1 = consultaWALKSNMP(comunity_name, agent_ip, port, oid_input)
		consulta2 = consultaWALKSNMP(comunity_name, agent_ip, port, oid_output)

		if (consulta1 == "None" or consulta1 == "" or consulta2 == "None" or consulta2 == "" or len(consulta1) != len(consulta2)):
			return "NO SUCH INSTANCE CURRENTLY EXISTS AT THIS OID - FAILURE"

		else:
			for i in range(len(consulta1)):
				valor = "N:" + str(consulta1[i] + ":" + consulta2[i])
				print(valor)
			return "READ SUCCESS"

	else:
		return "BAD MODE - FAILURE"


def main():
	agent_ip = input("Inserte la IP del Agente: ")
	port = int(input("Inserte el puerto: "))
	comunity_name = input("Inserte el nombre de la comunidad del agente: ")

	print("\nInserte el tipo de valor que desea obtener: \n 1) Directo \n 2) Porcentaje \n 3) I/O")
	type_val = input()

	if type_val == "1":
		oid = input("Inserte el OID de la variable que desea leer: ")
		print("\nInserte el modo en el cual se realizará la consulta SNMP: \n 1) GET \n 2) WALK")
		mode = input()
		print(startEvalDirect(agent_ip, port, comunity_name, oid, mode))

	elif type_val == "2":
		oid_top = input("Inserte el OID del valor tope que desea leer: ")
		oid_variable = input("Inserte el OID del valor variable que desea leer: ")
		print("\nInserte el modo en el cual se realizará la consulta SNMP: \n 1) GET \n 2) WALK")
		mode = input()
		print(startEvalPercentage(agent_ip, port, comunity_name, oid_top, oid_variable, mode))

	elif type_val == "3":
		oid_input = input("Inserte el OID de la variable de entrada que desea leer: ")
		oid_output = input("Inserte el OID de la variable de salida que desea leer: ")
		print("\nInserte el modo en el cual se realizará la consulta SNMP: \n 1) GET \n 2) WALK")
		mode = input()
		print(startEvalIO(agent_ip, port, comunity_name, oid_input, oid_output, mode))
	else:
		print("BAD TYPE - FAILURE")
	
if __name__ == "__main__":
	main()