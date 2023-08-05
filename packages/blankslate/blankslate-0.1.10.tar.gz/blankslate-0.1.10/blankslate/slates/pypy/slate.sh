#!/bin/bash
set -eou pipefail
source $BSDIR/scripts/commands.sh

PYPY_OUT="$BS_FILES_DIR/pypy.tar.bz2"
PYPY="https://bitbucket.org/pypy/pypy/downloads/${FILENAME}.tar.bz2 -O $PYPY_OUT"
if [ ! -f $PYPY_OUT ]; then
    call wget $PYPY
    call tar jxf $PYPY_OUT -C $BS_FILES_DIR
else
    log "$PYPY_OUT already exists"
fi
