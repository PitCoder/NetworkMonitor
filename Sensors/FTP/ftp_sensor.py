import ftplib
from time import time

FTP_HOST = "10.10.10.2"
FTP_USERNAME = "servidores"
FTP_PASSWORD = "12345678"

ftp = None
TEST_FILE = "configuracion.txt"

def getFile(ftp, file):
    try:
        ftp_file = open(file, 'wb')
        ftp.retrbinary('RETR ' + file, ftp_file.write)
        ftp.quit()
        return 0
    except Exception as e:
        print(e)
        return -1

def setFile(ftp):
    try:
        ftp_file = open(TEST_FILE, 'rb')
        ftp.storbinary('STOR ' + TEST_FILE, ftp_file)
        return 0
    except Exception as e:
        print(e)
        return -1

def doSubScanning(ftp, dir_path):
    try:
        ftp.cwd(dir_path)
        subdirectory_content = ftp.nlst()
        files = len(subdirectory_content)
        file_scan = ""

        if (files > 0):
            for directory in subdirectory_content:
                file_scan = file_scan + "Scanning directory/file: " + directory + "\n"
                if "." not in directory:
                    file_scan = file_scan + doSubScanning(ftp, dir_path + "/" + directory + "/")
        return file_scan
    except Exception as e:
        print(e)
        return -1

def doServerScanning(ftp):
    try:
        root_directory_content = ftp.nlst()
        file_scan = ""
        file_scan = file_scan + "Scanning: Server Root Directory\n"
        for directory in root_directory_content:
            file_scan = file_scan + "Scanning directory/file: " + directory + "\n"
            #if "." not in directory:
                #file_scan = file_scan + doSubScanning(ftp, "/" + directory + "/")
        return file_scan
    except Exception as e:
        print(e)
        return -1