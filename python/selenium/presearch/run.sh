#!/usr/bin/env bash

# python racknerd.py &
proxy=socks5://127.0.0.1:1081
# Activate Debug Mode on failures ("c" to continue)
# pytest --pdb -s --incognito --headed --proxy=${proxy} racknerd.py
# pytest --pdb -s --incognito --headed --proxy=${proxy} presearch.py
# pytest -v --pdb -s --headed --proxy=${proxy} presearch.py
pytest --user-data-dir="${HOME}/.config/google-chrome" --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py
# pytest --user-data-dir="${HOME}/.config/google-chrome"  --maximize -v --headed --proxy=${proxy} presearch.py
# pytest  --pdb -s --headed --proxy=${proxy} racknerd.py
