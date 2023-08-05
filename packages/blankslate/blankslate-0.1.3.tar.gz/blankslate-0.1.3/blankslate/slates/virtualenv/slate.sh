#!/bin/bash
set -e
source $BSDIR/scripts/argparse.sh

argparse "$@" <<EOF || exit 1
`cat $BSDIR/config/argparse_settings`
parser.add_argument('-name')
parser.add_argument('-p', help='python binary path')
EOF

<<DESC
virtualenv (http://docs.python-guide.org/en/latest/dev/virtualenvs/)
DESC

if [ ! -d $ENVS_DIR/$NAME ]; then
    virtualenv $ENVS_DIR/$NAME -p $P
else
    echo "debug: virtualenv $NAME already exists"
fi
