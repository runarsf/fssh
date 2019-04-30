#!/usr/bin/env python3
import os
import subprocess

username: str = 'Zawaken'
url = f'https://api.github.com/users/{username}/keys'

class Screen:
    """Manage screen sessions.

    :param name: name of screen
    :type name: str
    """

    def __init__(self, name):
        self.name = name

    def create(self):
        subprocess.call(['screen', '-d', '-m', '-S', self.name])

    def attach(self):
        subprocess.call(['screen', '-x', self.name])

    def destroy(self):
        subprocess.call(['screen', '-X', '-S', self.name, 'quit'])

def getGithubPubkey(username: str):
    """Get a GitHub user's public SSH keys.

    :param username: username of github user
    :type username: str
    """

def checkIfRoot(
        ):

if __name__ == '__main__':
    MyScreen = Screen('test')
    MyScreen.create()
    MyScreen.attach()
