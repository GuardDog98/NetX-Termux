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
