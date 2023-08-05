import subprocess
import shlex
import os

from blankslate.commands import call

def callerpath(*path):
    return os.path.join(os.getenv('CALLER'), *path)

def mkdir(path):
    call(['mkdir', '-p', path])

def git_clone(repository, target):
    cmd = shlex.split("git clone %s"%repository)
    call(cmd, target=target)

def github(repository):
    author = repository.split('/')[0]
    repo = '/'.join(repository.split('/')[1:])
    p = callerpath('slates', author)
    mkdir(p)
    if not os.path.isdir(callerpath('slates', author, repo)):
        git_clone("https://github.com/%s.git"%repository, target=p)
    call(['rm', '-rf', callerpath('slates', author, repo, '.git')])

def local(repository):
    call(['cp', '-R',
            os.path.join(os.getenv('BSDIR'), 'slates', repository) + os.sep,
            callerpath('slates', repository) + os.sep])
