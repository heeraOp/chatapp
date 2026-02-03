#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python chatapp/manage.py collectstatic --noinput
python chatapp/manage.py migrate
