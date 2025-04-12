#!/usr/bin/env bash
# Modified: 2024-11-16 23:38:04

# pytest test_genTABHTML.py
pytest --headless -vvv test_genTABHTML.py::TestGenTABHTML
echo copy files ... ~/myDocs/YUNIO/backup/main.htm
cp -v --update /tmp/main.htm $HOME/myDocs/YUNIO/backup/main.htm
cp -v --update /tmp/main.htm $HOME/Downloads/s1081.gfw.pac $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/

echo Done
