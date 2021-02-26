#!/usr/bin/env bash

 # pytest --headed ibmcloud.py
 # pytest --headed --proxy=127.0.0.1:1080 ibmcloud.py
 pytest --headed --proxy=127.0.0.1:8087 ibmcloud.py
 # pytest --headed --proxy=socks5://127.0.0.1:1081 ibmcloud.py
 # nosetests --headed --proxy=127.0.0.1:1080 ibmcloud.py
 # nosetests --headed --proxy=127.0.0.1:1080 --pdb -s ibmcloud.py
 # pytest --proxy=127.0.0.1:1080 ibmcloud.py
