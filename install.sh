#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg install python -y
python -m pip install .

echo "NetX-Termux installed! Run: netx"
