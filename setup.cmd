@echo off
python manage.py createdb
python manage.py makemigrations
python manage.py migrate
@echo on