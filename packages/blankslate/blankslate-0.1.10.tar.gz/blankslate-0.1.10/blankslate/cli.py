#!/usr/bin/env python
import os, sys, argparse, subprocess, shlex, logging, json
import six

import blankslate
from blankslate.download import github, local
from blankslate.commands import call, fail, ok
from blankslate.logging import logger

import click

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

    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True
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

    return args, unknown

def intro():
    if not os.getenv('BS_CLI_ANNOUNCE'):
        ok("Blank Slate v%s"%blankslate.version)
        os.environ['BS_CLI_ANNOUNCE'] = '1'

def slatedirs():
    for path in ['slates', 'files', 'envs']:
        if not os.path.isdir(os.path.join(os.getenv('CALLER'), path)):
            call(['mkdir', '-p', path], target=os.getenv('CALLER'))

def unknown_args(unknown):
    a = {}
    while len(unknown):
        try:
            name = unknown.pop(0)
            value = unknown.pop(0)
        except IndexError as e:
            value = ''
        name = name.replace('--','')
        a.setdefault(name, value)
    return a

def main():
    intro()
    args, unknown = getargs()
    setenv(**args.__dict__)
    args.unknown = unknown_args(unknown)
    slatedirs()

    logger.debug("%s"%sys.argv)

    getattr(thismodule, args.action)(args)

def help():
    raise Exception("Unknown cmd, not in [install, run]")

def run(args, cmd=['bash', 'run.sh']):
    # runners are external projects, call via .sh scripts
    for k in [os.getenv('CALLER'), os.getenv('BSDIR')]:
        if os.path.isfile(os.path.join(k, 'run.sh')):
            cmd = [cmd[0]] + os.path.expandvars(shlex.split(k + '/' + cmd[1]))
            logger.debug("%s"%cmd)
            call(cmd, env=os.environ.copy())
            break

def install(args):
    slatename = resolve_installer(args, sys.argv[2])
    for k in [os.getenv('CALLER')]:
        click.echo("Installing: %s"%slatename)
        path = os.path.join(k,
                            os.getenv('BS_SLATES_DIR'),
                            slatename,)
        runnable = os.path.join(path, 'slate.sh')
        config = os.path.join(path, 'slate.json')
        installcmd = ['bash'] + shlex.split(os.path.expandvars(runnable))
        if os.path.isfile(runnable):
            # config
            slate_args = gather_slate_args(config, args.unknown)
            env = os.environ.copy()
            for key,value in six.iteritems(dict(slate_args.items() + args.unknown.items())):
                env[key.upper()] = six.text_type(value)
            # run
            res = call(installcmd, env=env)
            if res != 0:
                fail(' '.join(installcmd))
                sys.exit(0)

def gather_slate_args(path, given):
    c = parse_slate_json(path)
    r = {}
    if c.get('args'):
        click.echo("Please provide the following configuration:")
    for name, data in six.iteritems(c.get('args')):
        if name.upper() in given and 'PROMPT' not in given:
            continue
        click.echo("%s"%name.capitalize())
        if data.get('help'):
            click.echo(" > help: %s"%data['help'])
        value = click.prompt('', default=data['default'])
        r.setdefault(name, value)
    return r

def parse_slate_json(path):
    c = dict(args={}, requires=[])
    try:
        c.update(json.load(open(path)))
        r = {}
        for name, data in six.iteritems(c.get('args', {})):
            if isinstance(data, six.string_types):
                data = dict(default=data)
            r.setdefault(name, data)
        c['args']= r
    except IOError as e:
        pass
    return c

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
