#!/usr/bin/env bash
service mysql start
service memcached start
echo "create database encryptly_backend" | mysql -u root -ptest123
python manage.py makemigrations
python manage.py makemigrations encryptly_backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000