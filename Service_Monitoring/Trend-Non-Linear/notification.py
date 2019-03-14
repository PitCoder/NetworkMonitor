import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time


pngpath = '/home/ESCOM/Documents/Pyhton/Trend-Non-Linear/IMG/' #'/home/osboxes/Desktop/TrendLineal/'

#--------------------Envio de correos
def sendEmail(subject, imag):
  
    msg = MIMEMultipart()
 
    msg['Subject'] = subject
 
 
    msg['From'] = 'escomcec@gmail.com'
    msg['To'] = 'tanibet.escom@gmail.com'
    password = "cec12345"

    fp = open(pngpath+imag, 'rb')

    msg.attach(MIMEImage(fp.read()))
 
    
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
 
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
 
 
    # send the message via the server.
    s.sendmail(msg['From'], msg['To'], msg.as_string())
 
    s.quit()
 
    print ("successfully sent email to %s:" % (msg['To']))


