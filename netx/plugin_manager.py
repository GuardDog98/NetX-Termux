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
