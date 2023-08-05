# !/bin/bash
set -eou pipefail

source $BSDIR/scripts/commands.sh

set +u
call source $CALLER/envs/$ENV/bin/activate
set -u
call django-admin startproject $NAME --no-color

cat <<EOT >> $CALLER/$NAME/$NAME/settings.py 
INSTALLED_APPS += ['$NAME',]
STATIC_URL = '/$NAME/static/'
STATIC_ROOT = '/tmp/$NAME/static/'
EOT

cat <<EOT >> $CALLER/$NAME/$NAME/urls.py 
from django.conf.urls import include
urlpatterns = [
    url(r'^$NAME/', include(urlpatterns)),
]
EOT
