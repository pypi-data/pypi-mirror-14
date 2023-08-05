#!/bin/bash
set -e
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "example!"

<<DESC
Example Blank Slate project
DESC

bash $CWD/packages

slate install django-haproxy -env py2 -name py2django
slate install django-haproxy -env py3 -name py3django
slate install django-haproxy -env pypy -name pypydjango

cp -R $CWD/config/ config/
cp -R $CWD/go/ go/
cp -R $CWD/nodejs/ nodejs/
cp $CWD/Procfile .

echo "Done!"

echo "Now:
./run -f slates/example/Procfile
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
