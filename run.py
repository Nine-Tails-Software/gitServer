import os, subprocess, requests


def runServerCommandOutput(command: list[str]) -> list[bytes]:
    temp = subprocess.Popen(command, stdout = subprocess.PIPE) 
    context = list(temp.communicate())
    return context

def runServerCommandStr(command: str) -> int:
    return os.system(command)


def moveFiles(FROM: str, TO: str):
    return runServerCommandStr(f"mv {FROM} {TO}")

def rm(path: str):
    return runServerCommandStr(f"rm -r {path}")

def mkdir(path: str):
    return runServerCommandStr(f"mkdir {path}")


def download_url_file(url: str, fileName: str, folder: str, fullName: str):
    if not os.path.isfile(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/{fileName}"):
        r = requests.get(url, allow_redirects=True)
        open(f'/mnt/md0/samba/gitServer/{folder}/{fullName}/{fileName}', 'wb').write(r.content)
        print("Finished Download")
    else:
        print("File Already Exists")


def create_runSH_file_server(startCommand: str, fullName: str, folder: str):
    f = open(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/run.sh", "x")
    f = open(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/run.sh", "w")
    f.write(f"""#!/bin/bash
cd /mnt/md0/samba/gitServer/{folder}/{fullName}
{startCommand}
    """)
    f.close
    runServerCommandStr(f"chmod +x /mnt/md0/samba/gitServer/{folder}/{fullName}/run.sh")

def createServiceFile(description: str, fullName: str, folder: str):
    f = open(f"/etc/systemd/system/{fullName}.service", "x")
    f = open(f"/etc/systemd/system/{fullName}.service", "w")
    description = description.replace("\n", " ")
    f.write(f"""
[Unit]
Description= {description}
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=5
User=root
ExecStart=/mnt/md0/samba/gitServer/{folder}/{fullName}/run.sh

[Install]
WantedBy=multi-user.target
    """)
    f.close



def start_service(fullName: str):
    return runServerCommandStr(f"systemctl start {fullName}.service")

def status_service(fullName: str):
    return runServerCommandOutput(["systemctl", "status", f"{fullName}.service"])[0].decode('UTF-8')

def stop_service(fullName: str):
    return runServerCommandStr(f"systemctl stop {fullName}.service")





def change_minecraft_Eula(fullName: str, folder: str):
    f = open(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/eula.txt", "w")
    f.write("""#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
    #Sat Dec 31 20:44:55 UTC 2022
    eula=true
    """)
    f.close()

def runJava_8(command: list[str]) -> list[bytes]:
    command = ["/usr/lib/jvm/java-8-openjdk-amd64/bin/java"] + command
    temp = subprocess.Popen(command, stdout = subprocess.PIPE)
    context = list(temp.communicate())
    return context

def runJava_11(command: list[str]) -> list[bytes]:
    command = ["/usr/lib/jvm/java-11-openjdk-amd64/bin/java"] + command
    temp = subprocess.Popen(command, stdout = subprocess.PIPE)
    context = list(temp.communicate())
    return context

def runJava_17(command: list[str]) -> list[bytes]:
    command = ['/usr/lib/jvm/java-17-openjdk-amd64/bin/java'] + command
    #print(command)
    temp = subprocess.Popen(command, stdout = subprocess.PIPE)
    context = list(temp.communicate())
    return context

def fix_perms(fullName: str, folder: str):
    runServerCommandOutput(["chmod", "-R", "a+rwX", f"/mnt/md0/samba/gitServer/{folder}/{fullName}/"])[0].decode('UTF-8')


from time import sleep
#minecraft_server.1.19.3.jar
url = "https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar"
javaVersion = 17
startCommand = '"/usr/lib/jvm/java-17-openjdk-amd64/bin/java" -Xmx8G -Xms2G -jar minecraft_server.jar nogui'
description = "Testing Minecraft Server for 1.19.3"

fullName = "testing"
folder = "servers"

fileName = "minecraft_server.jar"

"""

#Makes server folder
print("Creating Server Folder")
mkdir(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/")

#Downloads the launcher
print("Downloading File")
download_url_file(url, fileName, folder, fullName)

#runs firsts to generate eula.txt
#print("Running server file for first time")
#if javaVersion == 17:
#    print(runJava_17(["-Xmx4G", "-Xms4G", "-jar", "/mnt/md0/samba/testing/minecraft_server.jar", "nogui"]))
#elif javaVersion == 11:
#    print(runJava_11(["-Xmx4G", "-Xms4G", "-jar", "/mnt/md0/samba/testing/minecraft_server.jar", "nogui"]))
#elif javaVersion == 8:
#    print(runJava_8(["-Xmx4G", "-Xms4G", "-jar", "/mnt/md0/samba/testing/minecraft_server.jar", "nogui"]))
#sleep(1)

#Changes Eula to true
print("Changing Eula")
change_minecraft_Eula(fullName, folder)

#Generates run.sh file
print("Creating run.sh File")
create_runSH_file_server(startCommand, fullName, folder)

#Generate Service file
print("Generating Service file")
createServiceFile(description, fullName, folder)

#Start Service
print("Start Service")
start_service(fullName)

# wait for server to generate
print("Waiting for 10 sec")
sleep(10)

# stop
print("Stopping Service")
stop_service(fullName)

# edit server.properties


#fixs perms so non admins can edit files
#fix_perms(fullName, folder)


"""

def parse_server_properties(fullName: str, folder: str):
    f = open(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/server.properties", "r")
    lines = f.readlines()
    lines_ = []
    for x in lines:
        if "#" in x:
            continue
        x = x.strip("\n ")
        lines_.append(x)
    properties = {}
    for x in lines_:
        split = x.split("=")
        properties.update({split[0]: split[1]})
    return properties

def write_server_properties(fullName: str, folder: str, properties: dir):
    keys = list(properties.keys())
    values = list(properties.values())
    #print(keys)
    #print(values)

    lines = []
    for x in range(0, (len(keys)-1)):
        lines.append(f"{keys[x]}={values[x]}")

    print(lines)
    line = ""
    for x in lines:
        line = line + f"{x}\n"

    f = open(f"/mnt/md0/samba/gitServer/{folder}/{fullName}/server.properties", "w")
    f.write(line)
    f.close

props = parse_server_properties(fullName, folder)

props["server-ip"] = "192.168.1.200"
props["server-port"] = "25575"

write_server_properties(fullName, folder, props)