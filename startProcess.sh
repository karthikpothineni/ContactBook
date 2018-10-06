#!/usr/bin/env bash
if [ -z "$DB_HOST" ]; then     echo "Need to set DB_HOST"; exit 1; fi
if [ -z "$DB_PORT" ]; then     echo "Need to set DB_PORT"; exit 1; fi
if [ -z "$DB_USER" ]; then     echo "Need to set DB_USER"; exit 1; fi
if [ -z "$DB_PWD" ]; then     echo "Need to set DB_PSWD"; exit 1; fi
if [ -z "$DB_NAME" ]; then     echo "Need to set DB_NAME"; exit 1; fi

python3.5 manage.py makemigrations contact_book
python3.5 manage.py migrate
python3.5 /manage.py collectstatic --noinput

touch /log.log
cp /conf/nginx.conf /etc/nginx/sites-enabled/default
cp /conf/custom_50x.html /usr/share/nginx/html/
cp /conf/custom_400.html /usr/share/nginx/html/
service nginx start
uwsgi --socket :9000 --module ContactBook.wsgi -b 32768 --threads 5 --enable-threads > /log.log 2>&1
tail -f /log.log
