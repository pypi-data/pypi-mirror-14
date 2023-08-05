#!/bin/bash
set -e
echo "slate.sh: $@"
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $CWD/settings

printf "$(tput setaf 2)Running: $CWD/${DIR}${SLATE}/slate.sh $@ $(tput sgr0)\n"
bash "${CWD}/${DIR}${SLATE}/slate.sh" "$@"
