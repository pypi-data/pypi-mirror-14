#!/usr/bin/env python
import os, sys, argparse, subprocess, shlex, logging
import six

import blankslate
from blankslate.download import github, local
from blankslate.commands import call, fail, ok
from blankslate.logging import logger

thismodule = sys.modules[__name__]

CWD = os.path.dirname(os.path.abspath(__file__))

def setenv(**kw):
    os.environ['CALLER'] = os.getcwd()
    os.environ['BSDIR'] = CWD
    for k,v in six.iteritems(kw):
        logger.debug("os.setenv: BS_%s=%s"%(k.upper(),v))
        os.environ['BS_%s'%k.upper()] = v

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-slates', '--slates-dir', default="slates/", type=str,
                        help='optional argument [default %(default)s]')
    parser.add_argument('-files', '--files-dir', default="files", type=str,
                        help='optional argument [default %(default)s]')
    parser.add_argument('-envs', '--envs-dir', default="envs", type=str,
                        help='optional argument [default %(default)s]')

    subparsers = parser.add_subparsers(help='sub-command help', dest='action')
    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('-f', '--f', default="Procfile", type=str,
                        help='optional argument [default %(default)s]')
    parser_run.add_argument('-e', '--e', default=".env", type=str,
                        help='optional argument [default %(default)s]')

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument('slate')

    # 1) -h: remove when beyond args.action for argparses beyond this point
    has_help = '-h' in sys.argv
    if has_help and len(sys.argv) > 3:
        sys.argv.remove('-h')

    args, unknown = parser.parse_known_args()

    # 2) -h:
    if has_help:
        sys.argv.append('-h')

    return args

def intro():
    if not os.getenv('BS_CLI_ANNOUNCE'):
        ok("Blank Slate v%s"%blankslate.version)
        os.environ['BS_CLI_ANNOUNCE'] = '1'

def main():
    intro()
    args = getargs()
    setenv(**args.__dict__)

    logger.debug("%s"%sys.argv)

    getattr(thismodule, args.action)(args)

def help():
    raise Exception("Unknown cmd, not in [install, run]")

def run(args, cmd=['bash', 'run.sh']):
    # runners are external projects, call via .sh scripts
    for k in [os.getenv('CALLER'), os.getenv('BSDIR')]:
        if os.path.isfile(os.path.join(k, 'run.sh')):
            cmd = [cmd[0]] + os.path.expandvars(shlex.split(k + '/' + cmd[1]))
            cmd += sys.argv[2:] # pass arguments
            logger.debug("%s"%cmd)
            call(cmd, env=os.environ.copy())
            break

def install(args):
    slatename = resolve_installer(args, sys.argv[2])
    for k in [os.getenv('BSDIR'), os.getenv('CALLER')]:
        path = os.path.join(k,
                            os.getenv('BS_SLATES_DIR'),
                            slatename,
                            'slate.sh')
        installcmd = ['bash'] + shlex.split(os.path.expandvars(path))
        installcmd += sys.argv[2:] # pass arguments
        if os.path.isfile(path):
            res = call(installcmd, env=os.environ.copy())
            if res != 0:
                fail(' '.join(installcmd))
                sys.exit(0)

def resolve_installer(args, cmd):
    if ':' in cmd:
        source, package = cmd.split(':')
        if source == 'github':
            github(package)
        else:
            raise Exception("Unsupported installation source.")
        cmd = package
    else:
        local(args.slate)
    return cmd


if __name__ == '__main__':
    main()
