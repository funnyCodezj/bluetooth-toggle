@echo off
chcp 65001 >nul
title 蓝牙开关 - 打包程序

echo ========================================
echo    打包蓝牙开关为 exe
echo ========================================
echo.

setlocal enabledelayedexpansion

:: Find customtkinter path
for /f "tokens=*" %%i in ('python -c "import customtkinter,os;print(os.path.dirname(customtkinter.__file__).replace('\\','/'))"') do set CTK_PATH=%%i

echo customtkinter 路径: %CTK_PATH%
echo.

:: Build with PyInstaller
echo 正在打包，请稍候...
pyinstaller --noconsole --onefile ^
    --name "BluetoothToggle" ^
    --uac-admin ^
    --add-data "%CTK_PATH%/assets;customtkinter/assets" ^
    --hidden-import "PIL._tkinter_finder" ^
    --noconfirm ^
    --clean ^
    bluetooth_toggle.py

if %errorlevel% neq 0 (
    echo.
    echo ✗ 打包失败！
    pause
    exit /b 1
)

echo.
echo ✓ 打包成功！
echo 输出文件: dist\BluetoothToggle.exe
echo.

echo 正在创建桌面快捷方式...
set DIST_PATH=%~dp0dist\BluetoothToggle.exe

powershell -Command ^
    $WshShell = New-Object -ComObject WScript.Shell; ^
    $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\蓝牙开关.lnk'); ^
    $Shortcut.TargetPath = '%DIST_PATH:\=\\%'; ^
    $Shortcut.WorkingDirectory = '%~dp0dist'; ^
    $Shortcut.Description = '一键开关电脑蓝牙'; ^
    $Shortcut.Save();

echo ✓ 桌面快捷方式已创建
echo.
echo ========================================
echo    打包完成! exe 位于: dist\BluetoothToggle.exe
echo    双击桌面「蓝牙开关」即可运行
echo ========================================
echo.
pause
