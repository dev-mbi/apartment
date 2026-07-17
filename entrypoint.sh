#!/bin/sh
set -e
python seed_admin.py
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 "app:create_app()"
