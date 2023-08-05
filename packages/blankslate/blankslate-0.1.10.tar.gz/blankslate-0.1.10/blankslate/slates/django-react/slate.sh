#!/bin/bash
set -eou pipefail
source $BSDIR/scripts/commands.sh

call pip install Django django-webpack-loader
call django-admin startproject $NAME --no-color

call cd $NAME

call npm init -f
call npm install --save-dev react react-dom react-hot-loader
call npm install --save-dev babel-loader babel-cli
call npm install --save-dev babel-preset-es2015 babel-preset-react babel-preset-stage-2
call npm install --save-dev webpack webpack-bundle-tracker webpack-dev-server

call cp $(getcwd)/.babelrc .
call cp $(getcwd)/server.js .
call cp $(getcwd)/webpack.config.js .

# django
call mkdir -p assets/js $NAME/templates

call cp -R $(getcwd)/assets/js/ assets/js/
call cp -R $(getcwd)/templates/ $NAME/templates/

# urls.py with added home.html for React example
call cp $(getcwd)/project/urls.py $NAME/

# settings.py appends
cat <<EOT >> $NAME/settings.py 
INSTALLED_APPS += ['$NAME',]
INSTALLED_APPS += ['webpack_loader',]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
EOT
