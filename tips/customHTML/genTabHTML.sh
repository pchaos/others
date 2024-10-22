#!/usr/bin/env bash
# Modified: 2024-10-18 11:44:46

# pytest test_genTABHTML.py
pytest --headless -vvv test_genTABHTML.py::test_genTABHTML
echo copy files ... ~/myDocs/YUNIO/backup/main.htm
cp /tmp/main.htm $HOME/myDocs/YUNIO/backup/main.htm

echo Done
