#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

mkdir -p staticfiles
mkdir -p media
mkdir -p mediafiles

python manage.py collectstatic --noinput --clear

python manage.py migrate
