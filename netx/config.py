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
