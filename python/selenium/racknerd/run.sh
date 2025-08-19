#!/usr/bin/env bash

# Last Modified: 2025-08-18 10:51:33
# pip install pytest

# python racknerd.py &

proxy=socks5://127.0.0.1:1081
# Activate Debug Mode on failures ("c" to continue)
# pytest  --pdb -s --headed --proxy=socks5://127.0.0.1:1081 racknerd.py
# pytest --pdb -s --incognito --headed --proxy=socks5://127.0.0.1:1081 racknerd.py

# nosetests --headed --proxy=socks5://127.0.0.1:1081 racknerd.py --pdb -s --incognito


# chromium 114
pytest -v --binary-location="${HOME}/install/chrome-linux/chrome" --pdb -s --incognito --gui --proxy=${proxy} racknerd.py
