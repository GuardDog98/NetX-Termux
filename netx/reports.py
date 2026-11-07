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
