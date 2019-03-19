import spur

#Sample to run echo locally
shell = spur.LocalShell()
result = shell.run(["echo", "-n", "hello"])
print(str(result.output, encoding="utf-8")) # prints hello


#Excecuting the same command but now over SSH uses the same interface -the only diference is how the shell is been created
shell = spur.SshShell(
    hostname="10.100.78.61",
    username="ESCOM",
    password="EALAS3KO@"
)

with shell:
    result = shell.run(["echo", "-n", "hello"])
print(str(result.output, encoding="utf-8")) # prints hello

#Spur command shell excecution
shell = spur.SshShell(
    hostname="10.100.78.61",
    username="ESCOM",
    password="EALAS3KO@"
)

with shell:
    result = shell.run(["lpstat", "-p"])

if result.return_code == 0:
    lines = str(result.output, encoding="utf-8").split("\n")
    for line in lines:
        if(line != ""):
            data = str(line).split(" ")
            print(data)
            printer_name = data[1]
            printer_last_conn = " ".join(data[5:12])

            print(printer_name)
            print(printer_last_conn)

    print("Total number of printers: " + str(len(lines) - 1))

else:
    str(result.stderr_output, encoding="utf-8") # prints the stderr output code