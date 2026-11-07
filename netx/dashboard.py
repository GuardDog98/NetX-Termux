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

            print("\nTraffic history:")
            for r, t in history:
                print(f"RX {'#' * min(int(r / 1024), 30)}")
                print(f"TX {'+' * min(int(t / 1024), 30)}")

            previous = current

    except KeyboardInterrupt:
        print("\nDashboard dayandırıldı.")

