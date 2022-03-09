#!/usr/bin/env bash

# python justhost.selenium.py &

# pytest  --headed --proxy=socks5://127.0.0.1:1081 justhost.py &

# Activate Debug Mode on failures ("c" to continue)
pytest  --headed --proxy=socks5://127.0.0.1:1081 justhost.py --pdb -s --incognito
