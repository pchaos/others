#!/usr/bin/env bash
# Modified: 2022-10-29 20:50:48

pytest test_genTABHTML.py 
echo copy files ... ~/myDocs/YUNIO/backup/main.htm 
cp /tmp/main.htm $HOME/myDocs/YUNIO/backup/main.htm 

echo Done

