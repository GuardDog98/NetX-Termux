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
