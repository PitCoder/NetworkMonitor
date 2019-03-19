import spur

def doLogin():
    # Spur command shell excecution
    shell = spur.SshShell(
        hostname="10.10.10.2",
        username="servidores",
        password="12345678",
        port = "22",
        missing_host_key = spur.ssh.MissingHostKey.accept
    )
    return shell