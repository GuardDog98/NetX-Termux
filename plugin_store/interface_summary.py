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
