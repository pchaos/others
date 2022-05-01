#!/usr/bin/env bash

# pip install pytest

# python racknerd.py &

# Activate Debug Mode on failures ("c" to continue)
# pytest  --pdb -s --headed --proxy=socks5://127.0.0.1:1081 racknerd.py
pytest --pdb -s --incognito --headed --proxy=socks5://127.0.0.1:1081 racknerd.py

# nosetests --headed --proxy=socks5://127.0.0.1:1081 racknerd.py --pdb -s --incognito


