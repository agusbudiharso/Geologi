@echo off
title Instalasi Portal Dosen Teknik Geologi
color 0A
cd /d "%~dp0"

echo ==============================================
echo   INSTALASI PORTAL DOSEN TEKNIK GEOLOGI
echo   UNIVERSITAS PRISMA MANADO
echo ==============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python belum ditemukan.
    echo Instal Python dan centang "Add Python to PATH".
    pause
    exit /b
)

if not exist venv (
    echo Membuat virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install flask

echo.
echo Instalasi selesai.
echo Password admin awal: PrismaGeologi2026
echo Sangat disarankan mengganti password sebelum web dipublikasikan.
echo.
pause
