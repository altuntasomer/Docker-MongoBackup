import datetime
import os.path
import sys
import subprocess
import schedule
import time
import Backup
PASSWORD = "1229"
AUTO_BACKUP = False
#service_indexes = list()
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
def autoBackupOn():
    pass

def autoBackupOff():
    pass

def autoBackup():
    schedule.every().minute.do(backupAll, services)

    while True:
        schedule.run_pending()
        time.sleep(15)
        print("a")

if __name__ == '__main__':
    if (not(len(sys.argv) == 0)):
        pass

    else:
        pass

    services = subprocess.run(["sudo", "-S", "docker", "ps", "--format", "\"{{.Names}}\""],stdout=subprocess.PIPE).stdout.splitlines()
    #backupAll(services)
    autoBackup()