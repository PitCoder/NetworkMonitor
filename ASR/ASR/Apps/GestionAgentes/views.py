from django.shortcuts import render
#from django.http import HttpResponse
#from .Adquisition.multiThreading import multi  #importamos multiThreading

from ASR.Apps.GestionAgentes.models import Agente

from .tasks import *  #Importamos los tasks de la aplicación Celery

#===================Inicio de la aplicación================#

def inicio(request):
    agente = Agente.objects.all()  #Obtenemos los datos de la base
    datos = {'agentes':agente}   #Almacenamos y nombramos para usar en el HTML
    return render(request, 'index.html', datos)



#===================Monitoreo de cada Agente================#

def estado(request, host, comunidad): #Recibimos datos del agente
    dato1 = {'host': host, 'comunidad': comunidad}  #Los almacenamos y nombramos para usarlos en el HTML

    #multi(comunidad, host) #Aqui ejecutamos todos los hilos usando el MultiThreading

    #====================================
    # Aquí solo ejecutamos cada tarea de la aplicación Celery, .delay nos permite obsservar en la
    # consola de Celery los procesos que esta realizando dicho def
    #trafficReader.delay(comunidad, host)
    pingReader.delay(comunidad, host)
    icmpSegmentsReader.delay(comunidad, host)
    #tcpSegmentsReader.delay(comunidad, host)
    #updDatagramsReader.delay(comunidad, host)
    graph.delay(host)
    #===================================
    return render(request, 'estadoAg.html', dato1)


