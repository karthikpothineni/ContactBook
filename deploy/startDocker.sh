#!/usr/bin/env bash

cd ..

docker build -t contact_book_qa .

docker run -d -i -t \
-e DJANGO_SETTINGS_MODULE='ContactBook.settings.qa' \
-e DB_HOST=prod-rds-ie-xx.yyy.eu-west-1.rds.amazonaws.com \
-e DB_PORT=5432 \
-e DB_USER='user_name' \
-e DB_PWD='password' \
-e DB_NAME='db_name' \
-p 5575:80 \
--name contact_book_qa \
--hostname contact_book_qa contact_book_qa
