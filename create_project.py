from pathlib import Path

files = {
    "main.py": '''
from netx.menu import main

if __name__ == "__main__":
    main()
''',
    "pyproject.toml": '''
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "netx-termux"
version = "2.0.0"
description = "Network monitoring toolkit for Termux"
requires-python = ">=3.9"

[project.scripts]
netx = "netx.menu:main"

[tool.setuptools.packages.find]
include = ["netx*"]
''',
    "requirements.txt": "",
    ".gitignore": '''
__pycache__/
*.pyc
*.egg-info/
reports/
config.json
''',
    "LICENSE": '''
MIT License

Copyright (c) 2026 NetX-Termux

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
''',
    "README.md": '''
# 🚀 NetX-Termux v2.0.0

A modern network monitoring toolkit for Termux.

## Features
- Interactive terminal dashboard
- Live RX/TX traffic monitoring
- Traffic history graphs
- Plugin marketplace
- Configuration system
- GitHub update checker
- JSON statistics export

## Installation

```bash
pkg install python git
git clone git@github.com:GuardDog98/NetX-Termux.git
cd NetX-Termux
python -m pip install .
netx
''',
    "CHANGELOG.md": '''
# Changelog

## v2.0.0
- Added interactive dashboard
- Added traffic history
- Added plugin marketplace
- Added configuration support
- Added GitHub update checker
- Added JSON report export
''',
"install.sh": '''
#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg install python -y
python -m pip install .

echo "NetX-Termux installed! Run: netx"
''',
"netx/__init__.py": '''
__version__ = "2.0.0"
''',
"netx/config.py": '''
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".netx_config.json"

DEFAULTS = {
    "refresh_seconds": 2,
    "history_size": 20,
    "show_banner": True
}

def load():
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text())
            return {**DEFAULTS, **data}
        except (ValueError, OSError):
            pass

    save(DEFAULTS)
    return DEFAULTS.copy()

def save(data):
    CONFIG_FILE.write_text(json.dumps(data, indent=4))
''',
"netx/monitor.py": '''
from pathlib import Path

def get_interfaces():
    interfaces = {}

    try:
        lines = Path("/proc/net/dev").read_text().splitlines()[2:]

        for line in lines:
            if ":" not in line:
                continue

            name, data = line.split(":", 1)
            values = data.split()

            if len(values) >= 9:
                interfaces[name.strip()] = {
                    "rx_bytes": int(values[0]),
                    "tx_bytes": int(values[8])
                }

    except (OSError, ValueError):
        pass

    return interfaces

def get_totals():
    interfaces = get_interfaces()

    return {
        "rx_bytes": sum(v["rx_bytes"] for v in interfaces.values()),
        "tx_bytes": sum(v["tx_bytes"] for v in interfaces.values())
    }
''',
"netx/dashboard.py": '''
import time
import os
from .monitor import get_totals
from .config import load

def main():
    config = load()
    interval = max(1, config["refresh_seconds"])
    history = []
    previous = get_totals()

    print("NetX-Termux Dashboard")
    print("Dayandırmaq üçün CTRL + C bas.")

    try:
        while True:
            time.sleep(interval)
            current = get_totals()

            rx = max(0, current["rx_bytes"] - previous["rx_bytes"])
            tx = max(0, current["tx_bytes"] - previous["tx_bytes"])

            rx_speed = rx / interval
            tx_speed = tx / interval

            history.append((rx_speed, tx_speed))
            history = history[-config["history_size"]:]

            os.system("clear")
            print("=== NetX LIVE DASHBOARD ===")
            print(f"Download: {rx_speed / 1024:.2f} KB/s")
            print(f"Upload:   {tx_speed / 1024:.2f} KB/s")

            print("\\nTraffic history:")
            for r, t in history:
                print(f"RX {'#' * min(int(r / 1024), 30)}")
                print(f"TX {'+' * min(int(t / 1024), 30)}")

            previous = current

    except KeyboardInterrupt:
        print("\\nDashboard dayandırıldı.")

''',
"netx/plugin_manager.py": '''
import importlib.util
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent / "plugins"

def list_plugins():
    PLUGIN_DIR.mkdir(exist_ok=True)
    return sorted(PLUGIN_DIR.glob("*.py"))

def run_plugin(name):
    path = PLUGIN_DIR / f"{name}.py"

    if not path.is_file():
        print("Plugin tapılmadı!")
        return

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "run"):
        module.run()
    else:
        print("Plugin daxilində run() funksiyası yoxdur.")
''',
"netx/marketplace.py": '''
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
STORE = ROOT / "plugin_store"
PLUGINS = ROOT / "plugins"

def list_available():
    STORE.mkdir(exist_ok=True)
    return sorted(STORE.glob("*.py"))

def install_plugin(name):
    source = STORE / f"{name}.py"
    destination = PLUGINS / f"{name}.py"

    if not source.is_file():
        print("Plugin not found!")
        return

    PLUGINS.mkdir(exist_ok=True)
    shutil.copy2(source, destination)
    print(f"Plugin installed: {name}")
''',
"netx/updater.py": '''
import json
import urllib.request

REPO = "GuardDog98/NetX-Termux"
CURRENT_VERSION = "2.0.0"

def check_update():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "NetX-Termux"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())

        latest = data.get("tag_name", "").lstrip("v")

        print(f"Current version: {CURRENT_VERSION}")
        print(f"Latest version: {latest}")

        if latest and latest != CURRENT_VERSION:
            print("A newer release may be available!")
        else:
            print("You are using the latest release.")

    except Exception as error:
        print(f"Update check failed: {error}")
''',
"netx/reports.py": '''
import json
from datetime import datetime
from pathlib import Path
from .monitor import get_interfaces

def export_report():
    report = {
        "version": "2.0.0",
        "created_at": datetime.now().isoformat(),
        "interfaces": get_interfaces()
    }

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    filename = report_dir / (
        "netx_report_" +
        datetime.now().strftime("%Y%m%d_%H%M%S") +
        ".json"
    )

    filename.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(f"Report exported: {filename}")
''',
"netx/menu.py": '''
from .dashboard import main as dashboard
from .monitor import get_interfaces
from .plugin_manager import list_plugins, run_plugin
from .marketplace import list_available, install_plugin
from .updater import check_update
from .reports import export_report

def main():
    while True:
        print("\\n" + "=" * 35)
        print("       NETX-TERMUX v2.0.0")
        print("=" * 35)
        print("1. Live Dashboard")
        print("2. Network Interfaces")
        print("3. Plugin Manager")
        print("4. Plugin Marketplace")
        print("5. Check for Updates")
        print("6. Export JSON Report")
        print("0. Exit")

        choice = input("\\nSelect an option: ").strip()

        if choice == "1":
            dashboard()

        elif choice == "2":
            for name, stats in get_interfaces().items():
                print(f"{name}: RX={stats['rx_bytes']} TX={stats['tx_bytes']}")

        elif choice == "3":
            plugins = list_plugins()
            for plugin in plugins:
                print("-", plugin.stem)

            name = input("Plugin name to run: ").strip()
            if name:
                run_plugin(name)

        elif choice == "4":
            available = list_available()
            for plugin in available:
                print("-", plugin.stem)

            name = input("Plugin name to install: ").strip()
            if name:
                install_plugin(name)

        elif choice == "5":
            check_update()

        elif choice == "6":
            export_report()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")

        input("\\nPress Enter to continue...")
''',
"plugins/example_hello.py": '''
def run():
    print("Hello from NetX-Termux!")
    print("Your plugin is working successfully.")
''',
"plugin_store/connectivity_tips.py": '''
def run():
    print("NETX CONNECTIVITY TIPS")
    print("1. Check your Wi-Fi connection.")
    print("2. Keep your device software updated.")
    print("3. Use trusted networks.")
    print("4. Restart your connection if needed.")
''',
"plugin_store/interface_summary.py": '''
from netx.monitor import get_interfaces

def run():
    print("NETWORK INTERFACE SUMMARY")

    interfaces = get_interfaces()

    if not interfaces:
        print("No network interfaces found.")
        return

    for name, stats in interfaces.items():
        print(f"Interface: {name}")
        print(f"Received: {stats['rx_bytes']} bytes")
        print(f"Sent: {stats['tx_bytes']} bytes")
''',
}
for name, content in files.items():
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8")

print("NetX-Termux v2.0.0 files created!")
