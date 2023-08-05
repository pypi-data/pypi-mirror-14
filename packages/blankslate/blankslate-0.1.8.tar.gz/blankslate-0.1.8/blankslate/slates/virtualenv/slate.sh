#!/bin/bash
set -e

source $BSDIR/scripts/commands.sh
source $BSDIR/scripts/argparse.sh
argparse "$@" <<EOF || exit 1
parser.add_argument('-name', required=True)
parser.add_argument('-p', help='python binary path')
EOF

if [ ! -d $BS_ENVS_DIR/$NAME ]; then
    call virtualenv $BS_ENVS_DIR/$NAME -p $P
else
    log "virtualenv $NAME already exists"
fi
