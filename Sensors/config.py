import ftplib
import time

def connect(ip, user, password):
    ftp = ftplib.FTP(ip)
    ftp.login(user, password)
    return ftp

def getFile(ftp, file):
    try:
        ftp_file = open(file, 'wb')
        ftp.retrbinary('RETR ' + file, ftp_file.write)
        ftp.quit()
        return 0
    except Exception as e:
        print(e)
        return -1

def setFile(ftp, file):
    try:
        ftp_file = open(file, 'rb')
        ftp.storbinary('STOR ' + file, ftp_file)
        return 0
    except Exception as e:
        print(e)
        return -1

ftp = connect("30.30.30.2", "anonymous", "anonymous")

getFile(ftp, "startup_config")
setFile(ftp, "contact_info.txt")

