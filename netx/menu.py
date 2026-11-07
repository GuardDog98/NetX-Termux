from .dashboard import main as dashboard
from .monitor import get_interfaces
from .plugin_manager import list_plugins, run_plugin
from .marketplace import list_available, install_plugin
from .updater import check_update
from .reports import export_report

def main():
    while True:
        print("\n" + "=" * 35)
        print("       NETX-TERMUX v2.0.0")
        print("=" * 35)
        print("1. Live Dashboard")
        print("2. Network Interfaces")
        print("3. Plugin Manager")
        print("4. Plugin Marketplace")
        print("5. Check for Updates")
        print("6. Export JSON Report")
        print("0. Exit")

        choice = input("\nSelect an option: ").strip()

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

        input("\nPress Enter to continue...")
