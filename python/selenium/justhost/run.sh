#!/usr/bin/env bash

# conda install pytest
# python justhost.selenium.py &

# pytest  --headed --proxy=socks5://127.0.0.1:1081 justhost.py

# Activate Debug Mode on failures ("c" to continue)
pytest --pdb -s --incognito --headed --proxy=socks5://127.0.0.1:1081 justhost.py
