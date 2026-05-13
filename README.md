# BluetoothToggle

[English](#english) | [中文](#中文)

---

## 中文

Windows 蓝牙开关桌面工具 — 一键开启/关闭蓝牙，无需管理员权限。

![screenshot](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)

### 功能

- 一键切换蓝牙开关
- 实时显示蓝牙状态（开启/关闭）
- 显示蓝牙适配器名称
- 诊断功能（检查权限、测试切换）
- 无需管理员权限，无需安装
- Dark 风格界面

### 使用方法

1. 从 [Releases](https://github.com/funnyCodezj/bluetooth-toggle/releases) 下载最新版 `BluetoothToggle.exe`
2. 双击运行
3. 首次使用会弹出 Windows 权限确认窗口，点击「是」
4. 点击开关切换蓝牙

### 技术原理

使用 `Windows.Devices.Radios` API（通过 [winsdk](https://github.com/pywinrt/python-winsdk) Python 绑定）直接控制蓝牙无线电状态，与 Windows 设置/Action Center 中的蓝牙开关等效。

- **Python 3.10+** — 运行时
- **customtkinter** — 界面框架
- **winsdk** — Windows Radio API 绑定
- **PyInstaller** — 打包为单文件 exe

### 自行构建

```bash
pip install -r requirements.txt
pyinstaller --noconsole --onefile --name "BluetoothToggle" ^
  --add-data "<venv>/Lib/site-packages/customtkinter/assets;customtkinter/assets" ^
  --hidden-import PIL._tkinter_finder --collect-all winsdk ^
  bluetooth_toggle.py
```

产出在 `dist/BluetoothToggle.exe`。

---

## English

A desktop tool to toggle Windows Bluetooth radio on/off — no admin privileges required.

### Features

- One-click Bluetooth toggle
- Real-time status display (on/off)
- Bluetooth adapter name shown
- Diagnostic tools (permission check, test toggle)
- No admin rights needed, no installation required
- Dark theme UI

### Usage

1. Download the latest `BluetoothToggle.exe` from [Releases](https://github.com/funnyCodezj/bluetooth-toggle/releases)
2. Double-click to run
3. On first run, Windows will prompt for permission — click "Yes"
4. Click the switch to toggle Bluetooth

### How It Works

Uses the `Windows.Devices.Radios` API (via [winsdk](https://github.com/pywinrt/python-winsdk) Python bindings) to control the Bluetooth radio state directly — identical to the Bluetooth toggle in Windows Settings / Action Center.

- **Python 3.10+** — runtime
- **customtkinter** — GUI framework
- **winsdk** — Windows Radio API bindings
- **PyInstaller** — packaged as single-file exe

### Build from Source

```bash
pip install -r requirements.txt
pyinstaller --noconsole --onefile --name "BluetoothToggle" ^
  --add-data "<venv>/Lib/site-packages/customtkinter/assets;customtkinter/assets" ^
  --hidden-import PIL._tkinter_finder --collect-all winsdk ^
  bluetooth_toggle.py
```

Output at `dist/BluetoothToggle.exe`.
