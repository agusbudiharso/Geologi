@echo off
title Portal Dosen Teknik Geologi
color 0B
cd /d "%~dp0"

if not exist venv\Scripts\activate.bat (
    echo Belum diinstal. Jalankan INSTALL_WEB.bat terlebih dahulu.
    pause
    exit /b
)

call venv\Scripts\activate.bat
start "" http://127.0.0.1:5000
echo ==============================================
echo PORTAL DOSEN SEDANG BERJALAN
echo http://127.0.0.1:5000
echo.
echo Jangan tutup jendela ini selama web digunakan.
echo Tekan CTRL+C untuk menghentikan server.
echo ==============================================
python app.py
pause
