import threading
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import time

from CUPS.cups_sensor import doLogin
from HTTP.http_sensor import sense
from IMAP.imap_sensor import *
from SMTP.smtp_sensor import *
from FTP.ftp_sensor import *

logging.basicConfig( level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')

def cupsSensor():
    #We do login and obtain an instance of the shell
    shell = doLogin()

    #We run the command prompt from the shell
    with shell:
        result = shell.run(["lpstat", "-p"])

    #Then we parse the result and we process the text data
    if result.return_code == 0:
        lines = str(result.output, encoding="utf-8").split("\n")
        logging.debug("=====================")
        logging.debug("CUPS SENSOR")
        for line in lines:
            if (line != ""):
                data = str(line).split(" ")

                logging.debug("*****************")
                printer_name = data[1]
                printer_last_conn = " ".join(data[5:12])

                logging.debug("Printer name: " + str(printer_name))
                logging.debug("First enabled configuration: " + str(printer_last_conn))
                logging.debug("*****************")

        logging.debug("=====================")
        logging.debug("Total number of printers: " + str(len(lines) - 1))
    else:
        str(result.stderr_output, encoding="utf-8")  # prints the stderr output code

#def SSHSensor():

def httpSensor():
    test_web_pages = ['http://10.10.10.2:8000/']  # Hay que cambiar la IP de aquí xd

    logging.debug("=====================")
    logging.debug("HTTP SENSOR")

    for web_page in test_web_pages:
        logging.debug("*****************")
        logging.debug("Doing test to: " + web_page)
        roundtrip, size, size_in_bits, download_rate, response_code = sense(web_page)

        logging.debug('Total time: ' + str(roundtrip))  # Finally we print the result time in seconds.
        logging.debug('Total recieved bytes: ' + str(size))
        logging.debug('Total recieved bits: ' + str(size_in_bits))
        logging.debug('Download rate in bits/s: ' + str(int(download_rate)))
        logging.debug('Response code:' + str(response_code))
        logging.debug("*****************")

    logging.debug("=====================")

def imapSensor():
    conn = open_connection(verbose=False)
    try:
        logging.debug(conn)

        # Restrict mail search. Be very specific.
        # Machine should be very selective to receive messages.
        criteria = {
            'FROM': 'administrador@mailserver.asr'  # ,
            # 'SUBJECT': 'Correo de prueba del equipo # del grupo 4CM1',
            # 'BODY': 'Eric Alejandro Lopez Ayala\nJoel Lopez Romero',
        }

        # We stablish the max uid from mailbox
        uid_max = 0

        # We select the objects that are ar inbox
        conn.select('INBOX')
        result, data = conn.uid('search', None, search_string(uid_max, criteria))

        uids = [int(s) for s in data[0].split()]
        if uids:
            uid_max = max(uids)
        # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

        # We close the connection
        conn.logout()

        # Keep checking messages ...
        logging.debug("=====================")
        logging.debug("IMAP SENSOR")
        while True:
            start = time()
            end = 0
            # Have to login/logout each time because that's the only way to get fresh results.
            conn = open_connection(verbose=False)
            conn.select('INBOX')

            result, data = conn.uid('search', None, search_string(uid_max, criteria))

            uids = [int(s) for s in data[0].split()]

            for uid in uids:
                # Have to check again in case the UID criterion is not obeyed
                if uid > uid_max:
                    result, data = conn.uid('fetch', str(uid), '(RFC822)')  # Fetch entire message
                    msg = email.message_from_string(str(data[0][1], encoding="utf-8"))

                    uid_max = uid
                    # print(uid_max)

                    text = get_first_text_block(msg)
                    logging.debug('New message :::::::::::::::::::::')
                    logging.debug("Message Body: " + text)
                    end = time()
                    logging.debug("IMAP response time took: (" + str(end - start) + " seconds passed)" )
            conn.logout()
            #time.sleep(1)
        logging.debug("=====================")
    finally:
        conn.logout()

def smtpSensor():
    start = time()
    conn = open_connection(verbose=False)

    # Assembling a email basic header
    fromaddr = "administrador@mailserver.asr"
    toaddr = "servidorsmtp@mailserver.asr"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Correo de prueba del equipo # del grupo 4CM1"

    # Now we attach the body of the email to the MIME message
    body = "Eric Alejandro Lopez Ayala\nJoel Lopez Romero"
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    conn.sendmail(fromaddr, toaddr, text)
    end = time()

    logging.debug("=====================")
    logging.debug("SMTP SENSOR")
    logging.debug('Send message :::::::::::::::::::::')
    logging.debug(text)
    logging.debug("SMTP response time took (" + str(end - start) + " seconds passed)")
    logging.debug("=====================")

def ftpSensor():
    # Connect to host, default port
    ftp = ftplib.FTP(FTP_HOST)
    # Do login
    ftp.login(FTP_USERNAME, FTP_PASSWORD)

    logging.debug("=====================")
    logging.debug("FTP SENSOR")
    # Get welcome message from server
    logging.debug(ftp.getwelcome())
    start = time()
    # Doing FTP File Upload
    result = setFile(ftp)
    logging.debug("Upload of file sucessful")
    end = time()
    logging.debug("FTP response time: (%.2f seconds)" % (end - start))
    # Doing Sensor FTP Server File Count
    logging.debug(doServerScanning(ftp))
    logging.debug("=====================")
    # Quitting FTP Server Connection
    ftp.quit()

def sshSensor():
    # We do login and obtain an instance of the shell
    shell = doLogin()
    # We run the command prompt from the shell
    with shell:
        result = shell.run(["sh", "-c", "netstat -apt | grep 'ESTABLISHED.*ssh '"])

    # Then we parse the result and we process the text data
    if result.return_code == 0:
        lines = str(result.output, encoding="utf-8").split("\n")
        for line in lines:
            if (line != ""):
                data = re.findall(r'\S+', line)

                ssh_pid = int(str(data[6]).split("/")[0])
                ssh_conn = " ".join(data[4:])
                print("=====================")
                print("Process PID: " + str(ssh_pid))
                print("Connection: " + str(ssh_conn))
                # str(ssh_conn))

                # We do login and obtain an instance of the shell
                shell = doLogin()

                # We run the command prompt from the shell
                with shell:
                    result = shell.run(["sh", "-c", "ps -o etime -p " + str(ssh_pid)])

                ssh_conn_time = " ".join(re.findall(r'\S+', str(result.output, encoding="utf-8")))
                print("Time: " + str(ssh_conn_time))

                # Connect to host, default port
                ftp = ftplib.FTP(FTP_HOST)
                # Do login
                ftp.login(FTP_USERNAME, FTP_PASSWORD)

                print("Input/Output Traffic: " + obtainBytesActivity("10.10.10.2"))
                print("=====================")

        print("Total number of SSH connections: " + str(len(lines) - 1))

    else:
        str(result.stderr_output, encoding="utf-8")  # prints the stderr output code

if __name__ == "__main__":
    print("=============================")
    print("Administration monitor sensor")
    #CUPS thread monitoring sensor
    cups_thread = threading.Thread(target=cupsSensor, name='CUPS Sensor', args=[])
    #HTTP thread monitoring sensor
    http_thread = threading.Thread(target=httpSensor, name='HTTP Sensor', args=[])
    #IMAP thread monitoring sensor
    imap_thread = threading.Thread(target=imapSensor, name='IMAP Sensor', args=[])
    #SMTP thread monitoring sensor
    smtp_thread = threading.Thread(target=smtpSensor, name='SMTP Sensor', args=[])
    #FTP thread monitoring sensor
    ftp_thread = threading.Thread(target=ftpSensor, name='FTP Sensor', args=[])
    #SSH thread monitoring sensor
    ssh_thread = threading.Thread(target=sshSensor, name='SSH Sensor', args=[])

    #cups_thread.start()
    http_thread.start()
    ftp_thread.start()
    imap_thread.start()
    smtp_thread.start()
    ssh_thread.start()
    print("=============================")
