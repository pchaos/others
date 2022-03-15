#!/usr/bin/env bash

# python racknerd.py &

# Activate Debug Mode on failures ("c" to continue)
# pytest --pdb -s --incognito --headed --proxy=socks5://127.0.0.1:1081 racknerd.py
# pytest --pdb -s --incognito --headed --proxy=socks5://127.0.0.1:1081 presearch.py
# pytest -v --pdb -s --headed --proxy=socks5://127.0.0.1:1081 presearch.py
# pytest --user-data-dir=${HOME}/.config/google-chrome --maximize -v --pdb -s --headed --proxy=socks5://127.0.0.1:1081 presearch.py
pytest --user-data-dir="${HOME}/.config/google-chrome" --maximize -v --headed --proxy=socks5://127.0.0.1:1081 presearch.py
# pytest  --pdb -s --headed --proxy=socks5://127.0.0.1:1081 racknerd.py

# nosetests --headed --proxy=socks5://127.0.0.1:1081 racknerd.py --pdb -s --incognito

