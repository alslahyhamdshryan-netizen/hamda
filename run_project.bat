@echo off
cd /d "%~dp0"
python manage.py migrate --noinput
python setup_demo.py
call pnpm install
call pnpm build
start "عبد الإله HR - Django" cmd /k "python manage.py runserver 127.0.0.1:8000"
timeout /t 3 /nobreak >nul
start "عبد الإله HR" http://127.0.0.1:8000/
