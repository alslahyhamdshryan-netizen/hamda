#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 manage.py migrate --noinput
python3 setup_demo.py
pnpm install --silent
pnpm build
trap 'kill 0' EXIT
python3 manage.py runserver 127.0.0.1:8000 &
DJANGO_API_URL=http://127.0.0.1:8000 node dist/index.js
