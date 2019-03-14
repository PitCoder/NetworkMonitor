import sys
import rrdtool
import time

def graph(num_sources, init_time, database_name):
    num_cores = 4

    color_hex = ["#CEDF6C","#99BDE4","#FFA0C4","#FCEF6D"]
    propiedades = []
    propiedadesLineaBase = []
    propiedadesMinimosCuadrados = []

    propiedades.append("--start")
    propiedades.append(str(init_time - 100))
    propiedades.append("--end")
    propiedades.append(str(rrdtool.last(database_name + ".rrd") + 300))
    propiedades.append("--vertical-label=%Uso")

                        "DEF:obs=netPred.rrd:inoctets:AVERAGE",
                        "DEF:pred=netPred.rrd:inoctets:HWPREDICT",
                        "DEF:dev=netPred.rrd:inoctets:DEVPREDICT",
                        "DEF:fail=netPred.rrd:inoctets:FAILURES",
                        "CDEF:scaledobs=obs,8,*",
                        "CDEF:upper=pred,dev,2,*,+",
                        "CDEF:lower=pred,dev,2,*,-",
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "TICK:fail#FDD017:1.0:Fallas",
                        
                        "LINE1:scaledobs#00FF00:Values",


                        "CDEF:scaledpred=pred,8,*",                   
                        "LINE2:scaledpred#ee0099:Prediction",
            "LINE1:scaledupper#FF000E:Upper",
            "LINE1:scaledlower#0012FF:Lower")

    time.sleep(1)

    while 1:
        for i in range(num_sources):
            ret = rrdtool.graph( "IMG/" + database_name + str(i + 1) + ".png",
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
