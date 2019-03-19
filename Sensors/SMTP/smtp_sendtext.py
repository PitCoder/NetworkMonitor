import smtplib
from email.mime.text import  MIMEText

smtp_ssl_host = 'smtp_gmail.com' #Note: This can be: smtp.mail.yahoo.com, smtp-mail.outlook.com, etc..-
smtp_ssl_port = 465

username = "overlord.lae@gmail.com"
password = "EALAS3KO@"

sender = "overlord.lae@gmail.com"
targets = ["eralejandroayala@gmail.com", "jllpzrmr7@gmail.com"]

msg = MIMEText("Hola guapo, esta programando solo 7u7?")
msg["Subject"] = "Hola uwu"
msg["From"] =  sender
msg["To"] = ", ".join(targets)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()