#!/bin/bash

set -e
set -x

######################################################################
# Minimum configuration                                              #
######################################################################

# only lower alpha-numeric char and '_' and must start with a letter
[ -z "$APP_NAME" ] && ( echo 'APP_NAME empty. Default to: "default".' ; );
APP_NAME=${APP_NAME-default}

[ -z $URL ] && ( echo 'URL empty. Default to: "localhost".' ; URL=localhost ; );
URL=${URL-localhost}

[ -z "$PROJECT_NAME" ] && ( echo 'PROJECT_NAME empty. Default to: "Test".' ; );
PROJECT_NAME=${PROJECT_NAME-Test}

DEFAULT_DATA='fr' # available data: 'fr'

######################################################################
# Advanced configuration                                             #
######################################################################

# if the database is not local the database will be not automatically
# created
[ -z $DB_HOST ] && ( echo 'DB_HOST empty. Default to: "127.0.0.1".' ; );
DB_HOST=${DB_HOST-127.0.0.1}

# if not set automatically generated
DB_PASSWORD=${DB_PASSWORD-''}
DB_PORT='5432'
PG_VERSION=9.1

# ishtar git branch
[ -z "$VERSION" ] && ( echo 'VERSION empty. Default to: "stable".' ; );
VERSION=${VERSION-stable}

# change it for each instance on a same server
UWSGI_PORT=${UWSGI_PORT-8891}

# webserver port - default "80"
NGINX_PORT=${NGINX_PORT-80}

# don't forget the trailing slash
INSTALL_PREFIX=${INSTALL_PREFIX-/srv/}
if ! echo "$INSTALL_PREFIX" | grep -qs '/$'; then
    INSTALL_PREFIX="$INSTALL_PREFIX/"
fi

# if a virtualenv is used put the full path of the python to use
PYTHON=python

# proxy for pip
PIP_OPTIONS=''
[ -z "$http_proxy" ] || PIP_OPTIONS=' --proxy '$http_proxy;
[ -z "$HTTP_PROXY" ] || PIP_OPTIONS=' --proxy '$HTTP_PROXY;

# default for debian
UWSGI_AVAILABLE_PATH='/etc/uwsgi/apps-available/'
UWSGI_ENABLE_PATH='/etc/uwsgi/apps-enabled/'
NGINX_AVAILABLE_PATH='/etc/nginx/sites-available/'
NGINX_ENABLE_PATH='/etc/nginx/sites-enabled/'

# Don't edit below this line
######################################################################

echo "* installing dependencies"

APT_GET=${APT_GET-apt-get}
PIP=${PIP-pip}

if [ $DB_HOST = "127.0.0.1" ]; then
    $APT_GET -q -y install postgresql postgresql-$PG_VERSION-postgis postgresql 2> /dev/null > /dev/null
fi

$APT_GET -q -y install git apg python-pip 2> /dev/null > /dev/null

$APT_GET -q -y install python python-django \
      libjs-jquery libjs-jquery-ui python-pisa python-django-registration \
      python-utidylib python-lxml python-imaging python-django-south \
      python-psycopg2 python-gdal gettext python-bs4 python-tidylib \
      python-unicodecsv \
      python-django-extra-views python-memcache python-dbf 2> /dev/null > /dev/null

$APT_GET -q -y install uwsgi uwsgi-plugin-python nginx memcached 2> /dev/null > /dev/null

$PIP install$PIP_OPTIONS BeautifulSoup4==4.3.2

if [ -z "$DB_PASSWORD" ]
then

DB_PASSWORD=`apg -a 0 -M ncl -n 6 -x 10 -m 10 |head -n 1`

fi

DB_NAME='ishtar'$APP_NAME
INSTALL_PATH=$INSTALL_PREFIX$DB_NAME
DATE=`date +%F`
CDIR=`readlink -f $(dirname $0)`
SECRET_KEY=`apg -a 0 -M ncl -n 6 -x 10 -m 40 |head -n 1`

if [ $DB_HOST = '127.0.0.1' ]
then

