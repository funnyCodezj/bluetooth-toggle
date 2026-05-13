@echo off
chcp 65001 >nul
title 蓝牙开关 - 安装

echo ========================================
echo    蓝牙开关 - 安装程序
echo ========================================
echo.

:: Install customtkinter
echo [1/2] 安装依赖库 customtkinter...
python -m pip install customtkinter -q
if %errorlevel% neq 0 (
    echo 安装失败，请检查 Python 是否已安装
    pause
    exit /b 1
)
echo 依赖安装完成!
echo.

:: Create desktop shortcut via PowerShell
echo [2/2] 创建桌面快捷方式...
set SCRIPT_DIR=%~dp0

powershell.exe -Command ^
    $WshShell = New-Object -ComObject WScript.Shell; ^
    $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\蓝牙开关.lnk'); ^
    $Shortcut.TargetPath = 'powershell.exe'; ^
    $Shortcut.Arguments = '-NoProfile -Command Start-Process python -ArgumentList '''%SCRIPT_DIR%bluetooth_toggle.py''' -Verb RunAs'; ^
    $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; ^
    $Shortcut.Description = '一键开关电脑蓝牙'; ^
    $Shortcut.Save()

if %errorlevel% equ 0 (
    echo 桌面快捷方式已创建!
) else (
    echo 快捷方式创建失败，请手动运行 bluetooth_toggle.py
)

echo.
echo ========================================
echo    安装完成! 双击桌面 「蓝牙开关」 即可使用
echo ========================================
echo.
echo 首次使用会请求管理员权限，请点击「是」
echo.
pause
