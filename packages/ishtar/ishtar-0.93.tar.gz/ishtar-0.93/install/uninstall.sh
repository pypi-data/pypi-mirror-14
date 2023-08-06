#!/bin/bash

# only lower alpha-numeric char and '_' and must start with a letter
[ $APP_NAME ] || ( echo 'APP_NAME empty. Default to: "default".' ; );
APP_NAME=${APP_NAME-default}
# don't forget the trailing slash
INSTALL_PREFIX=/srv/

read -r -p "Are you sure to delete "$APP_NAME" app? [y/N] " response
response=${response,,}    # tolower
if [[ $response =~ ^(yes|y)$ ]]
then
    echo '* deleting '$APP_NAME;
else
    echo "canceled";
    exit;
fi

# default for debian
UWSGI_AVAILABLE_PATH='/etc/uwsgi/apps-available/'
UWSGI_ENABLE_PATH='/etc/uwsgi/apps-enabled/'
NGINX_AVAILABLE_PATH='/etc/nginx/sites-available/'
NGINX_ENABLE_PATH='/etc/nginx/sites-enabled/'

DB_NAME='ishtar'$APP_NAME
INSTALL_PATH=$INSTALL_PREFIX$DB_NAME

rm -f $UWSGI_AVAILABLE_PATH$APP_NAME'.ini'
rm -f $UWSGI_ENABLE_PATH$APP_NAME'.ini'
rm -f $NGINX_AVAILABLE_PATH$APP_NAME'.conf'
rm -f $NGINX_ENABLE_PATH$APP_NAME'.conf'

rm -rf $INSTALL_PATH

echo "All file cleaned."
echo "You can delete database '"$DB_NAME"' to fully clean your installation."
