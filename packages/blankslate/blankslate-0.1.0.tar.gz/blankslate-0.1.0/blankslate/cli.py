#!/usr/bin/env python
import os, sys, argparse, subprocess, shlex, logging

thismodule = sys.modules[__name__]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('blankslate')

CWD = os.path.dirname(os.path.abspath(__file__))

"""
install NAME:
- copy installable dir of slate.sh to slates/NAME
- run ./slates/NAME/slate.sh

run:
- procboy (run.sh)
"""

def setenv():
    os.environ['CALLER'] = os.getcwd()
    os.environ['BSDIR'] = CWD

def main():
    setenv()

    logger.debug("%s"%sys.argv)

    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in ['install', 'run']:
        cmd = 'help'
    getattr(thismodule, cmd)()

def help():
    raise Exception("Unknown cmd, not in [install, run]")

def run(cmd=['bash', 'run.sh']):
    cmd = [cmd[0]] + os.path.expandvars(shlex.split(CWD + '/' + cmd[1]))
    cmd += sys.argv[1:] # pass arguments
    logger.debug("%s"%cmd)
    subprocess.call(cmd, env=os.environ.copy())

def install(cmd=['bash', 'slate.sh']):
    cmd = [cmd[0]] + os.path.expandvars(shlex.split(CWD + '/' + cmd[1]))
    cmd += sys.argv[1:] # pass arguments
    logger.debug("%s"%cmd)
    subprocess.call(cmd, env=os.environ.copy())


if __name__ == '__main__':
    main()
