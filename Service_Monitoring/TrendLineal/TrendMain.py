import time
import rrdtool
from getSNMP import *

carga_CPU = []
core_num = 0

carga_CPU = consultaWALKSNMP('comunidadSNMP','localhost','1.3.6.1.2.1.25.3.3.1.2')
core_num = len(carga_CPU)
print (core_num)

datasources = []
rraverages = []

for i in range(core_num):
    data_string = "DS:CPU" + str(i+1) + "load:GAUGE:600:U:U"
    datasources.append(data_string)
    rraverages.append("RRA:AVERAGE:0.5:1:24")

print ("datasources -> " + str(datasources))
print ("rraverages -> " + str(rraverages))

ret = rrdtool.create("trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     datasources,
                     rraverages)
if ret:
    print (rrdtool.error())

while 1:
    #Lectura SNMP
    carga_CPU = consultaWALKSNMP('comunidadSNMP','localhost','1.3.6.1.2.1.25.3.3.1.2')

    valor = "N" 
    for val_CPU in carga_CPU:
        valor = valor + ":" + str(val_CPU)

    print (valor)
    rrdtool.update('trend.rrd', valor)
    rrdtool.dump('trend.rrd','trend.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)
