import os
import smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

smtp_ssl_host = "smtp.gmail.com"
smtp_ssl_port = 465

username = "overlord.lae@gmail.com"
password = "EALAS3KOQ"

sender = "overlord.lae@gmail.com"
targets = ["overlord.lae@gmail.com", "jllpzrmr7@gmail.com"]

msg = MIMEMultipart()
msg["Subject"] = "SMTP TESTING"
msg["From"] = sender
msg["To"] = ", ".join(targets)

txt = MIMEText("This is a SMTP testing...")
msg.attach(txt)

filepath = "pikachu.jpg"
with open(filepath, "rb") as file:
    img = MIMEImage(file.read())

img.add_header("Content-Disposition",
               "attachment",
               filename=os.path.basename(filepath))

msg.attach(img)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()