#!/usr/bin/env bash
# Modified: 2024-11-04 18:51:21

# pytest test_genTABHTML.py
pytest --headless -vvv test_genTABHTML.py::TestGenPchaosGitIo
# pytest --headless -vvv test_genTABHTML.py::TestGenPchaosGitIo::test_genHTML_phone
echo copy files ... $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/index.html index_phone.html
cp -v --update script.js styles.tab.css styles.tab.phone.css $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/
cp /tmp/index.html /tmp/index_phone.html $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/

echo Done
