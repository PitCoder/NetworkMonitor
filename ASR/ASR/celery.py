from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ASR.settings') #Configuramos la variable de entorno para obtener el modulo de configuracion

from django.conf import settings #importamos el archivo de configuracion

app = Celery('ASR') #Aqui se crea la aplicacion celery con el nombre AdquisitionData

app.config_from_object('django.conf:settings', namespace='CELERY') #Aqui se inicia la aplicación con toda la configuración del proyecto

#app.autodiscover_tasks()

app.autodiscover_tasks() #Con esto buscamos en el proyecto en las apps los metodos con la notación  @tasks

#app.conf.update(BROKER_URL = 'django://',)
#############
# Este archivo nos proporciona toda la configuración para Celery, en donde importamos el archivo de configuración del proyecto
# el cual es settings, ya que Celery funciona como una app aparte de django, por eso se instala en el archivo de settings.
# ademas de 'decirle' a la aplicación de Celery que busque en las apps del proyecto los tasks que ese usara.
#############