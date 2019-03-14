import time
import rrdtool

fname="netPred.rrd"
pngfname="predict.png"
title="Deteccion de comportamiento anomalo, valor de Alpha 0.1"
endDate = rrdtool.last(fname)
begDate = endDate - 86000

rrdtool.tune(fname,'--alpha','0.1')
ret = rrdtool.graph("netPalphaBajoFallas.png",
                        '--start', str(begDate), '--end', str(endDate), '--title=' + title,
                        "--vertical-label=Bytes/s",	
                        '--slope-mode',
                        "DEF:obs="       + fname + ":inoctets:AVERAGE",
                        "DEF:outoctets=" + fname + ":outoctets:AVERAGE",
                        "DEF:pred="      + fname + ":inoctets:HWPREDICT",
                        "DEF:dev="       + fname + ":inoctets:DEVPREDICT",
                        "DEF:fail="      + fname + ":inoctets:FAILURES",
                        "CDEF:scaledobs=obs,8,*",
                        "CDEF:upper=pred,dev,2,*,+",
                        "CDEF:lower=pred,dev,2,*,-",
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",
                        "TICK:fail#FDD017:1.0:Fallas",
                        "LINE3:scaledobs#00FF00:In traffic",
                        "LINE1:scaledpred#FF00FF:Prediccion\\n",
                        "LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
                        "LINE1:scaledlower#0000FF:Lower Bound Average bits in")
