@echo off
title 蓝牙开关
cd /d "%~dp0"
echo 正在请求管理员权限...
powershell.exe -Command "Start-Process python -ArgumentList 'bluetooth_toggle.py' -Verb RunAs -WorkingDirectory '%~dp0'"
