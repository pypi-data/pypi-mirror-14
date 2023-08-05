#!/bin/bash

source $BSDIR/scripts/argparse.sh
argparse "$@" <<EOF || exit 1
parser.add_argument('-f', '--f', default="Procfile", type=str,
                    help='optional argument [default %(default)s]')
parser.add_argument('-e', '--e', default=".env", type=str,
                    help='optional argument [default %(default)s]')
EOF

python -m procboy.utils.runner -e $E -f $F
