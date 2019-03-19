import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

#Stablish configuration parameters
hostname = "10.10.10.3"
username = "administrador@mailserver.asr"
destination = "servidorsmtp@mailserver.asr"
password = "123456"

def open_connection(verbose):
    #Connect to the server
    if verbose: print('Connecting to', hostname)
    connection = smtplib.SMTP(hostname, 25)

    # Login to our account
    if verbose: print('Logging in as', username)
    connection.login(username, password)
    return connection