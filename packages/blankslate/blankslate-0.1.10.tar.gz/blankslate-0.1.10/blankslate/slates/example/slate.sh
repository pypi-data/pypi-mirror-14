#!/bin/bash
set -eou pipefail
source $BSDIR/scripts/commands.sh
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

call bash $CWD/packages

slate install django-haproxy --ENV py2 --NAME py2django
slate install django-haproxy --ENV py3 --NAME py3django
slate install django-haproxy --ENV pypy --NAME pypydjango

call cp -R $CWD/config/ config/
call cp -R $CWD/go/ go/
call cp -R $CWD/nodejs/ nodejs/
call cp $CWD/Procfile .

log "Done!"

echo "Fire up project (processes in ./Procfile):
$ slate run
"

echo "Then browse:
http://localhost:9000 # 503 error, as no default backend configured
http://localhost:9000/py2django/
http://localhost:9000/py3django/admin/
http://localhost:9000/pypyjango/
http://localhost:9000/nodejs/
http://localhost:9000/go/hello-world/
http://localhost:9001/haproxy?stats
"

echo "Configuration:
slates/example/config/haproxy.cfg
slates/example/Procfile
"
