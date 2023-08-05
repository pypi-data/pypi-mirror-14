#!/bin/bash
set -e

source $BSDIR/scripts/commands.sh

SUDO="${SUDO:=}"
PIPCMD="${PIPCMD:=pip install}"
BREWCMD="${BREWCMD:=brew install}"

call mkdir -p $BS_FILES_DIR

# homebrew
BREW="${BREW:=haproxy python3 node go}"
call brew update
call $BREWCMD $BREW || true

# python dependencies
PIP="${PIP:=virtualenv}"
call $SUDO $PIPCMD $PIP || true

# python virtualenvs
call mkdir -p $BS_ENVS_DIR

# TODO: firstMatchingFile() /usr/local/bin/python2/ /usr/bin/python2/
if [ -z $PY2]; then
    if [ -f /usr/local/bin/python2/ ]; then
        PY2="${PY2:=/usr/local/bin/python2}"
    else
        PY2="${PY2:=/usr/bin/python2}"
    fi
fi

if [ -z $PY3]; then
    if [ -f /usr/local/bin/python2/ ]; then
        PY3="${PY3:=/usr/local/bin/python3}"
    else
        PY3="${PY3:=/usr/bin/python3}"
    fi
fi

slate install virtualenv -p $PY2 -name py2
slate install virtualenv -p $PY3 -name py3

slate install pypy
PYPY_VERSION="${PYPY_VERSION:=pypy-5.0.0-osx64}"
PYPY="${PYPY:=$BS_FILES_DIR/$PYPY_VERSION/bin/pypy}"
slate install virtualenv -p $PYPY -name pypy
