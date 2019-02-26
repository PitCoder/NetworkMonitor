#! /bin/bash/python3

import subprocess

cmd = 'snmpwalk -v 2c -c comunidadAmistades localhost 1.3.6.1.2.1.25.2.3'

process	= subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)

output = process.communicate()[0]

varBinds = output.decode('utf-8').split('\n')

resultado = []

for varBind in varBinds:
	zipvarB = varBind.split(' ')
	print(zipvarB)
	resultado.append(' '.join(zipvarB[3::]))
		
resultado.remove('')
print(resultado)
