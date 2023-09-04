#!/usr/bin/env bash

# Last Modified: 2023-09-01 12:08:14
# python racknerd.py &
proxy=socks5://127.0.0.1:1081
# Activate Debug Mode on failures ("c" to continue)
# pytest --pdb -s --incognito --headed --proxy=${proxy} racknerd.py
# pytest --pdb -s --incognito --headed --proxy=${proxy} presearch.py
# pytest -v --pdb -s --headed --proxy=${proxy} presearch.py
# pytest --user-data-dir="${HOME}/software/chrome-linux64" --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py

# google-chrome stable
# pytest --user-data-dir="${HOME}/software/chrome-linux64" --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py --demo

# chromium 114
pytest --binary-location="${HOME}/install/chrome-linux/chrome" --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py --demo

# pytest --binary-location="${HOME}/software/chrome-linux64/chrome"  --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py
# pytest --binary-location="${HOME}/software/chrome-linux64/chrome" --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py --wire
# pytest --user-data-dir="${HOME}/.config/google-chrome" --maximize -v --pdb -s --headed --proxy=${proxy} presearch.py
# pytest --user-data-dir="${HOME}/.config/google-chrome"  --maximize -v --headed --proxy=${proxy} presearch.py
