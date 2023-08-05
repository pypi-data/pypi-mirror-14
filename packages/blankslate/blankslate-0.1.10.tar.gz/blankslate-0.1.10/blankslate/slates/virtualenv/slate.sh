#!/bin/bash
set -eou pipefail
source $BSDIR/scripts/commands.sh

if [ ! -d $BS_ENVS_DIR/$NAME ]; then
    call virtualenv $BS_ENVS_DIR/$NAME -p $PYTHON
else
    log "virtualenv $NAME already exists"
fi
