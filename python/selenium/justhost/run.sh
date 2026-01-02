#!/usr/bin/env bash

# Last Modified: 2025-12-23 13:10:23
# conda install pytest
# python justhost.selenium.py &

proxy=socks5://127.0.0.1:1081
# pytest  --headed --proxy=socks5://127.0.0.1:1081 justhost.py

# Activate Debug Mode on failures ("c" to continue)
# google-chrome stable
# pytest --pdb -s --incognito --headed --proxy=socks5://127.0.0.1:1081 justhost.py
# pytest --user-data-dir="${HOME}/software/chrome-linux64" --pdb -s --incognito --headed --proxy=s{proxy} justhost.py

# conda info
# conda info -e
# conda env list

# chromium 122
pytest --binary-location="${HOME}/install/chrome-linux/chrome" --pdb -s --incognito --headed --proxy=${proxy} justhost.py
ssh justhost "nohup shutdown -r now"

ssh justhost "sudo shutdown -r now" || echo 0
