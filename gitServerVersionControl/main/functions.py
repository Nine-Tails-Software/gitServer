


from datetime import datetime
def defaultContext():
    cTime = datetime.utcnow()
    context = {
        'cTime': cTime
    }
    return context



from random import randint
def genCode(num: int, codeList: list[int]) -> str:
    charListStr = "abcdefghkpqrstuvwxyzABCDEFGHJKLPQRSTUVWXYZ123456789"
    charList = []
    charList.extend(charListStr)
    code = ''

    for x in range(0, num):
        char = str(charList[randint(0, len(charList)-1)])
        code = code+char
        
    if code in codeList:
        code = genCode(num, codeList)
    
    return code


import subprocess  
def runServerCommandOutput(command: list[str]) -> list[bytes]:
    temp = subprocess.Popen(command, stdout = subprocess.PIPE) 
    context = list(temp.communicate())
    return context

def runServerCommandStr(command: str) -> int:
    return os.system(command)



import os
def cloneRepo(url: str, tagName: str):
    return runServerCommandStr(f"git clone --branch {tagName} {url} /mnt/md0/samba/gitServer/temp/c")

def getTags(url: str):
    #tags = os.system(f"git ls-remote --tags --sort='v:refname' {url}")
    cmd = ["git", "ls-remote", '--tags', f"{url}"]
    
    tagsStr = str(runServerCommandOutput(cmd)).strip("()b").split("None")[0]
    #print(f"|{tagsStr}|")
    tagsStr = tagsStr.rstrip(", ")
    #print(f"|{tagsStr}|")
    tagsStr = tagsStr.strip("' ").strip("\\n ")
    #print(f"|{tagsStr}|")
    tagsStr = tagsStr.split("\\n")
    #print(f"|{tagsStr}|")
    tags = []
    for x in tagsStr:
        x = x.split("/")
        x = x[-1]
        tags.append(x)

    return tags

def moveFiles(FROM: str, TO: str):
    return runServerCommandStr(f"mv {FROM} {TO}")

def rm(path: str):
    return runServerCommandStr(f"rm -r {path}")

def mkdir(path: str):
    return runServerCommandStr(f"mkdir {path}")

def newFile(path: str):
    return runServerCommandStr(f"touch {path}")



def create_runSH_file(startCommand: str,fullName: str):
    f = open(f"/mnt/md0/samba/gitServer/programs/{fullName}/run.sh", "x")
    f = open(f"/mnt/md0/samba/gitServer/programs/{fullName}/run.sh", "w")
    f.write(f"""#!/bin/bash
cd /mnt/md0/samba/gitServer/programs/{fullName}/c
{startCommand}
    """)
    f.close
    runServerCommandStr(f"chmod +x /mnt/md0/samba/gitServer/programs/{fullName}/run.sh")



def createServiceFile(description: str,fullName: str):
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
ExecStart=/mnt/md0/samba/gitServer/programs/{fullName}/run.sh

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

def enable_service(fullName: str):
    return runServerCommandOutput(["systemctl", "enable", f"{fullName}.service"])[0].decode('UTF-8')

def disable_service(fullName: str):
    return runServerCommandOutput(["systemctl", "disable", f"{fullName}.service"])[0].decode('UTF-8')

def journalctl_service(fullName: str):
    return runServerCommandOutput(["journalctl", "-u", f"{fullName}.service"])[0].decode('UTF-8')

def daemon_reload():
    runServerCommandOutput(["systemctl", "daemon-reload"])[0].decode('UTF-8')

def fix_perms_programs(fullName: str):
    runServerCommandOutput(["chmod", "-R", "a+rwX", f"/mnt/md0/samba/gitServer/programs/{fullName}/"])[0].decode('UTF-8')



#enable = True
#url = "https://github.com/Waffleer/Tournament-Discord-Bot/"
#cTag = "v1.0.2"
#fullName = "Waffleer_Tournament-Discord-Bot_RkzX1A"
#startCommand = "python3 bot.py"
#description = "Testing Description"

#rm(f"/etc/systemd/system/{fullName}.service")
#rm(f"/mnt/md0/samba/gitServer/programs/{fullName}/")
#disable_service(fullName)


def remove_repository(fullName: str):
    disable_service(fullName)
    print(rm(f"/etc/systemd/system/{fullName}.service"))
    print(rm(f"/mnt/md0/samba/gitServer/programs/{fullName}/"))
    daemon_reload()


from time import sleep
def generate_repository(url: str, cTag: str, fullName: str, startCommand: str, description: str):
    #try:
    print(cloneRepo(url, cTag))
    sleep(1)
    print(mkdir(f"/mnt/md0/samba/gitServer/programs/{fullName}"))
    print(moveFiles("/mnt/md0/samba/gitServer/temp/c", f"/mnt/md0/samba/gitServer/programs/{fullName}/c"))
    print(create_runSH_file(startCommand, fullName))
    print(createServiceFile(description, fullName))

    print("\n\n\n")
    print(daemon_reload())
    sleep(1)
    print("\n\n\n")
    print(status_service(fullName))
    print("\n\n\n")
    print(start_service(fullName))
    print("\n\n\n")
    print(status_service(fullName))
    print("\n\n\n")
    fix_perms_programs(fullName)
    #except:
    #    print("\n\nSomething Failed in Repo Implementation")


#print(journalctl_service(fullName))

#generate_repository(url, cTag, fullName, startCommand, description)
#remove_repository(fullName)

#daemon_reload()
#fix_perms()


#print(stop_service(fullName))
#print("\n\n\n")
#print(status_service(fullName))

#create service file

from .models import Repository
def parse_repo(context: dict, repo: Repository):
    name = repo.name
    description = repo.description
    owner = repo.owner
    keepNumber = repo.keepNumber
    fullName = repo.fullName
    startCommand = repo.startCommand
    url = repo.url
    cTag = repo.cTag
    code = repo.code
    enable = repo.enable
    running = repo.running
    created = repo.created
    updated = repo.updated
    context.update({"name": name})
    context.update({"description": description})
    context.update({"owner": owner})
    context.update({"keepNumber": keepNumber})
    context.update({"fullName": fullName})
    context.update({"startCommand": startCommand})
    context.update({"url": url})
    context.update({"cTag": cTag})
    context.update({"code": code})
    context.update({"running":running})
    context.update({"enable": enable})
    context.update({"created": created})
    context.update({"updated": updated})
    return context