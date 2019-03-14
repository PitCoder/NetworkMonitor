import sys
import rrdtool
import time

num_cores = 4

color_hex = ["#CEDF6C","#99BDE4","#FFA0C4","#FCEF6D"]
propiedades = []
propiedadesLineaBase = []
propiedadesMinimosCuadrados = []

propiedades.append("--start")
propiedades.append("1539106151")
propiedades.append("--vertical-label=Carga CPU")
propiedades.append("--title=Uso de CPU")
propiedades.append("--color")
propiedades.append("ARROW#009900")
propiedades.append("--vertical-label")
propiedades.append("Uso de CPU (%)")
propiedades.append("--lower-limit")
propiedades.append("0")
propiedades.append("--upper-limit")
propiedades.append("100")

while 1:
    for i in range(num_cores):
        ret = rrdtool.graph( "trend" + str(i + 1) + ".png",
            propiedades,
            "DEF:carga" + str(i + 1) + "=trend.rrd:CPU" + str(i + 1) + "load:AVERAGE",
            "AREA:carga" + str(i + 1) + color_hex[i] + ":CPU " + str(i + 1) + " Load",
            "LINE1:30",
            "AREA:5#ff000022:stack",
            "VDEF:CPUlast=carga" + str(i + 1) + ",LAST",
            "VDEF:CPUmin=carga" + str(i + 1) + ",MINIMUM",
            "VDEF:CPUavg=carga" + str(i + 1) + ",AVERAGE",
            "VDEF:CPUmax=carga" + str(i + 1) + ",MAXIMUM",
            "COMMENT:                         Now          Min             Avg             Max//n",
            "GPRINT:CPUlast:%12.0lf%s",
            "GPRINT:CPUmin:%10.0lf%s",
            "GPRINT:CPUavg:%13.0lf%s",
            "GPRINT:CPUmax:%13.0lf%s",
            "VDEF:a=carga" + str(i + 1) + ",LSLSLOPE",
            "VDEF:b=carga" + str(i + 1) + ",LSLINT",
            "CDEF:avg2=carga" + str(i + 1) + ",POP,a,COUNT,*,b,+",
            "LINE2:avg2#FFBB00:Mínimos Cuadrados"

        )
    time.sleep(5)