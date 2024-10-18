#!/usr/bin/env bash
# Modified: 2024-10-17 16:50:36

# pytest test_genTABHTML.py
pytest --headless -vvv test_genTABHTML.py
echo copy files ... ~/myDocs/YUNIO/backup/main.htm
cp /tmp/main.htm $HOME/myDocs/YUNIO/backup/main.htm
cp /tmp/index.html $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/

echo Done