echo "* create database and user"
DB_PASSWORD=$DB_PASSWORD DB_NAME=$DB_NAME PROJECT_NAME=$PROJECT_NAME PG_VERSION=$PG_VERSION su postgres <<'EOF'
cd
if [ `psql -l | grep template_postgis | wc -l` -ne 1 ]; then
    echo "  * create template_postgis"
    createdb template_postgis
    psql -d template_postgis -f /usr/share/postgresql/$PG_VERSION/contrib/postgis-1.5/postgis.sql 2> /dev/null > /dev/null
    psql -d template_postgis -f /usr/share/postgresql/$PG_VERSION/contrib/postgis-1.5/spatial_ref_sys.sql 2> /dev/null > /dev/null

fi
if [ `psql -l | grep $DB_NAME | wc -l` -ne 1 ]; then
    echo "  * create "$DB_NAME
    createuser --echo --adduser --createdb --encrypted $DB_NAME 2> /dev/null > /dev/null
    psql --command "ALTER USER \""$DB_NAME"\" with password '"$DB_PASSWORD"';" 2> /dev/null > /dev/null
    createdb -T template_postgis --echo --owner $DB_NAME --encoding UNICODE $DB_NAME "$PROJECT_NAME" 2> /dev/null > /dev/null

fi
EOF

fi


echo '* get sources'

mkdir -p $INSTALL_PATH
mkdir $INSTALL_PATH'/conf'
cd $INSTALL_PATH

echo '  * ishtar'
git clone https://gitlab.com/ishtar/ishtar.git 2> /dev/null
# echo '  * oook!'
# git clone git://git.proxience.com/git/oook_replace.git 2> /dev/null
# ln -s $INSTALL_PATH'/oook_replace/oook_replace' $INSTALL_PATH'/ishtar/'

cd ishtar
git fetch 2> /dev/null
git checkout $VERSION 2> /dev/null

cd django-simple-history
python setup.py install
cd ..

cp -ra example_project $APP_NAME 2> /dev/null > /dev/null

rm $APP_NAME/settings.py
ln -s $INSTALL_PATH"/ishtar/example_project/settings.py" $INSTALL_PATH"/ishtar/"$APP_NAME"/"

APP_DIR=$INSTALL_PATH'/ishtar/'$APP_NAME

echo '* load parameters'
sed -s "s|#APP_NAME#|$APP_NAME|g;\
        s|#INSTALL_PATH#|$INSTALL_PATH|g;\
        s|#DATE#|$DATE|g;\
        s|#PROJECT_NAME#|$PROJECT_NAME|g;\
        s|#DB_HOST#|$DB_HOST|g;\
        s|#DB_NAME#|$DB_NAME|g;\
        s|#DB_PORT#|$DB_PORT|g;\
        s|#APP_DIR#|$APP_DIR|g;\
        s|#SECRET_KEY#|$SECRET_KEY|g;\
        s|#DB_PASSWORD#|$DB_PASSWORD|g;\
        s|#UWSGI_PORT#|$UWSGI_PORT|g;" $CDIR'/local_settings.py.sample' > \
                                  $INSTALL_PATH'/conf/local_settings.py'

ln -s $INSTALL_PATH'/conf/local_settings.py' $APP_DIR'/local_settings.py'

# rights
mkdir -p $APP_DIR'/media'
chown -R root:www-data $APP_DIR'/media'
chmod -R g+w $APP_DIR'/media'

# logs
mkdir -p /var/log/django/
chown root:www-data '/var/log/django'
touch '/var/log/django/ishtar-'$APP_NAME'.log'
chown root:www-data '/var/log/django/ishtar-'$APP_NAME'.log'
chmod g+w '/var/log/django/ishtar-'$APP_NAME'.log'

cd $APP_DIR
./manage.py collectstatic --noinput 2> /dev/null > /dev/null

# load locale data

