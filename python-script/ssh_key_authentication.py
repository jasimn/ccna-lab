import paramiko.util
from paramiko import client,ssh_exception
from getpass import getpass
import time
import socket
paramiko.util.log_to_file("paramiko.log", level = "DEBUG")
#username = input("Please enter the username:")
# if not username:
#     username = 'jasim'
#     print(f"No username provided, considering default username {username} ")
# password = getpass(f"Please enter the password of the user {username}:") or "jasim"
username = 'jasim'
R1_commands = ['enable', 'conf t', 'int e0/1', 'ip address 192.168.12.1 255.255.255.0', 'no shut', 'do wr', 'end']
def cisco_cmd_executer(hostname, commands):
    ssh_client = client.SSHClient()
    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
    #ssh_client.load_system_host_keys()
    ssh_client.connect(hostname=hostname,
                       port=22,
                       username=username,
                       look_for_keys=True, allow_agent=True, disabled_algorithms=dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256',]))
    print("connection successfully")
    device_access = ssh_client.invoke_shell()
    device_access.send("terminal len 0\n")

    for cmd in commands:
        device_access.send(f"{cmd}\n")
        time.sleep(1)
        output = device_access.recv(65535)
        print(output.decode())
    device_access.send("show run int e0/1\n")
    output = device_access.recv(65535)
    print(output.decode())
    ssh_client.close()

cisco_cmd_executer('192.168.160.150', R1_commands)