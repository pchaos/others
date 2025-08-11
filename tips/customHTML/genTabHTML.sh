#!/usr/bin/env bash
# Modified: 2025-08-06 12:45:44

# pytest test_genTABHTML.py
pytest --headless -vvv test_genTABHTML.py::TestGenTABHTML
if [[ $? -ne 0 ]]; then
  echo "生成文件失败, exiting."
  exit 1
fi
echo copy files ... ~/myDocs/YUNIO/backup/main.htm
cp -v --update /tmp/main.htm $HOME/myDocs/YUNIO/backup/main.htm
cp -v --update /tmp/main.htm $HOME/Downloads/s1081.gfw.pac $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/

echo Done