cd $INSTALL_PATH'/ishtar/archaeological_context_records'
django-admin compilemessages -l fr 2> /dev/null
cd $INSTALL_PATH'/ishtar/archaeological_files'
django-admin compilemessages -l fr 2> /dev/null
cd $INSTALL_PATH'/ishtar/archaeological_finds'
django-admin compilemessages -l fr 2> /dev/null
cd $INSTALL_PATH'/ishtar/archaeological_operations'
django-admin compilemessages -l fr 2> /dev/null
cd $INSTALL_PATH'/ishtar/archaeological_warehouse'
django-admin compilemessages -l fr 2> /dev/null
cd $INSTALL_PATH'/ishtar/ishtar_common'
django-admin compilemessages -l fr 2> /dev/null

echo "* sync database"

cd $APP_DIR
python ./manage.py syncdb --noinput 2> /dev/null > /dev/null
python ./manage.py migrate 2> /dev/null > /dev/null

echo "* load default data"
# data migrations have created some default data - return to a clean state
python ./manage.py flush --noinput 2> /dev/null

python ./manage.py loaddata \
    '../fixtures/initial_data-auth-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../ishtar_common/fixtures/initial_data-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../ishtar_common/fixtures/initial_towns-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../archaeological_operations/fixtures/initial_data-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../archaeological_files/fixtures/initial_data-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../archaeological_context_records/fixtures/initial_data-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../archaeological_finds/fixtures/initial_data-'$DEFAULT_DATA'.json' 2> /dev/null
python ./manage.py loaddata \
    '../archaeological_warehouse/fixtures/initial_data-'$DEFAULT_DATA'.json' 2> /dev/null

echo "* create superuser"
python ./manage.py createsuperuser

# "de-flush" migrations
$PYTHON ./manage.py migrate --fake 2> /dev/null > /dev/null

# add a default site
#echo '[{"pk":null, "model": "sites.site", "fields": {"domain": "'$URL'", "name": "'$PROJECT_NAME'"}}]' > \
#    /tmp/site.json
#python ./manage.py loaddata /tmp/site.json
#rm /tmp/site.json

echo '* uwsgi configuration'

# NOTE: Replacing #INSTALL_PREFIX#/ is done on purpose, since we
#       ensured that variable has a trailing slash.
sed -s "s|#APP_NAME#|$APP_NAME|g;\
        s|#DB_NAME#|$DB_NAME|g;\
        s|#INSTALL_PREFIX#/|$INSTALL_PREFIX|g;\
        s|#URL#|$URL|g;\
        s|#UWSGI_PORT#|$UWSGI_PORT|g;" $CDIR'/uwsgi.ini.template' > \
                                       $INSTALL_PATH'/conf/uwsgi.ini'

sed -s "s/#APP_NAME#/$APP_NAME/g;" $CDIR'/django.wsgi.template' > \
                    $INSTALL_PATH'/conf/'$APP_NAME'.wsgi'

ln -s $INSTALL_PATH'/conf/uwsgi.ini' \
      $UWSGI_AVAILABLE_PATH$APP_NAME'.ini'
ln -s $UWSGI_AVAILABLE_PATH$APP_NAME'.ini' \
      $UWSGI_ENABLE_PATH$APP_NAME'.ini'

service uwsgi restart

echo '* nginx configuration'


# NOTE: Replacing #INSTALL_PREFIX#/ is done on purpose, since we
#       ensured that variable has a trailing slash.
sed -s "s|#APP_NAME#|$APP_NAME|g;\
        s|#UWSGI_PORT#|$UWSGI_PORT|g;\
        s|#DB_NAME#|$DB_NAME|g;\
        s|#DATE#|$DATE|g;\
        s|#NGINX_PORT#|$NGINX_PORT|g;\
        s|#INSTALL_PREFIX#/|$INSTALL_PREFIX|g;\
        s|#URL#|$URL|g;" $CDIR'/nginx.conf.template' > \
                                       $INSTALL_PATH'/conf/nginx.conf'
ln -s $INSTALL_PATH'/conf/nginx.conf' \
      $NGINX_AVAILABLE_PATH$APP_NAME'.conf'
ln -s $NGINX_AVAILABLE_PATH$APP_NAME'.conf' \
      $NGINX_ENABLE_PATH$APP_NAME'.conf'

service nginx restart

