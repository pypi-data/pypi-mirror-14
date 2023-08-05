#!/bin/bash
set -eou pipefail
source $BSDIR/scripts/commands.sh

SUDO="${SUDO:=}"
PIPCMD="${PIPCMD:=pip install}"
BREWCMD="${BREWCMD:=brew install}"
APTGETCMD="${APTGETCMD:=apt-get install -y}"
BS_FILES_DIR="${BS_FILES_DIR:=files}"
BS_ENVS_DIR="${BS_ENVS_DIR:=envs}"

UNAME=$(uname)
if [ "$UNAME" == "Darwin" ]; then
    log "OSX -flavor"
    BREW="${BREW:=haproxy python3 node go}"
    call brew update
    $BREWCMD $BREW || true

    PYPY_VERSION="${PYPY_VERSION:=pypy-5.0.0-osx64}"
elif [ "$UNAME" == "Linux" ]; then
    echo "Linux -flavor"
    curl -sL https://deb.nodesource.com/setup_5.x | $SUDO bash -

    APTGET="${APTGET:=haproxy python3 nodejs golang}"
    call apt-get update
    call $APTGETCMD $APTGET

    PYPY_VERSION="${PYPY_VERSION:=pypy-5.0.0-linux64}"
else:
    echo "Unsupported OS"
    exit 1
fi

# python dependencies
PIP="${PIP:=virtualenv}"
call $SUDO $PIPCMD $PIP || true

# TODO: firstMatchingFile() /usr/local/bin/python2/ /usr/bin/python2/
PY2="${PY2:=}"
if [ -z $PY2]; then
    if [ -f /usr/local/bin/python2/ ]; then
        PY2="${PY2:=/usr/local/bin/python2}"
    else
        PY2="${PY2:=/usr/bin/python2}"
    fi
fi

PY3="${PY3:=}"
if [ -z $PY3]; then
    if [ -f /usr/local/bin/python2/ ]; then
        PY3="${PY3:=/usr/local/bin/python3}"
    else
        PY3="${PY3:=/usr/bin/python3}"
    fi
fi

slate install virtualenv --PYTHON $PY2 --NAME py2
slate install virtualenv --PYTHON $PY3 --NAME py3

slate install pypy --FILENAME $PYPY_VERSION
PYPY="${PYPY:=$BS_FILES_DIR/$PYPY_VERSION/bin/pypy}"
slate install virtualenv --PYTHON $PYPY --NAME pypy
