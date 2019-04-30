#!/usr/bin/env python3
import os
import sys
import getopt
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

def getGithubPubkey(username: str):
    """Get a GitHub user's public SSH keys.

    :param username: username of github user
    :type username: str
    :return: an array of ssh keys
    :rtype:
    """
    url = f'https://api.github.com/users/{username}/keys'
    data = requests.get(url).json()
    keys = []
    for key in data:
        keys.append(key)
    return keys

def checkRootStatus():
    """Check if script is run as root.

    :return: is script run as root
    :rtype: bool
    """
    return not int(os.getuid()) > 0

def helpMe():
    """Help formatter.
    """
    helpMessage: str = """Usage: python3 fssh.py

 -h, --help              Display this message.
     --sudo              Run script without root check.
 -u, --username <string> GitHub username.
 -r, --run               Run script.
 -k, --key <string>      Public part of an SSH keypair.
 -s, --screen <string>   Create a screen with the provided name (see `man screen` for more info.)
 -l, --list              List existing screen instances.
 -a, --attach <string>   Attach to an existing screen instance with the provided name.
 -d, --delete <string>   Delete an existing screen instance defined by the provided name."""
    print(helpMessage)

def getArgs(argv):
    try:
        opts, args = getopt.getopt(argv, "k:ru:s:ha:d:l", ["help", "sudo", "run", "username=", "key=", "screen=", "list=", "attach=", "delete="])
    except getopt.GetoptError:
        print('Invalid argument')
        exit()

    sudoCheck = bool(True)
    username = ''
    pubkey = ''
    for opt, arg in opts:
        if opt == "--sudo":
            sudoCheck = bool(False)
        elif opt in ("-u", "--username"):
            username = str(arg)
        elif opt in ("-k", "--key"):
            pubkey = str(arg)

    if sudoCheck and checkRootStatus():
        print('Running the script as root could lead to unwanted side-effects.')
        print('Exiting script, if you really want to run as root, pass the --sudo argument.')
        exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMe()
            exit()

        elif opt in ("-r", "--run"):
            pubkeysDict = getGithubPubkey(username)

            try:
                pubkeysDict[0]['id']
                userHasKeys = bool(True)
                key = []
                for item in pubkeysDict:
                    key.append(item['key'])
            except:
                userHasKeys = bool(False)
                key = pubkey

            if username and userHasKeys or pubkey:
                print('Test passed successfully')
                print(key)
            else:
                print('Key or GitHub user with a valid public key required, see --help for more details.')

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


if __name__ == '__main__':
    getArgs(sys.argv[1:])
