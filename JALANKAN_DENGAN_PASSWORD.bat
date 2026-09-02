@echo off
title Portal Dosen Teknik Geologi - Password Pribadi
color 0A
cd /d "%~dp0"

if not exist venv\Scripts\activate.bat (
    echo Jalankan INSTALL_WEB.bat terlebih dahulu.
    pause
    exit /b
)

set /p ADMIN_PASSWORD=Masukkan password admin yang ingin digunakan: 
if "%ADMIN_PASSWORD%"=="" (
    echo Password tidak boleh kosong.
    pause
    exit /b
)

call venv\Scripts\activate.bat
start "" http://127.0.0.1:5000/admin/login
python app.py
pause
