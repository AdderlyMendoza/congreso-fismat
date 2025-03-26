#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

mkdir -p staticfiles
mkdir -p media

python manage.py collectstatic --noinput --clear

python manage.py migrate

