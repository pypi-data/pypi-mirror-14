#!/bin/bash
set -e
source $BSDIR/scripts/commands.sh

PYPY_OUT="$BS_FILES_DIR/pypy.tar.bz2"
PYPY_VERSION="${PYPY_VERSION:=pypy-5.0.0-osx64}"
PYPY="https://bitbucket.org/pypy/pypy/downloads/${PYPY_VERSION}.tar.bz2 -O $PYPY_OUT"
if [ ! -f $PYPY_OUT ]; then
    call wget $PYPY
    call tar jxf $PYPY_OUT -C $BS_FILES_DIR
else
    log "$PYPY_OUT already exists"
fi
