#!/usr/bin/env python3
import os
import sys
import time
import shutil
import getopt
import socket
import getpass
import requests
import subprocess


class Screen:
    """Manage screen sessions.

    :param name: name of screen
    :type name: str
    """

    def __init__(self, name: str = ''):
        self.name = name

    def create(self):
        subprocess.call(['screen', '-d', '-m', '-S', str(self.name)])
    def attach(self):
        subprocess.call(['screen', '-x', str(self.name)])
    def destroy(self):
        subprocess.call(['screen', '-X', '-S', str(self.name), 'quit'])
    def list(self):
        subprocess.call(['screen', '-ls'])


def getPubkey(username: str):
    """Get a GitHub user's public SSH keys.

    :param username: username of github user
    :type username: str
    :return: an array of ssh keys
    :rtype: array
    """
    url = f'https://api.github.com/users/{username}/keys'
    data = requests.get(url).json()
    keys = []
    for key in data:
        keys.append(key['key'])

    return keys if bool(keys) else False


def helpMe():
    """Help formatter.
    """
    print("""Usage: python3 fssh.py

 -h, --help              Display this message.
 -r, --run <username>    Run script. Provide GitHub username.
 -u, --users             Connected SSH users (PID).
 -k, --kill <PID>        Kill SSH connection by PID.
 -s, --screen <instance> Create a screen with the provided name (see `man screen` for more info.)
 -l, --list              List existing screen instances.
 -a, --attach <instance> Attach to an existing screen instance with the provided name.
 -d, --delete <instance> Delete an existing screen instance defined by the provided name.""")


def start(keys):
    khPath = str(os.environ['HOME'] + '/.ssh/known_hosts')

    try:
        shutil.copyfile(khPath, khPath + '_fssh')

        with open(khPath, 'a+') as khFile:
            for k in keys:
                khFile.write('\n'+k)

        print(f'Added key(s) to {khPath}')
        print('Please do not modify the known_hosts file while the script is running, press ^C to stop the script.')
        print('Your friend can now access this computer with:')
        ipaddr = socket.gethostbyname(socket.gethostname())
        if ipaddr.startswith('127.0'):
            try:
                ipaddr = requests.get('https://api.ipify.org').text
            except:
                ipaddr = socket.gethostbyname(socket.gethostname())
        print(f'    ssh {getpass.getuser()}@{ipaddr}')

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        os.remove(khPath)
        shutil.copyfile(khPath + '_fssh', khPath)
        os.remove(khPath + '_fssh')

        print(f'\nKeys removed from {khPath}')


def getArgs(argv):
    try:
        opts, args = getopt.getopt(argv, "hr:uk:s:la:d:", ["help", "run=", "users", "kill=", "screen=", "list", "attach=", "delete="])
    except getopt.GetoptError:
        print('Invalid argument')
        exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMe()
            exit()

        elif opt in ("-r", "--run"):
            username = str(arg) if bool(str(arg)) else ''
            keys = getPubkey(username)

            if bool(username) and bool(keys):
                start(keys)
            else:
                print('GitHub user with a valid public key required, see --help for more details.')

        # SSH connections
        elif opt in ("-u", "--users"):
            users = str(subprocess.check_output(['pgrep', 'sshd']))
            print('PID of connected SSH sessions (pgrep sshd):\n' + users[2:-1].replace('\\n', '\n'))
        elif opt in ("-k", "--kill"):
            PID = str(arg)
            print(subprocess.check_output(['kill', '-9', PID]))

        # Screen-related args
        elif opt in ("-s", "--screen"):
            ScreenInstance = Screen(str(arg))
            ScreenInstance.create()
        elif opt in ("-a", "--attach"):
            ScreenInstance = Screen(str(arg))
            ScreenInstance.attach()
        elif opt in ("-d", "--delete"):
            ScreenInstance = Screen(str(arg))
            ScreenInstance.destroy()
        elif opt in ("-l", "--list"):
            ScreenInstance = Screen()
            ScreenInstance.list()
        else:
            helpMe()
            exit()


if __name__ == '__main__':
    getArgs(sys.argv[1:])
