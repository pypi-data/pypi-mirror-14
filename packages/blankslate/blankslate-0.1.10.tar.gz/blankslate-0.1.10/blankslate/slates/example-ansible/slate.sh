# !/bin/bash
set -eou pipefail
source $BSDIR/scripts/commands.sh

call pip install ansible
call ansible-playbook -i "localhost," -c local $(getcwd)/play.yml 
