#!/usr/bin/env bash
pytest test_genTABHTML.py 
echo copy files ... ~/myDocs/YUNIO/backup/main.htm 
cp /tmp/main.htm /home/myuser/myDocs/YUNIO/backup/main.htm 

echo Done

