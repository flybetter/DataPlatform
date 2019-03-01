import os
from ftplib import FTP
import paramiko

WINDOW_PATH = 'C:\\Users\\Administrator\\Desktop\\py\\house.html'
MAC_PATH = '/Users/michael/Downloads/test.txt'
LINUX_PATH = 'house.html'

server_ip = '192.168.10.221'
ftp_user = 'uftp'
ssh_user = 'root'
password = 'doucare'

docker_exec_action = 'sudo docker cp xx f8cd7d72d5ff:/app/app/templates/house/'

docker_restart_action = 'sudo docker restart f8cd7d72d5ff'


def ftp_server():
    ftp = FTP(server_ip)
    ftp.login(ftp_user, password)
    print(ftp.getwelcome())
    return ftp


def uploadfile(ftp):
    buffsize = 1024
    f = open(WINDOW_PATH, 'rb')
    ftp.storbinary(str('STOR ' + LINUX_PATH), f, buffsize)
    f.close()


def action():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, port=22, username=ssh_user, password=password)
    stdin, stdout, stderr = ssh.exec_command("docker cp /home/uftp/house.html f8cd7d72d5ff:/app/app/templates/house")
    print(stdout.readlines())
    stdin, stdout, stderr = ssh.exec_command("docker restart f8cd7d72d5ff")
    print(stdout.readlines())


if __name__ == '__main__':
    ftp = ftp_server()
    uploadfile(ftp)
    action()
