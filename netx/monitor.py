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
