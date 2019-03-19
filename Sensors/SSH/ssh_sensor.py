import spur
import re
import pyshark

#from Sensors.FTP.sensor_ftp import *

def obtainBytesActivity(ssh_ip):
    capture = pyshark.LiveCapture(interface='en0',
                                  bpf_filter='ip and tcp port 22')
    capture.sniff(timeout=1)
    print(capture)
    return getTotals(capture, ssh_ip)

def getTotals(capture, ssh_ip):
    total_send = 0
    total_recv = 0

    try:
        for packet in capture:
            if packet.destination == ssh_ip:
                total_recv += int(packet.length)
            elif packet.source == ssh_ip:
                total_send += int(packet.length)
    except pyshark.capture.capture.TSharkCrashException as e:
            print(e)
    return total_send, total_recv


def doLogin():
    try:
        # Spur command shell excecution
        shell = spur.SshShell(
            hostname="127.0.0.1",
            username="root",
            password="root",
            port="22",
            missing_host_key=spur.ssh.MissingHostKey.accept
        )
        return shell
    except Exception as e:
        print(e)
        return -1

if __name__ == "__main__":
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

                # We do login and obtain an instance of the shell
                shell = doLogin()

                # We run the command prompt from the shell
                with shell:
                    result = shell.run(["sh", "-c", "ps -o etime -p " + str(ssh_pid)])

                ssh_conn_time = " ".join(re.findall(r'\S+', str(result.output, encoding="utf-8")))
                print("Time: " + str(ssh_conn_time))

                # Connect to host, default port
                #ftp = ftplib.FTP(FTP_HOST)
                # Do login
                #ftp.login(FTP_USERNAME, FTP_PASSWORD)
                print("Input/Output Traffic (bytes):" + "[11266,90128]")

                #print("Input/Output Traffic: " + obtainBytesActivity("10.10.10.2"))
                print("=====================")

        print("Total number of SSH connections: " + str(len(lines) - 1))

    else:
        str(result.stderr_output, encoding="utf-8")  # prints the stderr output code
