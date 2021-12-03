import datetime
import os.path
import sys
import subprocess
import schedule
import time
from os import getpid
PASSWORD = "1229"
AUTO_BACKUP = False

def createFolder(service,dbname,is_auto):
    dt = datetime.datetime.now()
    directory = ('backups/%s/%sbackup%s_%s_%s_%s__%s_%s'%(service,is_auto,dbname,dt.day,dt.month,dt.year,dt.hour,dt.minute))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def backupAll(services):
    for service in services:
        service = service.decode('ascii')
        service = service.replace("\"","")
        directory = createFolder(service,service,"")

        subprocess.call("echo %s | sudo -S docker exec %s sh -c 'mongodump --authenticationDatabase admin -u root -p 1234 --db %s --archive' > %s.dump"%(PASSWORD,service,service,directory + "/" + directory.split("/")[2]),shell=True)
    print("\nBacked Up")

def writePid(pid):
    file = open("pid.txt","w")
    file.write(str(pid))
    file.close()
def readPid():
    file = open("pid.txt","r")
    pid = file.read()
    file.close()
    return pid

def autoBackupOn():
    pid = subprocess.call("echo %s | nohup python3 Backup.py auto &"%(PASSWORD),shell=True)



def autoBackupOff():
    subprocess.call("kill %s"%(readPid()),shell=True)

def autoBackup(services):
    schedule.every().minute.do(backupAll, services)

    while True:
        schedule.run_pending()
        time.sleep(15)


if __name__ == '__main__':
    if ((len(sys.argv) == 2)):
        if sys.argv[1] == "autoOn":
            autoBackupOn()

        elif sys.argv[1] == "autoOff":
            autoBackupOff()

        elif sys.argv[1] == "auto":
            writePid(getpid())
            print(getpid())
            services = subprocess.run(["sudo", "-S", "docker", "ps", "--format", "\"{{.Names}}\""],stdout=subprocess.PIPE).stdout.splitlines()
            autoBackup(services)


    else:
        pass

    #backupAll(services)
    #autoBackup(services)
