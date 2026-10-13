"""Windows shell integration: right-click 'Generate seamless texture'."""
from __future__ import annotations

import sys
from pathlib import Path

if sys.platform == "win32":
    import winreg  # type: ignore[import-not-found]

_MENU_KEY = r"Software\Classes\Directory\shell\TextureGen"


def register_context_menu() -> None:
    """Add a shell context-menu entry. Windows-only; no-op elsewhere."""
    if sys.platform != "win32":
        return
    exe = Path(sys.executable).resolve()
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _MENU_KEY) as key:
        winreg.SetValue(key, "", winreg.REG_SZ, "Generate seamless texture")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _MENU_KEY + r"\command") as cmd:
        winreg.SetValue(cmd, "", winreg.REG_SZ, f'"{exe}" -m texturegen generate -p "%V"')


def unregister_context_menu() -> None:
    if sys.platform != "win32":
        return
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, _MENU_KEY + r"\command")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, _MENU_KEY)
    except FileNotFoundError:
        pass