@echo off
title Smart Library Management System
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Something went wrong. Make sure Python and required packages are installed.
    echo Run: pip install pillow openpyxl matplotlib
    pause
)
