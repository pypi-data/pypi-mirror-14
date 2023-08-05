#!/bin/bash
set -e
source $BSDIR/settings

<<DESC
pypy (http://pypy.org/)
DESC

PYPY_OUT="$FILES_DIR/pypy.tar.bz2"
PYPY_VERSION="${PYPY_VERSION:=pypy-5.0.0-osx64}"
PYPY="https://bitbucket.org/pypy/pypy/downloads/${PYPY_VERSION}.tar.bz2 -O $PYPY_OUT"
if [ ! -f $PYPY_OUT ]; then
    wget $PYPY
    tar jxf $PYPY_OUT -C $FILES_DIR
else
    echo "pypy: $PYPY_OUT already exists"
fi
