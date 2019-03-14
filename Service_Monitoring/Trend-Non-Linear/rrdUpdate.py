import time
import logging
import rrdtool

from getSNMP import *
from notification import *

logging.basicConfig( level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')

counterfail = 0
now = 0
activated = 0
future = now + 10

def graph(database_name, num_graphs, labels_name, init_time):
    for i in range(num_graphs):
        ret = rrdtool.graph("IMG/" + database_name + ".png",
        						"--title=ABERRANT BEHAVIOUR FOR " + labels_name[1].upper() + " " + str(i+1),
                                "--start", str(init_time),
                                "--end", str(rrdtool.last("RRD/" + database_name + '.rrd')),
                                "--vertical-label=" + labels_name[0],
                                "--width=1000",
                                "--height=500",
                                "DEF:obs=" + "RRD/" + database_name + ".rrd:VALUES" + str(i+1) + ":AVERAGE",
                                "DEF:pred=" + "RRD/" + database_name + ".rrd:VALUES" + str(i+1) + ":HWPREDICT",
                                "DEF:dev=" + "RRD/" + database_name + ".rrd:VALUES" + str(i+1) + ":DEVPREDICT",
                                "DEF:fail=" + "RRD/" + database_name + ".rrd:VALUES" + str(i+1) + ":FAILURES",
                                "CDEF:pfail=fail,1,*",
                                "CDEF:scaledobs=obs,8,*",
                                "CDEF:upper=pred,dev,2,*,+",
                                "CDEF:lower=pred,dev,2,*,-",
                                "CDEF:scaledupper=upper,8,*",
                                "CDEF:scaledlower=lower,8,*",
                                "TICK:fail#FDD017:1.0:Failures",
                                "CDEF:scaledpred=pred,8,*", 
                                "LINE1:scaledobs#00FF00:" + labels_name[1],
                                "LINE2:scaledpred#ee0099:Forecast",
                                "LINE1:scaledupper#FF000E:Upper Bound",
                                "LINE1:scaledlower#0012FF:Lower Bound",
                                "PRINT:pfail:LAST:%0.0lf")
                                #"LINE1:obs#00FF00:" + labels_name[1],
                                #"LINE2:pred#ee0099:Forecast",
                                #"LINE1:upper#FF000E:Upper Bound",
                       	         #"LINE1:lower#0012FF:Lower Bound")

        logging.debug(ret)

        global now
        global future
        global activated

        now = time.time()
        to_normalformat = time.ctime(int(now))

        if(ret[2][0] != 'nan'):
                failure = int(ret[2][0])
                if(failure and (now > future)):
                    logging.debug("There is an error")
                    future = now + 30
                    activated = 1
                    sendEmail("Aberrant Behaviour Detetcted!! at: " + str(to_normalformat), database_name + ".png")

               	elif(failure == 0 and activated == 1):
               		logging.debug("The error has finished")
               		activated = 0
               		sendEmail("Error finished at: " + str(to_normalformat), database_name + ".png")

                logging.debug(to_normalformat)

def updateDirectGetDatabase(database_name, comunity_name, agent_ip, port, oid):
    variable_read = 0
    init_time = rrdtool.last("RRD/" + database_name + str(".rrd"))

    labels = input("Inserte el tipo de variable y el nombre: ").split(',')
    print(labels)

    if len(labels) == 2:
        while 1:
            variable_read = int(consultaSNMP(comunity_name, agent_ip, port, oid))
            value = "N:" + str(variable_read)
            logging.debug(value)
            ret = rrdtool.update("RRD/" + database_name + str(".rrd"), value)
            rrdtool.dump("RRD/" + database_name + str(".rrd"), "XML/" + database_name + str(".xml"))

            graph(database_name, 1, labels, init_time)
            time.sleep(1)


def updateDirectWalkDatabase(database_name, comunity_name, agent_ip, port, oid):
    variable_read = []
    init_time = rrdtool.last("RRD/" + database_name + str(".rrd"))
    
    labels = input("Inserte el tipo de variable y el nombre: ").split(',')
    print(labels)

    if len(labels) == 2:
        while 1:
            variable_read = consultaWALKSNMP(comunity_name, agent_ip, port, oid)
            value = "N"

            for variable in variable_read:
                value = value + ":" + str(variable)

            logging.debug(value)
            ret = rrdtool.update("RRD/" + database_name + str(".rrd"), value)
            rrdtool.dump("RRD/" + database_name + str(".rrd"), "XML/" + database_name + str(".xml"))

            time.sleep(1)
            graph(database_name, len(variable_read), labels, init_time)

def updatePercentageGetDatabase(database_name, comunity_name, agent_ip, port, oid_top, oid_variable):
    variable_read = 0
    init_time = rrdtool.last("RRD/" + database_name + str(".rrd"))

    variable_top =  int(consultaSNMP(comunity_name, agent_ip, port, oid_top))

    labels = input("Inserte el tipo de variable y el nombre: ").split(',')
    print(labels)

    if len(labels) == 2:
        while 1:
            variable_read = int(consultaSNMP(comunity_name, agent_ip, port, oid_variable))
            value = "N:" + str(int((variable_read*100)/variable_top))   
            
            logging.debug(value)
            ret = rrdtool.update("RRD/" + database_name + str(".rrd"), value)
            rrdtool.dump("RRD/" + database_name + str(".rrd"), "XML/" + database_name + str(".xml"))

            time.sleep(1)
            graph(database_name, 1, labels, init_time)