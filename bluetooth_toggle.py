"""Bluetooth Toggle - Desktop app for toggling Windows Bluetooth radio.

Uses Windows.Devices.Radios API (via winsdk) - no admin rights needed.
"""
import asyncio
import os
import sys

import customtkinter as ctk
from winsdk.windows.devices.radios import (
    Radio,
    RadioKind,
    RadioState,
    RadioAccessStatus,
)


# ── Bluetooth manager (async) ──────────────────────────────
class BluetoothManager:
    """Wraps the WinRT Radio API for Bluetooth."""

    def get_state(self) -> bool | None:
        """True=on, False=off, None=not found."""
        return asyncio.run(self._get_state())

    def toggle(self, turn_on: bool) -> tuple[bool, str]:
        """(success, error_message)"""
        return asyncio.run(self._toggle(turn_on))

    def get_name(self) -> str:
        return asyncio.run(self._get_name())

    @staticmethod
    async def _get_bt_radio():
        radios = await Radio.get_radios_async()
        for r in radios:
            if r.kind == RadioKind.BLUETOOTH:
                return r
        return None

    @staticmethod
    async def _get_state():
        radio = await BluetoothManager._get_bt_radio()
        if radio is None:
            return None
        return radio.state == RadioState.ON

    @staticmethod
    async def _get_name():
        radio = await BluetoothManager._get_bt_radio()
        if radio is None:
            return ""
        return radio.name

    @staticmethod
    async def _toggle(turn_on: bool):
        radio = await BluetoothManager._get_bt_radio()
        if radio is None:
            return False, "未检测到蓝牙适配器"

        # Request access (shows prompt on first use, cached afterwards)
        access = await Radio.request_access_async()
        if access != RadioAccessStatus.ALLOWED:
            msg = {
                RadioAccessStatus.DENIED_BY_USER: "用户拒绝了访问权限",
                RadioAccessStatus.DENIED_BY_SYSTEM: "系统拒绝了访问权限",
            }.get(access, f"访问被拒绝 (代码 {access})")
            return False, msg

        new_state = RadioState.ON if turn_on else RadioState.OFF
        await radio.set_state_async(new_state)
        await asyncio.sleep(0.3)

        # Verify
        radio2 = await BluetoothManager._get_bt_radio()
        if radio2 is None:
            return False, "切换后无法读取蓝牙状态"

        if turn_on and radio2.state == RadioState.ON:
            return True, ""
        if not turn_on and radio2.state == RadioState.OFF:
            return True, ""

        return False, f"蓝牙状态异常 (state={radio2.state})"

    @staticmethod
    async def _check_access():
        try:
            return await Radio.request_access_async()
        except TypeError:
            return Radio.request_access_async().get_results()


# ── GUI ────────────────────────────────────────────────────
class BluetoothToggleApp(ctk.CTk):
    def __init__(self, bluetooth: BluetoothManager):
        super().__init__()
        self.bt = bluetooth
        self.is_toggling = False

        self.title("蓝牙开关")
        self.geometry("380x220")
        self.resizable(False, False)
        self.after(100, self._center_window)
        self._set_icon()

        self._build_ui()
        self.after(300, self.init_bluetooth)

    # ── window ──────────────────────────────────────────
    def _set_icon(self):
        try:
            icon_path = os.path.join(
                sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(__file__),
                "logo.ico",
            )
            self.iconbitmap(icon_path)
        except Exception:
            pass

    def _center_window(self):
        self.update_idletasks()
        w, h = 380, 220
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI layout ───────────────────────────────────────
    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self, text="蓝牙控制", font=("Microsoft YaHei", 20, "bold")
        )
        self.title_label.pack(pady=(20, 4))

        self.device_label = ctk.CTkLabel(
            self, text="", font=("Microsoft YaHei", 12),
            text_color="gray"
        )
        self.device_label.pack(pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            self, text="检测中...", font=("Microsoft YaHei", 18)
        )
        self.status_label.pack(pady=(0, 10))

        self.toggle_switch = ctk.CTkSwitch(
            self, text="",
            command=self.on_toggle,
            switch_width=60, switch_height=28,
        )
        self.toggle_switch.pack(pady=(0, 6))

        self.error_label = ctk.CTkLabel(
            self, text="", font=("Microsoft YaHei", 11),
            text_color="#FF9800", wraplength=360
        )
        self.error_label.pack(pady=(0, 4))

        self.diag_button = ctk.CTkButton(
            self, text="诊断",
            width=50, height=22,
            font=("Microsoft YaHei", 10),
            command=self.run_diagnostics,
            fg_color="#555555", hover_color="#666666",
        )
        self.diag_button.pack()

    # ── init ────────────────────────────────────────────
    def init_bluetooth(self):
        name = self.bt.get_name()
        state = self.bt.get_state()

        if name:
            self.device_label.configure(text=name)

        if state is None:
            self.status_label.configure(text="未检测到蓝牙适配器", text_color="red")
            self.toggle_switch.configure(state="disabled")
            self.diag_button.configure(state="disabled")
            self.device_label.configure(text="")
            return

        self._update_status(state)
        self.error_label.configure(text="")

    def _update_status(self, on: bool):
        if on:
            self.status_label.configure(text="蓝牙已开启", text_color="#4CAF50")
            self.toggle_switch.select()
        else:
            self.status_label.configure(text="蓝牙已关闭", text_color="#F44336")
            self.toggle_switch.deselect()

    # ── toggle ──────────────────────────────────────────
    def on_toggle(self):
        if self.is_toggling:
            return
        self.is_toggling = True
        self.toggle_switch.configure(state="disabled")
        self.error_label.configure(text="")

        target_on = self.toggle_switch.get() == 1
        action = "开启" if target_on else "关闭"
        self.status_label.configure(text=f"正在{action}蓝牙...", text_color="gray")
        self.update()

        ok, err = self.bt.toggle(target_on)

        if ok:
            self.status_label.configure(text=f"已{action}蓝牙")
            self.after(400, self._refresh)
        else:
            self.status_label.configure(text=f"{action}失败", text_color="red")
            self.error_label.configure(text=f"错误: {err[:100]}")
            self._refresh()  # rollback switch

        self.toggle_switch.configure(state="normal")
        self.is_toggling = False

    def _refresh(self):
        state = self.bt.get_state()
        if state is not None:
            self._update_status(state)

    # ── diagnostics ─────────────────────────────────────
    def run_diagnostics(self):
        lines = []
        name = self.bt.get_name()
        lines.append(f"蓝牙适配器: {name or '未检测到'}")

        state = self.bt.get_state()
        lines.append(f"蓝牙状态: {'开启' if state else '关闭' if state is False else '未知'}")

        # Test access (no actual toggle)
        try:
            access = asyncio.run(self.bt._check_access())
            access_names = {
                RadioAccessStatus.ALLOWED: "允许",
                RadioAccessStatus.DENIED_BY_USER: "被用户拒绝",
                RadioAccessStatus.DENIED_BY_SYSTEM: "被系统拒绝",
            }
            lines.append(f"切换权限: {access_names.get(access, str(access))}")
        except Exception as e:
            lines.append(f"切换权限检查失败: {e}")

        diag = ctk.CTkToplevel(self)
        diag.title("诊断信息")
        diag.geometry("480x300")
        diag.transient(self)
        text = ctk.CTkTextbox(diag, font=("Microsoft YaHei", 11), wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", "\n".join(lines))
        text.configure(state="disabled")


# ── entry ──────────────────────────────────────────────────
def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = BluetoothToggleApp(BluetoothManager())
    app.mainloop()


if __name__ == "__main__":
    main()
