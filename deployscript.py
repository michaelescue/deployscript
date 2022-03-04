#!/bin/python

# Author: Michael Escue
# Date 3/3/22
# This is a  Python (3.8) script.
#
# Usage: python deployscript.py user host port password script
#
# Test setup:
#   Windows 11 Home 22000.493 (local) machine
#   Linux 5.13.0-30-generic (remote) machine
#   - PasswordAuthentication Allowed
#   - Port 254 instead of 22 (Personal configuration)
#   SSH connections performed over LAN due to closed ports on ISP.
#
# Brief:
#   Creates ssh connection with remote, transfers shell script to execute,
#   executes script through ssh, transfers data from remote. Data is
#   free memory from remote machine tagged with date and time info
#   down to nano-seconds.

# Required modules
import os
import sys
import paramiko

def sendScript(client, c):
    print(f'Sending {c.remote_script} to {c.user}@{c.host}.\n')

    # Create sftp connection
    sftp = client.open_sftp()

    # Send script file
    sftp.put(c.remote_script_path, f'{c.remote_script_dest}/{c.remote_script}')
    sftp.close()

def runScript(client, c):
    print(f'Running {c.remote_script} on {c.user}@{c.host}.\n')

    # Change executable permission bit over ssh
    stdin, stdout, stderr = client.exec_command(f'chmod +x ~/Desktop/{c.remote_script}')

    # Parse stdout/stderr responses
    print(''.join(stdout.readlines()))
    print(''.join(stderr.readlines()))

    # Execute shell script over ssh
    stdin, stdout, stderr = client.exec_command(f'bash ~/Desktop/{c.remote_script}')

    # Parse stdout/stderr responses
    print(stdout.readlines())
    print(stderr.readlines())

def getData(client, c):
    print(f'Getting {c.remote_data} from {c.user}@{c.host}.\n')

    # Create sftp connection
    sftp = client.open_sftp()

    # Transfer data to local machine
    sftp.get(f'{c.remote_script_dest}/{c.remote_data}', f'{c.cwd}/{c.remote_data}')

# Configuration class holding
class SshConfig:
    user = 'server'
    host = '192.168.0.3'
    port = 254  # typically 22, but personal ssh server setup differently.
    password = '********' # Enter password here, or on command line.
    cwd = os.getcwd()
    remote_script = 'remote_script.sh'
    remote_script_path = f'{cwd}/{remote_script}'
    remote_script_dest = f'/home/{user}/Desktop'
    remote_data = 'data.json'

if __name__ == '__main__':

    # Class for connection attributes
    config = SshConfig

    # If Command Line args included, update config.
    if sys.argv[1]:
        # User
        config.user = sys.argv[1]
        # Host
        config.host = sys.argv[2]
        # Port
        config.port = sys.argv[3]
        # Password
        config.password = sys.argv[4]
        # Script to deploy
        config.script = sys.argv[5]

    # SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.host,
                config.port,
                config.user,
                config.password,)

    # Required steps
    sendScript(ssh, config)
    runScript(ssh, config)
    getData(ssh, config)
