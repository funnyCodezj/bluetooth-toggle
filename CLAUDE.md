# BluetoothToggle

Windows 蓝牙开关桌面工具。一键开启/关闭蓝牙，无需管理员权限。

## 技术栈

- **Python 3.10+** — 运行时
- **customtkinter** — GUI 框架（dark 风格）
- **winsdk** — Windows Radio API 绑定（`Windows.Devices.Radios`）
- **PyInstaller** — 打包为单文件 exe

## 项目结构

```
bluetooth_toggle.py    # 主程序（蓝牙管理 + GUI）
蓝牙开关.vbs           # 无黑窗口启动器（源码运行时用）
build.bat              # PyInstaller 打包脚本
install.bat            # 安装依赖 + 创建桌面快捷方式
requirements.txt       # Python 依赖
dist/BluetoothToggle.exe  # 打包后的可执行文件
```

## 核心架构

`BluetoothManager` — winsdk 封装层，通过 `asyncio.run()` 桥接异步 Radio API 到同步 GUI。

```
用户点击 → on_toggle() → BluetoothManager.toggle() → asyncio.run(_toggle())
  → Radio.request_access_async()  →  Radio.set_state_async(ON|OFF)
  → 验证状态 → 更新 UI
```

关键设计：
- **无需管理员权限** — Radio API 走 Windows 原生权限弹窗，不需要 admin
- **不调 PowerShell** — 没有黑窗口闪动，没有编码问题
- **asyncio.run() 做桥接** — 每次调用创建独立事件循环，操作完成后销毁

## 构建

```bash
pip install -r requirements.txt
pyinstaller --noconsole --onefile --name "BluetoothToggle" ^
  --add-data "<venv>/Lib/site-packages/customtkinter/assets;customtkinter/assets" ^
  --hidden-import PIL._tkinter_finder --collect-all winsdk ^
  bluetooth_toggle.py
```

产出在 `dist/BluetoothToggle.exe`（约 37 MB）。

## 注意事项

- `Radio.request_access_async()` 首次调用会弹出 Windows 权限确认窗口，用户允许后不再出现
- `set_state_async()` 后需要 `asyncio.sleep(0.3)` 等待状态稳定再验证
- winsdk 的 `IAsyncOperation` 可直接 `await`，但 `asyncio.run(op)` 不行（不是 coroutine），须包在 `async def` 里
- 蓝牙适配器名称来自 WinRT 原生字符串，无编码问题
- 字体使用 `Microsoft YaHei`，Windows 中文系统自带
